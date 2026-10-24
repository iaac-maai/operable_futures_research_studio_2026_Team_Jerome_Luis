# First test on real data: quality gate (25 Oct 2026)

Deliverable for 29 Oct: "agent working on real data as a first test".
Spec: `spec/features/quality_gate.md`. Code: `src/experiments/real_data_quality.py`. Figure: `figures/08_real_data_quality_gate.png`.

## What was run
The quality gate's image checks (sharpness, brightness) on **every image** of two public datasets, downloaded into `data/raw/` (git-ignored):

| Dataset | Images | Size | Labels | Check of the download |
|---|---|---|---|---|
| Ultralytics crack-seg [33][34] | 4,029 (3,717 train, 200 val, 112 test) | all 416 x 416 | YOLO polygons, 1 class; 1 empty label file | Counted in the zip |
| Darbhanga brick masonry [30] | 4,259 (3,407 train, 639 val, 213 test) | all 768 x 768 | YOLO bounding boxes, 1 class; test has no labels; 203 train images without labels (no crack) | SHA-256 matches the Mendeley record |

The coin check is not implemented, so every image was treated as if the coin were confirmed; these sets have no coin.
SDNET2018 could not be downloaded by script (HTTP 403) and is not in this run.

## Results

![Quality gate on real images](../../figures/08_real_data_quality_gate.png)

| Dataset | Label | n | Pass rate | Median sharpness | Median brightness | Main failure |
|---|---|---|---|---|---|---|
| crack-seg | crack | 4,028 | 97% | 763.5 | 160.8 | too bright (118), blurred (14) |
| crack-seg | no crack (empty label) | 1 | 100% | 4,591.0 | 181.3 | - |
| Darbhanga | crack | 3,843 | 73% | 217.9 | 123.9 | blurred |
| Darbhanga | no crack | 203 | 95% | 233.9 | 149.9 | blurred |
| Darbhanga | unlabelled (test) | 213 | 89% | 286.6 | 121.7 | blurred |

## What we learned
1. **The code runs on real images end to end**: 8,288 images read, measured and logged, with a figure.
2. **Bug found and fixed: sharpness depended on resolution.** Before the fix the gate rejected 63% of all Darbhanga images as blurred. Scaling the same images to 416 px dropped the blurred share from 67% to 11% (sample of 107 images). A phone photo at about 4000 px would almost always have failed. The gate now measures on a copy scaled to 512 px (`spec/decisions.md` D8). This is why a test on real data was worth doing before the pilot.
3. **Cracked brick images score lower on sharpness than uncracked ones** (73% vs 95% pass). Possible reasons: close-ups of cracks, smoother surfaces, or real blur. Not tested; we need to look at the rejected images before changing anything.
4. **"Too bright" is the main failure on crack-seg** (118 of 4,029). Many images are pale concrete or pavement; the 220 limit may be too strict for light walls. To check on the pilot phone photos.

## Limits
- None of these are phone photos with a coin, so the thresholds are not calibrated by this test (`spec/decisions.md` D7).
- No ground truth for "usable": we only know what the gate decided, not whether a person would retake the photo. The pilot adds deliberately bad shots for that.
- Sharpness thresholds stay illustrative.

## Next
- Look at a sample of rejected Darbhanga and "too bright" crack-seg images.
- Rerun with the pilot phone photos and their deliberately bad shots.
- Add SDNET2018 when it is downloaded in a browser: `py src/experiments/real_data_quality.py data/raw/crack-seg data/raw/darbhanga data/raw/sdnet2018`.
