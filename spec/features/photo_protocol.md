# Feature: photo protocol and pilot (`src/pilot/prepare.py`)

Status: version 2 (27 Oct 2026), for the three scales S, O and P of pipeline v3 (`spec/features/pipeline.md`). Version 1 used a coin; the printed scale card replaces it (decision D24). To be tested on ordinary phones, then fixed with the engineering partners in Phase 1.

## Pilot goal
About 30 cracks on public facades in Barcelona, in one week (target is an assumption).
Tests: can a non-expert follow the protocol; does the quality gate work on real phone photos; how many pixels across the crack a phone gets at each distance; can width be read from the scale card.
The pilot has **no risk labels**: we are not engineers, so we record what we measure, never a risk level.

## Ethics and privacy (AGENTS.md rule 9)
- Only public facades seen from the street. Do not enter private property; ask the owner before touching a wall.
- No people, faces, house numbers, street signs or car plates in frame. Retake rather than blur later. The building photo (S) is taken so that the address cannot be read.
- Marker stickers only with the owner's permission; in the public pilot, use removable stickers and take them off, or skip them.
- `prepare.py` removes all metadata (including GPS) and renames files before anything is labelled. Originals stay on the phone and are deleted after preparation.
- Nothing from the pilot is committed; it lives in `data/pilot/` (ignored).

## Kit
- **Printed scale card** (about A6; assumption): a 50 mm scale bar in two directions; crack-width lines of 0.1, 0.2, 0.3, 0.5, 1, 2 and 3 mm (they include the band edges 0.3, 1 and 3 mm of the risk matrix); black, grey and white patches to check exposure; fields for the building ID and the crack ID. Printed at 100 % and checked with a ruler. A 1 euro coin (23.25 mm) is the backup when no card is at hand.
- No element or material tag in the app: the models identify the material and the element (D25). In the pilot, the team writes its own guess of both in the label sheet, to test the models later.
- **Two round marker stickers** per crack (`spec/features/monitoring.md`).
- **A reference phone** for field workers (any phone for residents' follow-ups).

## Shots per building
| Scale | Shot | Distance (assumption) | Content |
|---|---|---|---|
| S | Building | 5 to 20 m | The whole facade; once per building |
| O | Element | 1 to 3 m | The whole element, the scale card visible |
| P | Crack | 10 to 30 cm, closer until the app counts at least 3 pixels across the crack | The widest part of the crack, the scale card flat on the wall next to it, the stickers in frame |

Rules for every shot:
- Save as JPEG (on iPhone: Settings > Camera > Formats > Most Compatible).
- Camera perpendicular to the wall [46].
- Scale card in the same plane as the crack; on large surfaces, a second scale reference, because the pixel size is not uniform across an image [46].
- Brush dust off the crack area first: dusty and eroded crack lips are measured less accurately [46].
- A burst of about 5 photos (assumption), with and without flash [46].
- Hold still; tap to focus on the crack.
- At least 3 pixels across the crack, 6 to 8 recommended, for a width uncertainty of about ±30 % and ±15 % respectively [46]. If the phone cannot get there, read the width band on the card by eye.

For quality-gate testing, also take **one deliberately bad shot per five cracks** (moving, too dark, or card missing) and mark it in the sheet.

## Label sheet (`data/pilot/labels.csv`)
Columns, one row per photo:
`photo_id, building_id, crack_id, scale (S/O/P), element, material, pattern_guess, width_band_card, width_mm_card, flash (on/off), card_visible (yes/no), deliberately_bad (yes/no), notes`
`pattern_guess` uses the seven patterns in `spec/features/risk_matrix.md` or `unsure`; `element` uses column, beam, slab, load_bearing_wall or infill_wall; it is our guess, to compare later with an engineer. `width_band_card` uses the matrix bands (under_0.3, 0.3_to_1, 1_to_3, over_3).
A template is in `docs/templates/pilot_labels.csv`.

## Preparation
`py src/pilot/prepare.py <folder with phone photos> data/pilot/photos`
Copies every image as P0001.jpg, P0002.jpg..., with all metadata removed, and writes `data/pilot/photo_index.csv` (new name, original file name) so the label sheet can be filled in.

## What we report after the pilot
- Share of shots the quality gate accepts, and whether it rejects the deliberately bad ones.
- Pixels across the crack at each distance, per phone.
- Width from the photo vs width read on the card, once the measurement code exists.
- What was hard to follow in the protocol; change the protocol, record the change in `spec/decisions.md`.
