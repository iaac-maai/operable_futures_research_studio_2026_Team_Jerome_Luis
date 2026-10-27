# Feature: risk matrix v3 (`src/triage/risk_matrix_v3.json`, `src/triage/matrix.py`)

Status: implemented as **v3.0-illustrative** (27 Oct 2026). Every level, band, raise and interval below is illustrative until calibrated with the engineering partners (sections "What we need from the engineer" and "Calibration plan"). Replaces v2 (`spec/decisions.md` D28; v2 stays in `risk_matrix_v2.json` for the record).

## Why v3
v2 had the pattern, the width, the element and seven warning signs. Chapters 2 to 4 of the reference thesis [46] (notes: `docs/literature/corres_sojo_2024.md`, section D) add three things a photo of the element can show and that change how serious a crack is:
- **where on the element** the crack is (bars are anchored and lapped at the ends of elements, and splitting starts there);
- **thin cover or missing stirrups** where the bar is exposed (little confinement gives brittle failure);
- **a crack meeting a crack along a bar or stirrup** (cracks along bars weaken the bar's grip).
v3 also adds **damp** as an assumption to check, and records the **basis** of every value in the JSON so an engineer can see where each one comes from.

## Inputs
| Input | From | Values |
|---|---|---|
| Element | element model (scale O), confirmed by a field worker or engineer when unsure | column, beam, slab, load-bearing wall, infill wall |
| **Location on the element (new)** | element photo (scale O), field worker; never asked to the resident (D25) | end zone, middle, unknown |
| Pattern | pattern model, or the field worker from drawings | the seven patterns below |
| Width (mm) and its uncertainty (mm) | measurement | the matrix uses the **upper end** = width + uncertainty |
| Pattern confidence | pattern model | 0 to 1, threshold 0.8 (illustrative) |
| Material and its confidence | material model | concrete only (D17) |
| Warning signs | field worker, resident answers, a second photo, building data | list below |

## Patterns (reinforced concrete)
| Key | Name | What it can mean | Allowed elements |
|---|---|---|---|
| `surface_map` | surface map cracking | shrinkage of the finish or cover, not structural | all |
| `flexural` | flexural (bending) crack | bending of the element | all |
| `diagonal_shear` | diagonal shear crack | shear; brittle failure possible | all |
| `along_bar` | crack along a bar | splitting along the bar, often from corrosion; weakens the bar's grip [46] | all |
| `column_horizontal` | horizontal crack in a column | bending or axial overload of the column | column only |
| `spalling_exposed_bar` | spalling with exposed or rusted bar | loss of cover, advanced corrosion | all |
| `joint` | crack at a beam-column joint | joint damage | column, beam |

A pattern on an element where it is not allowed goes to Expert needed.

## Width bands (illustrative)
Lower bound inclusive: `under_0.3` [0, 0.3), `0.3_to_1` [0.3, 1), `1_to_3` [1, 3), `over_3` [3, inf), on the upper end of the measured width. The thesis gives no width threshold for safety [46]; these edges wait for the guides it cites [50][51][52] and the engineers.

## Base levels: pattern x width band (illustrative, unchanged from v2)
| Pattern | under 0.3 mm | 0.3 to 1 mm | 1 to 3 mm | over 3 mm |
|---|---|---|---|---|
| surface map cracking | Low | Low | Medium | Medium |
| flexural crack | Low | Medium | High | High |
| diagonal shear crack | Medium | High | High | High |
| crack along a bar | Medium | Medium | High | High |
| horizontal crack in a column | Medium | High | High | High |
| spalling with exposed bar | Medium | High | High | High |
| beam-column joint crack | Medium | High | High | High |

## Raises (only raise, never lower; capped at High)
**Element:** column +1 (a column carries everything above it).

**Location on the element (new):**
| Key | Meaning | Raise | Basis |
|---|---|---|---|
| `end_zone` | within about one element depth of a joint or support, where bars are anchored or lapped (length: assumption, to set with the engineer) | +1 for cracks along a bar and diagonal shear cracks | [46] ch. 2.1, 2.3 (splitting starts where the bar is anchored; anchorages with cracks along bars); diagonal shear near supports: assumption, to confirm |
| `middle` | the rest of the element | +0 | |
| `unknown` | not seen or not sure | **treated as an end zone** | rule 2: doubt never lowers a level |

**Warning signs:**
| Key | Sign | Effect | Basis |
|---|---|---|---|
| `growing` | wider than in the previous photo of the same crack, beyond the measurement uncertainty | +1 | [46] ch. 5.3; D23 |
| `rust_stain` | rust staining along the crack | +1 | v2 |
| `sticking_openings` | doors or windows started to stick | +1 | v2 |
| `recent_earthquake` | an earthquake since the crack was last seen | +1 | v2 |
| `added_floors` | floors added to the building | +1 | studio professor, 27 Oct |
| `thin_cover` **(new)** | where the bar is exposed: cover under about one bar diameter (measured on the scale card), or no stirrups visible | +1 | [46] ch. 2.3.3 (cover of 1 bar diameter: brittle failure), ch. 3.2 (thin cover and no stirrups: brittle splitting) |
| `crossing_bar_crack` **(new)** | the crack meets a crack running along a bar or stirrup | +1 | [46] ch. 4.4 (cracks along stirrups lower the bond) |
| `damp` **(new)** | damp, water marks or moss at the crack | +1 | assumption: [46] ch. 6.2 lists these signs as not yet evaluated; code exposure classes (Eurocode 2) not yet read |
| `offset` | one side of the crack displaced; measured: sliding larger than its uncertainty (±2 px at ≥ 3 px across [46] ch. 5.2) | straight to High | v2; [46] ch. 5.1 |
| `sagging` | visible sagging of a beam or slab | straight to High | v2 |

An unknown warning sign or location is a programming error, not a guess. Each sign counts once.

## Recorded, not rules (for the engineer's dossier)
- **Number and spacing of parallel cracks** on the element: measurable on existing structures and the key unknown when linking width to the load in the bar [46] ch. 4.1, 4.2; no rule links it to risk.
- **Bar diameter and cover depth** when the bar is exposed: the weakening from a crack along a bar grows with its width relative to the bar diameter [46] ch. 4.5.
- **Opening and sliding** of the crack, each with its uncertainty [46] ch. 5.2.

## Decision order
1. Photo not usable: Retake.
2. Material not concrete, or unsure: Expert needed.
3. Unknown element, unknown pattern, pattern not allowed on the element, pattern confidence below threshold, or width not measurable: Expert needed.
4. Base level from pattern x band (upper end of the width).
5. Element, then location, then warning signs raise it; cap at High.

## Output
Level, one-sentence reason (pattern, element, width with its upper end, band, and everything that raised the level), engineer-review flag (High and Expert needed), and a next step:

| Level | Next step (illustrative intervals) |
|---|---|
| Low | Routine monitoring: photograph the same crack again in 6 months. |
| Medium | Low-cost advice; photograph the same crack again in 1 month. If it has grown, it goes to an engineer. |
| High | An engineer must confirm; the case is sent now. |
| Expert needed | An engineer decides; the case is sent now. |
| Retake | Retake the photo following the protocol. |

## Where the numbers live
`src/triage/risk_matrix_v3.json`: version, bands, patterns, base table, element raise, locations, warning signs with their **basis**, next steps. Readable and editable by an engineer; every change is a new version recorded in `spec/decisions.md`. The code never changes a value on its own.

## What we need from the engineer (in order of importance)
**A. Values to set** (one card session, about 1 hour; see the calibration plan):
1. **Width band edges** (0.3, 1, 3 mm): right for reinforced concrete homes? Different per pattern?
2. **Base level of each pattern x band** (28 cells), and which patterns are **brittle**, so High even when narrow.
3. **Element weights:** column +1 only? A load-bearing wall, a beam over an open ground floor?
4. **End zone:** how long (one element depth? two?), which patterns it raises (along a bar, diagonal shear, horizontal crack in a column?).
5. **Thin cover / no stirrups:** is "cover under one bar diameter" the right line? +1, or straight to High?
6. **Warning signs:** is +1 right for each? Which go straight to High? Should damp be one at all?

**B. Definitions to confirm**
7. **Growth:** the smallest growth that counts, and over what interval (we use: larger than the combined uncertainty, D23).
8. **Accuracy:** is ±1 pixel at 3 pixels across the crack (±30 %) enough for triage, or do we require 6 to 8 pixels [46]?
9. **Confidence threshold** (0.8): how many referrals per week can an engineer take? (trade-off: fewer missed High vs more Expert needed)
10. **Dispatch and recheck times:** V1 within 1 week, V2 within 1 month, V3 recheck in 1 month (D27); Low in 6 months, Medium in 1 month.
11. **Building risk score:** are age over 50 years, floors added, changes and an open ground floor the right flags, and is "two flags = one tier up" right (D22)?

**C. Ground truth**
12. **Rate photos blind:** the same set of field photos rated by the engineer from the photo only (the non-AI baseline) and, where possible, on site (`spec/features/evaluation.md`).

## Calibration plan
1. **Literature anchors.** The reference thesis [46] gives the principles (pattern over width; brittle modes; anchorage, cover and confinement; measurement accuracy) but no width thresholds. Next, read Zaborac et al. 2019 [50], the Swiss and Spanish inspection guides [51][52], then FEMA 306, ACI 224R and Eurocode 2 (crack limits and exposure classes). No number from them enters the matrix before it is read in the source.
2. **Sense check on Haiti.** The Haiti engineers' damage definitions [41] against our bands.
3. **Engineer card session.** About 40 cards (element x location x pattern x width, with and without warning signs), each rated by each engineer on their own. Where they agree, the matrix takes their level; where they disagree, the more cautious one. Their agreement is reported as a result.
4. **Test on engineer-rated photos.** Target: almost no missed High (`spec/features/evaluation.md`), while tracking the share sent to experts.
5. **Version.** v3.1, v3.2, ... each recorded as a decision; never automatic.
