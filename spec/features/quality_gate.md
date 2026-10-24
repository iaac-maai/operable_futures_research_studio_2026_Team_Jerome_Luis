# Feature: quality gate (`src/quality/gate.py`)

Status: first version, written rules (not learned). Thresholds are illustrative until tuned on our own phone photos.

## Purpose
Decide whether a photo is usable before any model sees it. Unusable means Retake (`spec/features/triage.md`).

## Checks
| Check | Measure | Fails when (illustrative) |
|---|---|---|
| Sharpness | Variance of the 4-neighbour Laplacian of the grey image (0 to 255 scale) | below 100 |
| Too dark | Mean grey level | below 40 |
| Too bright | Mean grey level | above 220 |
| Coin visible | Not implemented yet (needs a coin detector) | `coin_visible` is not `True` |

`image_ok` is true only when every check passes. A missing coin result counts as a fail: any doubt means retake.
The result lists every failed check, so the app can tell the user what to fix.

## First test on real data (29 Oct)
Run the sharpness and brightness checks on a stratified sample of SDNET2018 (`src/experiments/sdnet_quality.py`).
Report the distributions and pass rates per surface and crack / no-crack.
Limits: SDNET2018 tiles are 256 x 256 crops from a camera, not phone photos, and have no coin, so this tests the code on real images; it does not calibrate thresholds.
