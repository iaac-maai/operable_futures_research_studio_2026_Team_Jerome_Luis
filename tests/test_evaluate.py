import pytest

from triage.evaluate import confusion, metrics, safety_table

# Synthetic labels for testing the arithmetic only, not results.
TRUTH = ["High", "High", "High", "High", "Medium", "Medium", "Low", "Low", "Low", "High"]
PRED = ["High", "Expert needed", "Medium", "Low", "Low", "High", "Low", "Medium", "Expert needed", "Retake"]


def test_confusion_counts_every_cell():
    table = confusion(TRUTH, PRED)
    assert table["High"] == {"Low": 1, "Medium": 1, "High": 1, "Expert needed": 1, "Retake": 1}
    assert sum(sum(row.values()) for row in table.values()) == len(TRUTH)


def test_safety_table():
    assert safety_table(TRUTH, PRED) == {
        "TP": 2, "FN": 2, "FP": 2, "TN": 3, "retake": 1, "retake_high": 1, "false_all_clear": 2,
    }


def test_metrics():
    m = metrics(TRUTH, PRED)
    assert m["recall_high"] == 0.5
    assert m["missed_high"] == 0.5
    assert m["referral_rate"] == pytest.approx(4 / 9)
    assert m["precision"] == 0.5
    assert m["retake_rate"] == 0.1


def test_expert_needed_on_a_high_crack_counts_as_caught():
    assert safety_table(["High"], ["Expert needed"])["TP"] == 1


def test_no_high_cases_gives_none_not_zero():
    assert metrics(["Low"], ["Low"])["recall_high"] is None


@pytest.mark.parametrize("truth, pred", [(["High"], ["Safe"]), (["Severe"], ["High"]), (["High"], [])])
def test_bad_input_raises(truth, pred):
    with pytest.raises(ValueError):
        confusion(truth, pred)
