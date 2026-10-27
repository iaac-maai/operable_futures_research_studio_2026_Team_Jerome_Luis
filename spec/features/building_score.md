# Feature: building risk score and priority (`spec/features/building_score.md`)

Status: specified on 27 Oct 2026; code planned for 12 Nov (`spec/constitution/roadmap.md`). Every threshold is illustrative until calibrated with the engineering partners (decision D22).

## Why
Engineers do not judge a crack alone: they read the pattern across the building and whether cracks are growing (studio professor, 27 Oct). The building risk score ranks buildings so that scarce engineers visit the right ones first (mission). It is a written, auditable rule (AGENTS.md rule 5), not a learned model.

## Inputs
**Building case (S scale)**, answered once by the field worker or the resident. Every question accepts "unknown".

| Key | Question | Risk flag when |
|---|---|---|
| `age` | When was the building built? | More than 50 years ago (assumption: a common design working life for buildings; to verify), or unknown |
| `added_floors` | Were floors added after the building was built? | Yes, or unknown |
| `changed` | Were walls or columns removed, the ground floor opened (for example for shops), or the use changed (for example housing to workshop)? | Yes, or unknown |
| `open_ground_floor` | Is the ground floor open (shops, parking) with few walls? | Yes, or unknown |
| `typology` | Reinforced concrete frame with masonry infill / reinforced concrete walls / other or mixed | Not a flag. "Other or mixed" means not reinforced concrete: every crack goes to an engineer (D17) |
| `storeys` | How many storeys? | Not a flag; recorded for the dossier and the sort order |
| `occupants` | About how many people live or work in it? | Not a flag; recorded for the sort order |

The age, added floors and typology changes come from the professor's list of building data (27 Oct). Unknown counts as a flag because a missing answer must not make a building look safer; the dossier shows it as unknown.

**Crack results (P and O scales):** the level of every crack recorded in the building, after the element rule and the warning signs, including growth (matrix v2, `spec/features/monitoring.md`).

## Rules (illustrative)
1. **Base tier from the worst crack:** any High: P1. Otherwise any Medium or Expert needed: P2. Otherwise (only Low, or no crack recorded yet): P3.
2. **Building data:** two or more risk flags: one tier higher.
3. **Damage spread:** Medium or worse in two or more different elements: one tier higher.
4. Tiers stop at P1. The score never lowers a crack level and is never shown to residents as "safe".
5. **Order within a tier:** number of High cracks, then number of growing cracks, then number of risk flags, then occupants.

Output: the tier, the rules that raised it (one sentence each), and the list of unknown answers.

## Meaning of the tiers (illustrative)
| Tier | Meaning |
|---|---|
| P1 | An engineer visits as soon as possible. |
| P2 | An engineer visits within a month. |
| P3 | Monitoring: the resident photographs the cracks again on their recheck dates. |

Every High and every referral is also confirmed by an engineer on the review screen, whatever the tier (AGENTS.md rule 4).

## Example
A 60-year-old building (flag) with floors added (flag), one Medium crack in a beam and one Medium crack in a column: base P2 (worst crack Medium); two flags: P1. Reason shown: "Worst crack: Medium; raised because 2 building risk flags (older than 50 years, floors added)."
Note: a crack in a column is already raised one level by the element rule, so a Medium in a column means its base pattern was Low.

## Calibration
1. Check rapid visual screening methods for buildings (candidates to verify: FEMA P-154 and the GEM building taxonomy) before any threshold changes.
2. The engineering partners rate about 20 building cases (questionnaire plus crack results) from P1 to P3; where the rules disagree with them, the rules change in a reviewed version.

## Tests (when coded)
- Each base tier; each raise; the cap at P1; unknown answers count as flags; "other or mixed" typology sends every crack to an engineer; the order within a tier; a building with no crack recorded is P3 unless raised; the reasons list every rule that fired.
