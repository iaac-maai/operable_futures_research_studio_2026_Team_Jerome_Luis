# Feature: crack segmentation (`src/segmentation/`)

Status: day 1 of the first model (29 Oct): data preparation done (9,441 pairs: crack-seg 3,717 / 199 / 112, CrackSeg9k 4,365 / 439 / 609 train / val / test); training next. Box [6] of the pipeline story (figure 01d), scope D30.

## Purpose
Mark which pixels of a usable photo are crack. The mask feeds the width measurement (mm, from the scale card) and then the written risk matrix. The model never gives a level itself.

## Model (planned, day 2)
U-Net with a ResNet-34 encoder pre-trained on ImageNet (`segmentation-models-pytorch`), one output channel (crack / not crack). No Ultralytics code (AGPL-3.0, D9).
Pre-trained on public crack sets now; fine-tuned on our own engineer-labelled photos later (learn loop, box [9]).

## Data preparation (`src/segmentation/prepare.py`)
Sources (licences and checks in `docs/data_map.md`):

| Set | Used | Masks | Split |
|---|---|---|---|
| CrackSeg9k Vol1 [25] | 5,413 image + mask pairs (Vol2 not downloaded) | grey masks with soft edges (0 to 255); crack = value above 127 (assumption) | own split, grouped by source photo (below) |
| crack-seg [33] | 4,029 images | YOLO polygons filled into masks | kept as published (train 3,717, val 200, test 112) |

- Every image and mask is resized to 416 x 416 px (crack-seg's own size, a multiple of 32 as the U-Net needs). Images: bilinear. Masks: resized as grey, then thresholded, so thin cracks are not lost.
- CrackSeg9k's published train/test lists **leak**: tiles cut from the same source photo sit in both (Rissbilder: 116 of the source photos; DeepCrack: 37; GAPS384: 40). A test score on them would be too optimistic. We split by **source photo** instead: 80 / 10 / 10 % train / val / test, decided by a hash of the source-photo key, so the split is fixed and repeatable.
- crack-seg's train set holds up to 6 augmented copies of one photo (`<id>.rf.<hash>`); no id crosses splits, so its split is kept.
- Images with an empty mask stay: CrackSeg9k's 1,411 "noncrack" images teach what is not a crack. The one crack-seg image with an empty label file is dropped (likely a missing annotation, assumption).
- Output: `data/processed/segmentation/{train,val,test}/{images,masks}/` as PNG (mask 0 or 255), plus `index.csv` (file, set, split, source-photo group, crack fraction). Never committed (`data/` is ignored).

## Limits
- Mostly pavement, concrete surfaces and walls; few columns and beams; no scale in any image. Off-concept for informal buildings (D14), used only to pre-train crack pixels.
- crack-seg polygons are drawn wider than the crack (checked on a sample, 29 Oct); CrackSeg9k masks are thin. Both teach where the crack is; width in mm must not be calibrated on crack-seg masks.
- Thresholds (127, 416 px, 80/10/10) are illustrative until checked against engineer-labelled photos.

## Tests (`tests/test_segmentation_prepare.py`)
Polygon to mask, soft mask threshold, source-photo keys, split is repeatable and never splits a group.
