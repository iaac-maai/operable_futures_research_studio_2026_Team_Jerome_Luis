# Reference thesis: Corres Sojo (2024), EPFL

**Corres Sojo E.**, *Contributions to rebar-to-concrete interaction and its structural implications for design and monitoring applications*, PhD thesis n° 10772, EPFL, Structural Concrete Laboratory (IBETON), supervised by Prof. A. Muttoni, 2024. doi:10.5075/epfl-thesis-10772 [46].
Read on 26 Oct 2026: abstract, chapter 1, chapter 2 set-up, chapters 4, 5 and 6 in full, and the cited references below. Sent by the studio professor as the main reference for the state of the art and the methodology.

## What the thesis is about
How reinforcing bars and concrete hold together (bond), how that governs cracking in reinforced concrete, and how cracks in existing structures can be measured from images. Chapters 2 to 5 are journal articles (Structural Concrete 2023; others submitted).

## Findings that matter for Second Look

### A. Cracks and safety (chapters 1, 4, 5)
1. **A crack is not automatically a safety problem, and a small crack is not automatically safe.** "Cracks do not necessarily indicate an insufficient level of safety if they are expected and coherent with the structural behaviour"; "small crack openings might not be an indicator of sufficient resistance in cases governed by fragile failure modes" (ch. 4.1, citing Zaborac et al. 2019 and Monney et al. 2022).
   → Supports our design: the level depends on the **pattern** (what the crack means), not on width alone; brittle patterns such as diagonal shear cracks start at Medium even below 0.3 mm (`spec/features/risk_matrix.md`).
2. Cracks are one of the indicators used in visual inspections for structural assessment, with national inspection guides (Switzerland OFROU 2021, Spain DGC 2012) and a US report on evaluating structural cracking in concrete (Zaborac et al. 2019, FHWA/TX-19/0-6919-1) [50][51][52].
   → These are the **literature anchors** to check first for calibrating the matrix.
3. Crack **kinematics** have two components: **opening** (perpendicular to the crack) and **sliding** (along it). Kinematics help estimate which shear-transfer mechanisms are active (ch. 5.1).
   → Measuring sliding, not only width, gives a measured basis for our "offset" warning sign.
4. The stress in a bar can be estimated from the crack width, but only with the crack spacing, cover, bar diameter and bond conditions (ch. 4).
   → **Not feasible from one phone photo**; out of scope. Possible later research direction.

### B. Measuring cracks from photos (chapter 5.2): direct input for our measurement stage
5. Pipeline used by the authors: (1) segment the crack into a binary image with an open-source deep network (Rezaie et al. 2020 [47]), trained either on DIC-speckle images or on the **Özgenel concrete crack segmentation dataset** [49]; (2) compute opening and sliding from the binary image with an open-source algorithm (Pantoja-Rosero et al. 2022 [48], EPFL EESD). Analysis in 256 x 256 pixel windows.
6. **Validated with a smartphone** (OnePlus 6, 16 MP) as well as a professional camera (Nikon D800), from 0.1 to 2.5 m: results are comparable for the same pixel size.
7. **Accuracy rule:** with **at least 3 pixels across the crack**, the error is about **±1 pixel for the opening (±30 %)** and ±2 pixels for the sliding. **6 to 8 pixels across the crack are recommended for about ±15 %.** Below 3 pixels, errors grow quickly (low contrast, too few features on the crack lips).
   → A measured rule for our quality gate and for the width uncertainty in the matrix.
8. Recommendations for photos: camera **perpendicular** to the surface; for large surfaces, **several scale references** because pixel size is not uniform across the image; take images **with and without flash** depending on surface roughness.
   → Updates our photo protocol (coin, distance, flash).
9. **On a real bridge** (Chillon Viaducts, crack about 50 years old), photo-based widths matched crack-microscope and crack-ruler measurements within ±1 pixel at most points, with one larger error (0.73 mm measured by hand, 1.18 mm by the algorithm). Reason: **dust and eroded crack lips** make old cracks less sharp than in the lab.
   → Expect lower accuracy on old cracks in informal housing; clean the surface before the photo; keep the width uncertainty honest.
10. The authors list open issues for real conditions: **corrosion traces, water, sediment marks and moss** around cracks were not evaluated (ch. 6.2).
   → Matches our warning signs (rust staining) and our field reality; a test we can run on our own photos.

### C. Following a crack over time (chapter 5.3, 5.4)
11. To detect real change between inspections, the authors fix **circular markers on both sides of the crack** and compare their positions; the camera can be removed between visits.
12. **Temperature opens and closes cracks**: over 19 hours on the bridge the crack moved by a few micrometres with daily temperature; a correction of about 2.5 μm was needed. Long-term monitoring needs measurements over more than a year to separate seasonal movement from permanent change.
   → Our "growing" warning sign must only count growth **larger than the measurement uncertainty**, and repeat photos should be taken in similar conditions. Phone photos cannot see micrometre movements; only clear growth (several pixels) is meaningful.
13. Averaging about 10 images reduces both random noise and bias.
   → Taking a short burst of photos and averaging the measurement is a cheap accuracy gain.

## What we can take from it (proposed, not yet implemented)
| # | Feature | Where | Based on |
|---|---|---|---|
| 1 | Width uncertainty = ±1 pixel (opening) from the measured pixel size; below 3 pixels across the crack, the width is not trusted: Retake closer, or Expert needed | Measurement, quality gate, matrix input `width_uncertainty_mm` | Finding 7 |
| 2 | Photo protocol: camera perpendicular, close shot giving 6 to 8 pixels across the crack, a coin near the crack (and a second one on large surfaces), photos with and without flash, clean the surface first | `spec/features/photo_protocol.md` | Findings 8, 9 |
| 3 | Measure opening and sliding, not only width; sliding counts as a measured "offset" | Measurement, matrix escalator `offset` | Findings 3, 5 |
| 4 | Start the segmenter from the open-source EPFL tools and the Özgenel segmentation dataset (concrete of buildings) | Models, data map | Finding 5 |
| 5 | "Growing" only when growth exceeds the measurement uncertainty; repeat photos in similar light and time of day; burst of photos averaged | Matrix escalator `growing`, follow-up flow | Findings 12, 13 |
| 6 | Check the matrix against inspection guides (OFROU 2021, DGC 2012) and Zaborac et al. 2019 before the engineer session | Calibration plan | Finding 2 |
| 7 | Report honestly that a phone photo cannot estimate bar stress | Limits, pitch | Finding 4 |

## Open questions for the expert (Enrique Corres Sojo)
- Which crack patterns in reinforced concrete homes would you treat as brittle (High even when narrow)?
- Is ±1 pixel (±30 %) at 3 pixels per crack acceptable for triage, or should we require 6 to 8 pixels?
- What would you accept as evidence that a crack is growing, from two phone photos months apart?
- Would you rate our 30 to 40 calibration cards (element x pattern x width x warning signs)?
