# Feature: figures (`src/viz/figures.py`)

Status: implemented. Run `py src/viz/figures.py` from the repository root; PNGs go to `figures/`.

Every figure is drawn from the repo's own rules and data map, so it changes when they change. None shows a measured result.

| File | Shows | Drawn from |
|---|---|---|
| `01_pipeline.png` | Pipeline v3: three scales (S, O, P as in PHI-Net task 1) x five phases, scene check, monitoring and learning loops, status of each box | `spec/features/pipeline.md` |
| `01b_pipeline_flow.png` | Step 0, report and dispatch (when a field worker visits: V1, V2, V3, D27), then the same pipeline v3 drawn as a task flow: phases as numbered columns, scales as lanes; diamonds for written checks with stop (Retake, Expert needed) and continue marks, stacked boxes for learned models, both loops. Black, white and grey only: white = photos and people, grey = written rules (code), black = learned models | `spec/features/pipeline.md`, `spec/features/dispatch.md` |
| `02_decisions_and_players.png` | Decisions and players: the five players (resident, app models, app written rules, field worker, engineer) as lifelines, time going down, 14 numbered hand-offs showing what passes between them; decisions only on the written rules (dispatch, triage + building score) and the engineer (confirms or corrects); a 'who decides what' panel. Same black, white and grey style as 01b | `triage.dispatch.screen()`, `triage.matrix.assess()`, `spec/features/building_score.md` |
| `03_risk_matrix.png` | Matrix v3 in black, white and grey, symbols only (key below): base category per pattern x width band (1 white, 2 grey, 3 black) and a card for every raise (+1, or straight to 3); ? marks an assumption | `src/triage/risk_matrix_v3.json` (read at run time) |
| `04_segmentation_tree.png` | Tree v3: crack path (yellow) into the atomic problem, building path (navy) into the building risk score, context (grey); scale badge and evidence under each node | `docs/segmentation_tree.md` |
| `05_data_coverage.png` | Which data source feeds which pipeline stage, by scale | `docs/data_map.md`, section 1 |
| `06_dataset_sizes.png` | Image counts and licences of public sets vs our target data | `docs/data_map.md`, section 2 |
| `07_confusion_template.png` | TP / FN / FP / TN and the full 3 x 5 confusion matrix, no counts | `spec/features/evaluation.md` |
| `08_real_data_quality_gate.png` | Sharpness of public dataset images against the blur limit (made by `src/experiments/real_data_quality.py`, not by this script) | Haiti 2010, Darbhanga, Strathclyde, PHI-Net tasks 8, 3 and 6, METU, SDNET2018, crack-seg; panels ordered by fit to the concept |
| `09_timeline.png` | Plan to the final presentation (17 Dec) with syllabus milestones and tasks at risk | `spec/constitution/roadmap.md` |
| `10_dataset_comparison.png` | Every dataset on our disk side by side, in order of fit: images, quality gate pass rate, labels, what it trains, licence; one row per PHI-Net task | `docs/data_map.md`, sections 0 and 6; gate rates from `data/processed/real_data_quality.csv` |

Colour rules: flow figures (01b, 02) and the matrix (03) use black, white and grey only: white = photos and people, grey = written rules, black = learned models; in the matrix, Category 1 white, 2 grey, 3 black, always with the number. Older figures (07, 09) still use the status colours, always with a text label; coverage uses one blue ramp.

When `docs/` changes, update the data constants in `figures.py` (TREE, COVERAGE, DATASETS, HELD, PLAN, MILESTONES) and rerun.
Later, once engineer-labelled photos exist: a filled confusion matrix and the measured threshold curve (missed Category 3 vs referral rate).

## Symbol key of the risk matrix (`03_risk_matrix.png`)
| Symbol | Means |
|---|---|
| Network of fine cracks on a panel | surface map cracking |
| Beam with short vertical cracks from the bottom | flexural crack |
| Beam with a diagonal crack near its support | diagonal shear crack |
| Crack running over a dashed bar | crack along a bar |
| Column with horizontal cracks | horizontal crack in a column |
| Missing patch with a bar showing | spalling with exposed bar |
| Cross of beam and column with an X at the joint | beam-column joint crack |
| Lines of growing thickness | crack width bands (< 0.3, 0.3–1, 1–3, > 3 mm) |
| Column under a load arrow | it is a column (+1) |
| Grey end of a beam next to a column | end zone, or location unknown (+1 for cracks along bars and diagonal shear) |
| Crack with arrows pointing outward | the crack is growing |
| Grey stain below a crack | rust staining |
| Door skewed in its frame | doors or windows started to stick |
| Seismograph trace | an earthquake since the last photo |
| Building with a dashed extra floor | floors added |
| Bar close to the surface with a small gap mark | thin cover or no stirrups |
| Crack crossing a crack along a bar | the crack meets a crack along a bar or stirrup |
| Water drops | damp, water marks or moss |
| Step across a crack | offset: one side displaced (straight to 3) |
| Beam bending down between supports | sagging (straight to 3) |
| Eye, 6 mo | Category 1: routine monitoring, recheck in 6 months |
| Wrench, 1 mo | Category 2: low-cost repair advice, recheck in 1 month |
| Hard hat, now | Category 3: an engineer must confirm now |
| ? → hard hat | any doubt: Expert needed, an engineer decides |
| Camera and circular arrow | Retake |
| Small ? on a card | the value is an assumption, to confirm with the engineer |
