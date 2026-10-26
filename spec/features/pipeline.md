# Feature: full pipeline, version 2 (26 Oct 2026)

Status: specified; stages 2 and 8 exist in code, the rest are planned. Answers the professor's feedback of 26 Oct (`spec/decisions.md` D17 to D19).

## Scope
Cracks in **reinforced concrete elements** (walls, columns, beams, slabs) of buildings in informal and ageing neighbourhoods. Other materials (brick, block, stone, wood) are not assessed: they go to an engineer.

## Two users
- **Resident or field worker:** takes the photo, receives a level, a reason and what to do next.
- **Structural engineer:** reviews every High and every referral on a review screen, confirms or corrects, and so produces the labels that improve the models.

## Stages
| # | Stage | Kind | Output (each with its confidence) | If unsure or failed |
|---|---|---|---|---|
| 1 | Capture | Human | Photo with coin and element tag (`spec/features/photo_protocol.md`) | - |
| 2 | Quality check | Written rule | Usable or not, and why (blur, light, coin) | Retake |
| 3 | **Material check** | Learned model | Concrete / not concrete / unsure, confidence 0 to 1 | Not concrete or unsure: Expert needed, "material not supported" |
| 4 | Find the crack | Learned models | Crack pixels (U-Net) and element box (detector), confidence | No crack found with confidence: Expert needed |
| 5 | Measure | Written code | Width in mm with an uncertainty range (from the coin), length, orientation | Width not measurable: Expert needed |
| 6 | Pattern | Learned model | Pattern and its probability | Below threshold: Expert needed |
| 7 | Triage rules | Written rule | Level from the risk matrix, the matrix cell, a one-sentence reason, overall confidence, engineer-review flag | - |
| 8 | Engineer review | Human | Confirmed or corrected: level, pattern, material, width | - |
| 9 | Corrections logged | Data | Each correction stored as a labelled example, with consent (AGENTS.md rule 9) | - |
| 10 | Retraining | Learned models | New model version, checked on held-out engineer-rated photos before use (`spec/features/evaluation.md`) | Worse on missed Highs: not deployed |

## What a result contains (resident view and engineer view)
Material and confidence; crack found and confidence; width in mm with uncertainty, length, orientation; pattern and probability; matrix cell; level (Low, Medium, High, Expert needed, Retake); one-sentence reason; whether an engineer must review.
The resident sees the level, the reason and the next step; the engineer sees everything.

## Human-in-the-loop learning
Engineer corrections become training labels for the learned models (stages 3, 4 and 6), and the models are retrained in batches. This is supervised retraining with expert feedback (human-in-the-loop, active learning); it is not reinforcement learning in the strict sense.
The risk matrix and thresholds (stage 7) never change automatically: an engineer's correction can only change them through a reviewed decision in `spec/decisions.md` (AGENTS.md rule 5).

## Thresholds
All confidence thresholds are illustrative until calibrated on engineer-rated photos.
