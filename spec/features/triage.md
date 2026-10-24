# Feature: triage rules (`src/triage/matrix.py`)

Status: implemented. Thresholds are illustrative until calibrated with a structural engineer.

## Inputs
- `pattern`: one of the five patterns below, from the pattern model.
- `width_mm`: crack width in millimetres, from the measurement step (coin scale).
- `confidence`: pattern-model confidence, 0 to 1.
- `image_ok`: result of the quality gate (blur, light, coin visible).

## Outputs
| Level | Meaning (deck, slide 6) | Engineer review |
|---|---|---|
| Retake | Photo unusable; take it again following the protocol | No |
| Expert needed | The system is unsure; a human decides | Yes |
| Low | Routine monitoring | No |
| Medium | Low-cost advice, recheck | No |
| High | Engineer must confirm | Yes |

Every result carries a one-sentence reason, e.g. "diagonal / stair-step crack, 1.5 mm wide (1 to 3 mm band): High."
The tool never outputs "safe", a clearance or a permit.

## Decision order
1. `image_ok` is false -> Retake.
2. Any doubt -> Expert needed:
   - unknown pattern;
   - confidence missing, not a number, outside 0 to 1, or below the threshold (0.8, illustrative);
   - width missing, not a number, negative or infinite (measurement failed).
3. Otherwise read the matrix: width band x pattern.

The confidence threshold is a module constant, not a function argument, so it can only change in a reviewed commit.

## Patterns (provisional, see `spec/decisions.md` D1)
`plaster_crazing`, `wall_vertical`, `diagonal_step` (diagonal and stair-step in brick), `column_or_beam`, `spalling_rust`.

## Width bands (illustrative)
Lower bound inclusive, upper bound exclusive. A crack exactly on a boundary goes to the wider band (safer).
`under_0.3`: [0, 0.3) · `0.3_to_1`: [0.3, 1) · `1_to_3`: [1, 3) · `over_3`: [3, inf).

## Risk matrix (illustrative, deck slide 7)
| Width | plaster_crazing | wall_vertical | diagonal_step | column_or_beam | spalling_rust |
|---|---|---|---|---|---|
| under 0.3 mm | Low | Low | Medium | Medium | Medium |
| 0.3 to 1 mm | Low | Medium | Medium | High | High |
| 1 to 3 mm | Medium | Medium | High | High | High |
| over 3 mm | Medium | High | High | High | High |

## Tests (`tests/test_matrix.py`)
- Bad photo -> Retake; low, NaN or out-of-range confidence -> Expert needed (never Low).
- Bad width (NaN, negative, infinite) -> Expert needed.
- Low only when image usable, confidence over threshold and matrix says Low (exhaustive check).
- Every High and every Expert needed sets `engineer_review`.
- Band boundaries go to the wider band.

## Not yet covered
Comparison against the non-AI baseline (an engineer's visual check): needs engineer-labelled photos (see `docs/data_map.md`).
