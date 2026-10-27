# Reference thesis: Corres Sojo (2024), EPFL

**Corres Sojo E.**, *Contributions to rebar-to-concrete interaction and its structural implications for design and monitoring applications*, PhD thesis n° 10772, EPFL, Structural Concrete Laboratory (IBETON), supervised by Prof. A. Muttoni, 2024. doi:10.5075/epfl-thesis-10772 [46].
Read on 26 Oct 2026: abstract, chapter 1, chapter 2 set-up, chapters 4, 5 and 6 in full, and the cited references below. Read on 27 Oct 2026 (full text from the EPFL repository): chapter 2 results (2.3 to 2.5), chapter 3 (3.1, 3.2) and chapter 4 again (4.1, 4.2, 4.4, 4.5), for features of the risk matrix (section D). Sent by the studio professor as the main reference for the state of the art and the methodology.

## What the thesis is about
How reinforcing bars and concrete hold together (bond), how that governs cracking in reinforced concrete, and how cracks in existing structures can be measured from images. Chapters 2 to 5 are journal articles (Structural Concrete 2023; others submitted).

## Findings that matter for Second Look

### A. Cracks and safety (chapters 1, 4, 5)
1. **A crack is not automatically a safety problem, and a small crack is not automatically safe.** "Cracks do not necessarily indicate an insufficient level of safety if they are expected and coherent with the structural behaviour"; "small crack openings might not be an indicator of sufficient resistance in cases governed by fragile failure modes" (ch. 4.1, citing Zaborac et al. 2019 and Monney et al. 2022).
   → Supports our design: the level depends on the **pattern** (what the crack means), not on width alone; brittle patterns such as diagonal shear cracks start at Category 2 even below 0.3 mm (`spec/features/risk_matrix.md`).
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
   → Updates our photo protocol (scale reference, distance, flash); done in photo protocol v2 (D24).
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

### D. Cracks along the bars, cover and confinement (chapters 2, 3, 4; read 27 Oct)
14. **Cracks along a bar weaken its grip.** "Longitudinal cracking along the bar has been shown to significantly reduce the bond stresses" (ch. 2.1); in the beam tests, regions with longitudinal cracks along the stirrups had lower bond stresses (ch. 4.4). The reduction grows with the width of the crack along the bar relative to the bar diameter (factor of Brantschen et al. 2016, Eq. 4.9, ch. 4.5).
   → Supports our `along_bar` pattern as a serious pattern; suggests that its width matters relative to the bar diameter, which a photo only shows when the bar is exposed.
15. **Confinement decides brittle or ductile.** With thin cover and no transverse reinforcement (stirrups), splitting cracks run through the cover and cause a brittle failure; with larger cover or some stirrups the brittle failure is prevented; well confined (heavy stirrups or cover of at least 5 bar diameters) gives a ductile pull-out (ch. 3.2, citing fib 2000 and Model Code 2010). In the pull-out tests, specimens with a cover of 1 bar diameter "present a relatively brittle failure with a sudden drop in the force" (ch. 2.3.3).
   → A possible new dimension: **thin cover or missing stirrups**, visible only where concrete has spalled and the bar is exposed (the scale card gives the cover depth in mm).
16. **Anchorage zones.** Splitting cracks appeared first at the loaded end of the bar and spread from there (ch. 2.3); the thesis names "anchorages affected by longitudinal cracks due to corrosion" as a case for assessing existing structures (ch. 2.1, 2.4).
   → A possible new dimension: **where on the element** the crack is. Cracks along bars at the ends of beams and columns, where bars are anchored or lapped, are more critical than mid-span (to confirm with the engineer; the thesis studies anchorages, not building elements).
17. **Crack spacing can be measured in existing structures** and is the main uncertainty when linking crack width to the stress in the bar (ch. 4.1, Figure 4.2). Secondary and splitting cracks "can be measured or visually verified".
   → Record the **number and spacing of parallel cracks** on an element as a measured feature for the engineer; the thesis gives no rule linking spacing to risk, so it does not enter the matrix.
18. **Crack limits in codes depend on exposure.** Eurocode 2 and Model Code 2010 limit crack widths "based on the environmental exposure", for durability and water tightness (ch. 4.1); the thesis gives no numbers. Chapter 6.2 lists corrosion traces, water, sediment marks and moss as signs not yet evaluated.
   → A possible **damp or wet exposure** warning sign, only after reading the exposure classes in Eurocode 2 itself.
19. **What the thesis does not give:** no crack-width thresholds for safety (0.3 mm, 1 mm or similar do not appear), and bar-stress estimates need bar diameter, cover, crack spacing and bond conditions that a phone photo cannot give (ch. 4). Our band edges must come from the guides it cites [50][51][52] and from the engineers.

## What we can take from it (proposed, not yet implemented)
| # | Feature | Where | Based on |
|---|---|---|---|
| 1 | Width uncertainty = ±1 pixel (opening) from the measured pixel size; below 3 pixels across the crack, the width is not trusted: Retake closer, or Expert needed | Measurement, quality gate, matrix input `width_uncertainty_mm` | Finding 7 |
| 2 | Photo protocol: camera perpendicular, close shot giving 6 to 8 pixels across the crack, the scale card near the crack (and a second reference on large surfaces), photos with and without flash, clean the surface first | `spec/features/photo_protocol.md` | Findings 8, 9 |
| 3 | Measure opening and sliding, not only width; sliding counts as a measured "offset" | Measurement, matrix escalator `offset` | Findings 3, 5 |
| 4 | Start the segmenter from the open-source EPFL tools and the Özgenel segmentation dataset (concrete of buildings) | Models, data map | Finding 5 |
| 5 | "Growing" only when growth exceeds the measurement uncertainty; repeat photos in similar light and time of day; burst of photos averaged | Matrix escalator `growing`, follow-up flow | Findings 12, 13 |
| 6 | Check the matrix against inspection guides (OFROU 2021, DGC 2012) and Zaborac et al. 2019 before the engineer session | Calibration plan | Finding 2 |
| 7 | Report honestly that a phone photo cannot estimate bar stress | Limits, pitch | Finding 4 |
| 8 | Matrix dimension "location on the element": end zone (anchorage, lap, joint) vs middle; along-bar and diagonal cracks in end zones +1 (illustrative) | Risk matrix v3 (proposal) | Findings 14, 16 |
| 9 | Warning sign "thin cover or no stirrups", seen where the bar is exposed: cover under about 1 bar diameter, measured on the scale card, +1 (illustrative) | Risk matrix v3 (proposal) | Finding 15 |
| 10 | Warning sign "crack along a bar or stirrup meets another crack" (transverse + longitudinal), +1 (illustrative) | Risk matrix v3 (proposal) | Findings 14, 17 |
| 11 | Record crack count and spacing per element in the engineer's dossier (not a rule) | Building case, dossier | Finding 17 |
| 12 | Damp or wet exposure as a warning sign, after reading Eurocode 2 exposure classes | Risk matrix (later) | Finding 18 |

## Open questions for the expert (Enrique Corres Sojo)
- Which crack patterns in reinforced concrete homes would you treat as brittle (Category 3 even when narrow)?
- Is ±1 pixel (±30 %) at 3 pixels per crack acceptable for triage, or should we require 6 to 8 pixels?
- What would you accept as evidence that a crack is growing, from two phone photos months apart?
- Would you rate our 30 to 40 calibration cards (element x pattern x width x warning signs)?
- In self-built concrete homes, is thin cover with few stirrups common enough that an exposed bar should always raise the level?
- Are cracks along bars at the ends of beams and columns (anchorage and lap zones) more critical than mid-span ones, and by how much?
