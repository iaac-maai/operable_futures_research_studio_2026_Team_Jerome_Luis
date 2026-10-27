# Feature: figures (`src/viz/figures.py`)

Status: implemented. Run `py src/viz/figures.py` from the repository root; PNGs go to `figures/`.

Every figure is drawn from the repo's own rules and data map, so it changes when they change. None shows a measured result.

| File | Shows | Drawn from |
|---|---|---|
| `01_pipeline.png` | Pipeline v3: three scales (S, O, P as in PHI-Net task 1) x five phases, scene check, monitoring and learning loops, status of each box | `spec/features/pipeline.md` |
| `01b_pipeline_flow.png` | Step 0, report and dispatch (when a field worker visits: V1, V2, V3, D27), then the same pipeline v3 drawn as a task flow: phases as numbered columns, scales as lanes; diamonds for written checks with stop (Retake, Expert needed) and continue marks, stacked boxes for learned models, both loops. Black, white and grey only: white = photos and people, grey = written rules (code), black = learned models | `spec/features/pipeline.md`, `spec/features/dispatch.md` |
| `02_decisions_and_players.png` | Decisions and players: the five players (resident, app models, app written rules, field worker, engineer) as lifelines, time going down, 14 numbered hand-offs showing what passes between them; decisions only on the written rules (dispatch, triage + building score) and the engineer (confirms or corrects); a 'who decides what' panel. Same black, white and grey style as 01b | `triage.dispatch.screen()`, `triage.matrix.assess()`, `spec/features/building_score.md` |
| `03_risk_matrix.png` | Matrix v3: base level per pattern x width band, and what raises it (element, location on the element, warning signs; new and assumed raises tagged) | `src/triage/risk_matrix_v3.json` (read at run time) |
| `04_segmentation_tree.png` | Tree v3: crack path (yellow) into the atomic problem, building path (navy) into the building risk score, context (grey); scale badge and evidence under each node | `docs/segmentation_tree.md` |
| `05_data_coverage.png` | Which data source feeds which pipeline stage, by scale | `docs/data_map.md`, section 1 |
| `06_dataset_sizes.png` | Image counts and licences of public sets vs our target data | `docs/data_map.md`, section 2 |
| `07_confusion_template.png` | TP / FN / FP / TN and the full 3 x 5 confusion matrix, no counts | `spec/features/evaluation.md` |
| `08_real_data_quality_gate.png` | Sharpness of public dataset images against the blur limit (made by `src/experiments/real_data_quality.py`, not by this script) | Haiti 2010, Darbhanga, Strathclyde, PHI-Net tasks 8, 3 and 6, METU, SDNET2018, crack-seg; panels ordered by fit to the concept |
| `09_timeline.png` | Plan to the final presentation (17 Dec) with syllabus milestones and tasks at risk | `spec/constitution/roadmap.md` |
| `10_dataset_comparison.png` | Every dataset on our disk side by side, in order of fit: images, quality gate pass rate, labels, what it trains, licence; one row per PHI-Net task | `docs/data_map.md`, sections 0 and 6; gate rates from `data/processed/real_data_quality.csv` |

Colour rules: triage levels always use the same four status colours (Low green, Medium yellow, High red, Expert needed orange) and always carry a text label; coverage uses one blue ramp.

When `docs/` changes, update the data constants in `figures.py` (TREE, COVERAGE, DATASETS, HELD, PLAN, MILESTONES) and rerun.
Later, once engineer-labelled photos exist: a filled confusion matrix and the measured threshold curve (missed High vs referral rate).
