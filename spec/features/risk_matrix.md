# Feature: risk matrix v2 (`src/triage/risk_matrix_v2.json`, `src/triage/matrix.py`)

Status: implemented as **v2.0-illustrative** (26 Oct 2026). Every level, band and interval below is illustrative until calibrated with the engineering partners (section "Calibration plan"). Replaces the v1 pattern x width table (`spec/decisions.md` D20).

## Why v2
v1 ignored the structural element, mixed surface finishes with structural patterns, had no warning signs, ignored measurement uncertainty and kept its numbers in code. v2 fixes all five.

## Inputs
| Input | From pipeline stage | Values |
|---|---|---|
| Element | 4 (detector) or element tag | column, beam, slab, load-bearing wall, infill wall |
| Pattern | 6 (pattern model) | the seven patterns below |
| Width (mm) and its uncertainty (mm) | 5 (measurement) | the matrix uses the **upper bound** = width + uncertainty |
| Pattern confidence | 6 | 0 to 1, threshold 0.8 (illustrative) |
| Material and its confidence | 3 | concrete only (D17) |
| Escalators | resident answers, a second photo, building data over MCP | list below |

## Patterns (reinforced concrete)
| Key | Name | What it can mean | Allowed elements |
|---|---|---|---|
| `surface_map` | surface map cracking | shrinkage of the finish or cover, not structural | all |
| `flexural` | flexural (bending) crack | bending of the element | all |
| `diagonal_shear` | diagonal shear crack | shear; brittle failure possible | all |
| `along_bar` | crack along a bar | splitting, often from bar corrosion | all |
| `column_horizontal` | horizontal crack in a column | bending or axial overload of the column | column only |
| `spalling_exposed_bar` | spalling with exposed or rusted bar | loss of cover, advanced corrosion | all |
| `joint` | crack at a beam-column joint | joint damage | column, beam |

A pattern on an element where it is not allowed (for example a horizontal column crack on a slab) goes to Expert needed: the models disagree with each other.

## Width bands (illustrative)
Lower bound inclusive: `under_0.3` [0, 0.3), `0.3_to_1` [0.3, 1), `1_to_3` [1, 3), `over_3` [3, inf). Computed on the upper bound of the measured width.

## Base levels: pattern x width band (illustrative)
| Pattern | under 0.3 mm | 0.3 to 1 mm | 1 to 3 mm | over 3 mm |
|---|---|---|---|---|
| surface map cracking | Low | Low | Medium | Medium |
| flexural crack | Low | Medium | High | High |
| diagonal shear crack | Medium | High | High | High |
| crack along a bar | Medium | Medium | High | High |
| horizontal crack in a column | Medium | High | High | High |
| spalling with exposed bar | Medium | High | High | High |
| beam-column joint crack | Medium | High | High | High |

## Element criticality (only raises)
Column: +1 level (a column carries everything above it). Beam, slab, load-bearing wall, infill wall: +0. Never lowers a level.

## Escalators (only raise, never lower; AGENTS.md rule 8)
| Key | Sign | Effect |
|---|---|---|
| `growing` | wider than in the previous photo of the same crack | +1 level |
| `rust_stain` | rust staining along the crack | +1 level |
| `sticking_openings` | doors or windows started to stick | +1 level |
| `recent_earthquake` | an earthquake since the crack was last seen | +1 level |
| `added_floors` | floors added to the building (building data) | +1 level |
| `offset` | one side of the crack displaced (a step across it) | straight to High |
| `sagging` | visible sagging of a beam or slab | straight to High |

Levels are capped at High. An unknown escalator is a programming error, not a guess.

## Decision order
1. Photo not usable: Retake.
2. Material not concrete, or unsure: Expert needed.
3. Unknown element, unknown pattern, pattern not allowed on the element, pattern confidence below threshold, or width not measurable: Expert needed.
4. Base level from pattern x band (upper bound of width).
5. Element criticality, then escalators; cap at High.

## Output
Level, one-sentence reason (pattern, element, width with its upper bound, band, and what raised the level), engineer-review flag (High and Expert needed), and a **next step with a recheck interval**:

| Level | Next step (illustrative intervals) |
|---|---|
| Low | Routine monitoring: photograph the same crack again in 6 months. |
| Medium | Low-cost advice; photograph the same crack again in 1 month. If it has grown, it goes to an engineer. |
| High | An engineer must confirm; the case is sent now. |
| Expert needed | An engineer decides; the case is sent now. |
| Retake | Retake the photo following the protocol. |

## Where the numbers live
`src/triage/risk_matrix_v2.json`: version, bands, patterns, base table, element criticality, escalators, next steps. Readable and editable by an engineer; every change is a new version recorded in `spec/decisions.md`. The code never changes a value on its own.

## Calibration plan
1. **Literature anchors.** Check how engineering references classify crack damage in reinforced concrete by width and pattern (candidates to verify: FEMA 306 for damaged concrete walls, ACI 224R, Eurocode 2 crack-width limits, and the reference thesis [Corres Sojo 2024]). No number from them enters the matrix before it is read in the source.
2. **Sense check on Haiti.** The Haiti engineers' damage definitions (light: hairline; moderate: wider cracks or spalling; severe: see-through cracks or failure) [41] against our bands.
3. **Engineer session.** About 30 to 40 cards (element x pattern x width, with and without escalators). Each engineer rates each card on their own. Where they agree, the matrix takes their level; where they disagree, the more cautious level. Their agreement is reported as a result.
4. **Test on engineer-rated photos.** Target: almost no missed High (`spec/features/evaluation.md`), while tracking the share sent to experts.
5. **Version.** v2.1, v2.2, ... each recorded as a decision; never automatic.
