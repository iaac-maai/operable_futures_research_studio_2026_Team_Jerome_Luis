# Feature: evaluation (`src/triage/evaluate.py`)

Status: definitions and code ready; no results yet. All numbers come from a held-out test set of engineer-labelled photos, which does not exist yet.

## Ground truth and comparisons
- Ground truth: the rating (Low, Medium, High) of an engineer who assessed the building on site (deck slide 10: "buildings an engineer already assessed").
- Tool: the output of `triage()` on the photo.
- Non-AI baseline: an engineer's visual check of the same photo, without the tool. Scored with the same tables.

![Confusion template](../../figures/07_confusion_template.png)

## Table 1: the safety question (binary)
Positive = the on-site engineer rated the crack High. "Flagged" = the tool sent the case to a human (High or Expert needed).

|  | Tool flags (High or Expert needed) | Tool does not flag (Low or Medium) |
|---|---|---|
| **Engineer: High** | **TP**: danger caught, engineer visits | **FN**: missed danger, a wrong all-clear lands on residents. Stop condition. |
| **Engineer: Low or Medium** | **FP**: unneeded engineer visit, costs scarce engineer time | **TN**: correctly kept off the engineer's list |

Retake is not counted in Table 1; it is reported as the retake rate. A High crack that stays in the retake loop is reported separately, as missed in the field.

### Metrics
| Metric | Formula | Why it matters | Target |
|---|---|---|---|
| Recall on High (sensitivity) | TP / (TP + FN) | Share of dangerous cracks caught | Near 1 (target, not a result) |
| Missed High (false negative rate) | FN / (TP + FN) | Main failure; stop or redesign if engineers would flag what we miss | Near 0 (target) |
| Referral rate | (TP + FP) / all assessed | Engineer workload | "Only a few", number to set with the engineering partner |
| Precision of flags | TP / (TP + FP) | How many visits were needed | Tracked |
| Retake rate | Retake / all photos | Does the photo protocol work on ordinary phones | Tracked |

## Table 2: full confusion matrix (3 x 5)
Rows: engineer on site. Columns: tool output. Each cell is a count; the label says what kind of error it is.

| Engineer \ Tool | Low | Medium | High | Expert needed | Retake |
|---|---|---|---|---|---|
| **Low** | correct | over-cautious | false alarm | referral | retake |
| **Medium** | **false all-clear** | correct | over-cautious | referral | retake |
| **High** | **missed danger (worst)** | **missed danger** | correct | referral (safe) | retake |

"False all-clear" (tool says Low, engineer says Medium or High) is counted separately: Low must be earned (AGENTS.md rule 3).

## Threshold curve
Recompute Table 1 for confidence thresholds 0.5 to 0.95 and plot missed High against referral rate (deck slide 7 shows the illustrative shape). Pick the threshold with the engineering partner, then record it in `spec/decisions.md`.
