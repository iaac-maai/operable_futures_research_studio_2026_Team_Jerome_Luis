# Feature: triage rules (`src/triage/matrix.py`)

Status: implemented with risk matrix v3.0-illustrative (`spec/features/risk_matrix.md`). All thresholds are illustrative until calibrated with the engineering partners.

## Inputs
- `pattern`: one of the seven reinforced-concrete patterns in `spec/features/risk_matrix.md`, from the pattern model.
- `element`: column, beam, slab, load-bearing wall or infill wall, from the element model; never asked to the resident (D25).
- `width_mm` and `width_uncertainty_mm`: crack width and its uncertainty in millimetres, from the measurement step (printed scale card; D24).
- `confidence`: pattern-model confidence, 0 to 1.
- `image_ok`: result of the quality gate (blur, light, scale card visible).
- `material` and `material_confidence`: result of the material check (decision D17).
- `escalators`: warning signs (growing, rust staining, sticking openings, recent earthquake, added floors, thin cover or no stirrups, a crack meeting a crack along a bar, damp, offset, sagging).
- `location`: where on the element the crack is: end zone, middle or unknown (unknown counts as an end zone; matrix v3, D28).

## Outputs
| Level | Meaning (deck, slide 6) | Engineer review |
|---|---|---|
| Retake | Photo unusable; take it again following the protocol | No |
| Expert needed | The system is unsure; a human decides | Yes |
| Low | Routine monitoring | No |
| Medium | Low-cost advice, recheck | No |
| High | Engineer must confirm | Yes |

Every result carries a one-sentence reason and a next step with a recheck interval, e.g. "diagonal shear crack in a beam, 1.5 mm wide, 1 to 3 mm band: High; raised because rust staining along the crack." / "An engineer must confirm; the case is sent now."
The tool never outputs "safe", a clearance or a permit.

## Decision order
1. `image_ok` is false -> Retake.
2. Any doubt -> Expert needed:
   - material confidence missing, invalid or below 0.8 (illustrative) -> "Material unclear";
   - material not reinforced concrete -> "Material not supported" (decision D17);
   - unknown element or pattern, or a pattern that does not fit the element;
   - confidence missing, not a number, outside 0 to 1, or below the threshold (0.8, illustrative);
   - width or its uncertainty missing, not a number, negative or infinite (measurement failed).
3. Base level from pattern x width band, using the upper end of the measured width.
4. Element criticality, the location on the element (end zone: cracks along bars and diagonal shear cracks +1) and warning signs raise the level (never lower it); capped at High.

The confidence thresholds are module constants, not function arguments, so they can only change in a reviewed commit. The matrix values live in `src/triage/risk_matrix_v3.json`.

## Tests (`tests/test_matrix.py`)
- Bad photo -> Retake; low, NaN or out-of-range confidence -> Expert needed (never Low).
- Bad width or uncertainty -> Expert needed; the upper end of the width is used.
- Unknown element or pattern, or a pattern on the wrong element -> Expert needed.
- Columns raise one level; every warning sign raises and never lowers; offset and sagging go straight to High; unknown warning signs are an error.
- Low only when image usable, confidence over threshold, not a column, no warning sign and the matrix says Low (exhaustive check).
- Every High and every Expert needed sets `engineer_review`; every result has a reason and a next step.
- Band boundaries go to the wider band.

## Not yet covered
Comparison against the non-AI baseline (an engineer's visual check): needs engineer-labelled photos (see `docs/data_map.md`).
