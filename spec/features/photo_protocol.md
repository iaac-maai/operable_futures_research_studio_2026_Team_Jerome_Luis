# Feature: photo protocol and pilot (`src/pilot/prepare.py`)

Status: version 1 for the Barcelona pilot. To be tested on ordinary phones, then fixed with the engineering partner in Phase 1.

## Pilot goal
About 30 cracks on public facades in Barcelona, 3 shots each, in one week (target is an assumption).
Tests: can a non-expert follow the protocol; does the quality gate work on real phone photos; can width be measured from the coin.
The pilot has **no risk labels**: we are not engineers, so we record what we measure, never a risk level.

## Ethics and privacy (AGENTS.md rule 9)
- Only public facades seen from the street. Do not enter private property; ask the owner if you need to touch a wall.
- No people, faces, house numbers, street signs or car plates in frame. Retake rather than blur later.
- `prepare.py` removes all metadata (including GPS) and renames files before anything is labelled. Originals stay on the phone and are deleted after preparation.
- Nothing from the pilot is committed; it lives in `data/pilot/` (ignored).

## Kit
- A 1 euro coin (23.25 mm diameter) as scale reference.
- An element tag: a card with the crack ID (P01, P02...), element (column, beam, slab, brick wall, other) and material.
- A crack-width card (printed comparator with lines of 0.1 to 3 mm), to read the width by eye. This is our measurement ground truth, not an engineer's rating.

## Shots per crack
| Shot | Distance (assumption) | Content |
|---|---|---|
| A, context | 2 to 3 m | The whole element, the tag visible |
| B, mid | about 1 m | The whole crack, coin and tag visible |
| C, close | 20 to 30 cm | The widest part of the crack, coin flat on the wall next to it |

Rules for every shot: save as JPEG (on iPhone: Settings > Camera > Formats > Most Compatible); phone parallel to the wall; daylight, no flash; coin in the same plane as the crack; hold still, tap to focus on the crack.
For quality-gate testing, also take **one deliberately bad shot per five cracks** (moving, too dark, or coin missing) and mark it in the sheet.

## Label sheet (`data/pilot/labels.csv`)
Columns, one row per shot:
`photo_id, crack_id, shot (A/B/C), element, material, pattern_guess, width_mm_card, length_cm_estimate, coin_visible (yes/no), deliberately_bad (yes/no), notes`
`pattern_guess` uses the seven patterns in `spec/features/risk_matrix.md` or `unsure`; `element` uses column, beam, slab, load_bearing_wall or infill_wall; it is our guess, to compare later with an engineer.
A template is in `docs/templates/pilot_labels.csv`.

## Preparation
`py src/pilot/prepare.py <folder with phone photos> data/pilot/photos`
Copies every image as P0001.jpg, P0002.jpg..., with all metadata removed, and writes `data/pilot/photo_index.csv` (new name, original file name) so the label sheet can be filled in.

## What we report after the pilot
- Share of shots the quality gate accepts, and whether it rejects the deliberately bad ones.
- Coin found by eye in how many close shots.
- Width from the coin vs width from the card, once the measurement code exists.
- What was hard to follow in the protocol; change the protocol, record the change in `spec/decisions.md`.
