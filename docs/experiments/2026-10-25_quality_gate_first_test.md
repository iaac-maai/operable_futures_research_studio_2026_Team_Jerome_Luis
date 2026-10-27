# First test on real data: quality gate (25 Oct 2026)

Deliverable for 29 Oct: "agent working on real data as a first test".
Spec: `spec/features/quality_gate.md`. Code: `src/experiments/real_data_quality.py`. Figure: `figures/08_real_data_quality_gate.png`.

## What was run
The quality gate's image checks (sharpness, brightness) on six public datasets, downloaded into `data/raw/` (git-ignored). First run: every image of crack-seg and Darbhanga (8,288). Later runs added SDNET2018, METU, Strathclyde and the Haiti 2010 engineer photos: up to 2,000 random images per group (about 23,000 in the last run).

| Dataset | Images | Size | Labels | Check of the download |
|---|---|---|---|---|
| Ultralytics crack-seg [33][34] | 4,029 (3,717 train, 200 val, 112 test) | all 416 x 416 | YOLO polygons, 1 class; 1 empty label file | Counted in the zip |
| Darbhanga brick masonry [30] | 4,259 (3,407 train, 639 val, 213 test) | all 768 x 768 | YOLO bounding boxes, 1 class; test has no labels; 203 train images without labels (no crack) | SHA-256 matches the Mendeley record |
| METU concrete cracks [36] | 40,000 (20,000 crack, 20,000 no crack) | 227 x 227 tiles | crack / no crack by folder | SHA-256 matches the Mendeley record |
| Haiti 2010 Earthquake Database [41] | 4,450 photos recovered of 6,526 | full-size field photos | per building: light / moderate / severe | Partial: the 14 GB Dropbox zip broke at 85% and cannot resume; every recovered file passed its CRC-32 check |
| SDNET2018 [22] | 56,092 (deck 2,025 cracked / 11,595 uncracked; wall 3,851 / 14,287; pavement 2,608 / 21,726) | 256 x 256 tiles | crack / no crack by folder | Downloaded in a browser (scripted download blocked); every file size checked against the download |

The coin check is not implemented, so every image was treated as if the coin were confirmed; these sets have no coin.

## Ranking: share of images the gate accepts, best to worst (last run)

| # | Dataset | Accepted (cracked / uncracked) | Main rejection |
|---|---|---|---|
| 1 | Strathclyde brick facades | 100% / 100% | none |
| 2 | crack-seg (roads, walls) | 97% / - | too bright |
| 3 | **Haiti 2010 engineer photos** (full-size field photos) | 95% (light 94%, moderate 92%, severe 94%) | blurred |
| 4 | SDNET2018 pavement | 91% / 82% | blurred |
| 5 | Darbhanga brick masonry | 72% / 95% | blurred |
| 6 | METU building concrete | 37% / 3% | blurred |
| 7 | SDNET2018 bridge decks | 25% / 13% | blurred |
| 8 | SDNET2018 walls | 22% / 10% | blurred |

A low score means the gate struggles with that surface, not that the data is bad: textured brick and field photos pass, smooth plaster and concrete tiles are wrongly called blurred (D12).

## Results (last run, six datasets)

![Quality gate on real images](../../figures/08_real_data_quality_gate.png)

The figure orders the datasets by fit to our concept, best first (`docs/data_map.md`, section 0); each panel shows its fit and the share of images accepted.

### Datasets by fit to our concept, with the gate result

| # | Dataset | Fit to our concept | Accepted by the quality gate |
|---|---|---|---|
| 1 | Haiti 2010 (engineer survey) | high | 95% |
| 2 | Darbhanga (brick masonry) | medium | 76% |
| 3 | Strathclyde (brick facades) | medium | 100% |
| 4 | METU (building concrete) | low | 20% |
| 5 | SDNET2018 wall | low | 16% |
| 6 | crack-seg (roads, walls) | low | 97% |
| 7 | SDNET2018 pavement | off-concept | 87% |
| 8 | SDNET2018 bridge deck | off-concept | 19% |

"Accepted" counts cracked and uncracked images together (up to 2,000 per group, last run on 25 Oct 2026); the split is in the results table below. A low share means the gate struggles with that surface (smooth plaster and concrete, D12), not that the data is bad.

| Dataset | Label | n | Pass rate | Median sharpness | Median brightness | Main failure |
|---|---|---|---|---|---|---|
| crack-seg | crack | 2,000 | 97% | 765.9 | 159.9 | too bright |
| Darbhanga | crack | 2,000 | 73% | 219.6 | 123.9 | blurred |
| Darbhanga | no crack | 203 | 95% | 233.9 | 149.9 | blurred |
| Darbhanga | unlabelled (test) | 213 | 89% | 286.6 | 121.7 | blurred |
| Haiti 2010, building rated light | engineer: light | 167 | 94% | 792.6 | 118.8 | blurred |
| Haiti 2010, building rated moderate | engineer: moderate | 241 | 92% | 554.9 | 126.1 | blurred |
| Haiti 2010, building rated severe | engineer: severe | 633 | 94% | 633.1 | 123.8 | blurred |
| Haiti 2010, photo not linked to a building | not linked | 2,000 | 96% | 973.1 | 120.1 | blurred |
| Strathclyde brick facades | crack | 350 | 100% | 1,418.7 | 135.6 | - |
| Strathclyde brick facades | no crack | 350 | 100% | 964.6 | 151.4 | - |
| METU building concrete | crack | 2,000 | 39% | 82.0 | 165.0 | blurred |
| METU building concrete | no crack | 2,000 | 3% | 21.5 | 183.5 | blurred |
| SDNET2018 bridge deck | crack | 2,000 | 25% | 58.2 | 178.6 | blurred |
| SDNET2018 bridge deck | no crack | 2,000 | 13% | 44.3 | 177.7 | blurred |
| SDNET2018 wall | crack | 2,000 | 20% | 44.5 | 173.1 | blurred |
| SDNET2018 wall | no crack | 2,000 | 11% | 31.7 | 167.3 | blurred |
| SDNET2018 pavement | crack | 2,000 | 91% | 439.0 | 156.3 | blurred |
| SDNET2018 pavement | no crack | 2,000 | 84% | 340.2 | 156.2 | blurred |

First run on every crack-seg image (4,029): 97% pass, 118 too bright, 14 blurred. Every Darbhanga image (4,259): same pass rates as above within 1 point.

## What we learned
1. **The code runs on real images end to end**: six datasets, about 23,000 images in the last run, measured and logged, with a figure.
2. **Bug found and fixed: sharpness depended on resolution.** Before the fix the gate rejected 63% of all Darbhanga images as blurred. Scaling the same images to 416 px dropped the blurred share from 67% to 11% (sample of 107 images). A phone photo at about 4000 px would almost always have failed. The gate now measures on a copy scaled to 512 px (`spec/decisions.md` D8). This is why a test on real data was worth doing before the pilot.
3. **Cracked brick images score lower on sharpness than uncracked ones** (73% vs 95% pass). Possible reasons: close-ups of cracks, smoother surfaces, or real blur. Not tested; we need to look at the rejected images before changing anything.
4. **Second problem found: the blur measure confuses smooth surfaces with blur.** The gate rejects 75 to 89% of SDNET2018 wall and deck tiles, but only 9 to 16% of pavement. These are 256 px tiles, so it is not the resolution bug. A visual check of 8 rejected cracked-wall tiles: most are in focus, smooth low-contrast concrete with hairline cracks; a few look slightly soft. Laplacian variance measures texture as much as focus. On real walls this means **hairline cracks on smooth plaster or concrete would be sent back for retake again and again**. That is safe (a retake is never a Category 1) but makes the tool unusable for exactly the walls we care about. **Confirmed on building walls:** on METU (concrete surfaces of campus buildings, the closest of these sets to our concept, D14) the gate rejects 61% of cracked and 97% of uncracked tiles. Textured brick passes (Strathclyde brick facades: 100%), so the problem is specific to smooth surfaces: plaster and concrete. Not fixed yet: we need photos with known blur to choose a better measure (`spec/decisions.md` D12).
5. **Real field photos pass.** The Haiti photos are full-size camera photos of damaged buildings taken by engineers; 95% pass. Each photo in a building folder carries that building's engineer rating (1,041 photos; the other photos are camera dumps sorted by photographer and date, whose photo log was lost in the broken download). The gate accepts photos of lightly, moderately and severely damaged buildings at the same rate (92 to 94%), so it does not filter out the serious cases. One photo in the original archive is all zeros; the gate records it as "unreadable file" (a retake) instead of crashing. This is the first test on photos like the ones the tool will receive, and it shows the 512 px working size (D8) works on them. They are not phone photos and have no coin, so the thresholds are still not calibrated.
6. **"Too bright" is the main failure on crack-seg** (118 of 4,029). Many images are pale concrete or pavement; the 220 limit may be too strict for light walls. To check on the pilot phone photos.

## Update 27 Oct 2026: PHI-Net added
Rerun on all seven datasets on disk, now with PHI-Net tasks 8 (damage type), 3 (spalling) and 6 (components), the three we plan to train on (`docs/data_map.md`, section 6). Up to 2,000 images per group, 33,971 images in all. Figure 8 now has 11 panels, ordered by fit. The other datasets' rates match the 25 Oct run within 1 point.

| Group | Label | n | Pass rate | Median sharpness | Median brightness |
|---|---|---|---|---|---|
| PHI-Net t8 damage type | damaged | 2,000 | 85% | 463.9 | 127.3 |
| PHI-Net t8 damage type | undamaged | 1,813 | 71% | 324.2 | 119.8 |
| PHI-Net t3 spalling | spalling | 2,000 | 66% | 238.6 | 131.1 |
| PHI-Net t3 spalling | no spalling | 2,000 | 57% | 193.4 | 135.0 |
| PHI-Net t6 components | (no damage label) | 2,000 | 79% | 386.8 | 124.0 |

7. **About a quarter of PHI-Net images fall under the blur limit**, mostly the undamaged and non-spalling ones. PHI-Net images are 224 px crops, measured as they are (the gate never scales up). Why they fail is not checked: real softness, upscaled small photos and smooth undamaged surfaces (D12) are all possible. Before training, look at the rejected images; the gate result can be a filter for the training set.

## Limits
- None of these are phone photos with a coin, so the thresholds are not calibrated by this test (`spec/decisions.md` D7).
- No ground truth for "usable": we only know what the gate decided, not whether a person would retake the photo. The pilot adds deliberately bad shots for that.
- Sharpness thresholds stay illustrative.

## Next
- Look at a sample of rejected Darbhanga and "too bright" crack-seg images.
- Rerun with the pilot phone photos and their deliberately bad shots.
- On the pilot photos, compare the current measure with ones less tied to texture (for example sharpness of the strongest edges only), using the deliberately blurred shots as ground truth.
- Rerun on everything: `py src/experiments/real_data_quality.py data/raw/haiti2010 data/raw/phinet data/raw/darbhanga data/raw/strathclyde-brickwork data/raw/metu data/raw/sdnet2018 data/raw/crack-seg --per-group 2000` (plain `py`, not `py -I`: matplotlib needs the user packages).
