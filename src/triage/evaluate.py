"""Confusion tables for the tool and the non-AI baseline. Spec: spec/features/evaluation.md."""

from collections import Counter

TRUTH = ["Low", "Medium", "High"]
OUTPUTS = ["Low", "Medium", "High", "Expert needed", "Retake"]
FLAGGED = {"High", "Expert needed"}


def confusion(truth: list[str], predicted: list[str]) -> dict[str, dict[str, int]]:
    """Table 2: rows are the engineer's rating, columns the tool output."""
    if len(truth) != len(predicted):
        raise ValueError("truth and predicted must have the same length")
    counts = Counter(zip(truth, predicted))
    for t, p in counts:
        if t not in TRUTH or p not in OUTPUTS:
            raise ValueError(f"unknown label pair: {t!r}, {p!r}")
    return {t: {p: counts[(t, p)] for p in OUTPUTS} for t in TRUTH}


def safety_table(truth: list[str], predicted: list[str]) -> dict[str, int]:
    """Table 1: positive is engineer High, flagged is High or Expert needed. Retakes are counted apart."""
    table = confusion(truth, predicted)
    high = table["High"]
    others = [table["Low"], table["Medium"]]
    return {
        "TP": sum(high[p] for p in FLAGGED),
        "FN": high["Low"] + high["Medium"],
        "FP": sum(row[p] for row in others for p in FLAGGED),
        "TN": sum(row["Low"] + row["Medium"] for row in others),
        "retake": sum(row["Retake"] for row in table.values()),
        "retake_high": high["Retake"],
        "false_all_clear": table["Medium"]["Low"] + table["High"]["Low"],
    }


def metrics(truth: list[str], predicted: list[str]) -> dict[str, float | None]:
    """Ratios from Table 1; None when the denominator is zero."""
    s = safety_table(truth, predicted)
    assessed = s["TP"] + s["FN"] + s["FP"] + s["TN"]

    def ratio(a, b):
        return a / b if b else None

    return {
        "recall_high": ratio(s["TP"], s["TP"] + s["FN"]),
        "missed_high": ratio(s["FN"], s["TP"] + s["FN"]),
        "referral_rate": ratio(s["TP"] + s["FP"], assessed),
        "precision": ratio(s["TP"], s["TP"] + s["FP"]),
        "retake_rate": ratio(s["retake"], assessed + s["retake"]),
    }
