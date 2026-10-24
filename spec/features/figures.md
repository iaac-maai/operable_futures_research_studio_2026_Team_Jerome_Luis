# Feature: figures (`src/viz/figures.py`)

Status: implemented. Run `py src/viz/figures.py` from the repository root; PNGs go to `figures/`.

Every figure is drawn from the repo's own rules and data map, so it changes when they change. None shows a measured result.

| File | Shows | Drawn from |
|---|---|---|
| `01_pipeline.png` | Photo-to-triage pipeline, coloured by learned / written rule / human | Deck slide 5, `tech_stack.md` |
| `02_decision_flow.png` | Order of checks: Retake, Expert needed, matrix, engineer review | `triage.matrix.assess()` |
| `03_risk_matrix.png` | Width band x pattern -> level | `triage.matrix.MATRIX` (read at run time) |
| `04_segmentation_tree.png` | Macro, meso, micro, atomic, with scope tags | `docs/segmentation_tree.md` |
| `05_data_coverage.png` | Which data source feeds which pipeline stage | `docs/data_map.md`, section 1 |
| `06_dataset_sizes.png` | Image counts and licences of public sets vs our target data | `docs/data_map.md`, section 2 |
| `07_confusion_template.png` | TP / FN / FP / TN and the full 3 x 5 confusion matrix, no counts | `spec/features/evaluation.md` |
| `08_real_data_quality_gate.png` | Sharpness of public dataset images against the blur limit (made by `src/experiments/real_data_quality.py`, not by this script) | crack-seg, Darbhanga; SDNET2018 when downloaded |
| `09_timeline.png` | 10-week plan with workstreams, milestones and tasks at risk | `spec/constitution/roadmap.md` |

Colour rules: triage levels always use the same four status colours (Low green, Medium yellow, High red, Expert needed orange) and always carry a text label; coverage uses one blue ramp.

When `docs/` changes, update the data constants in `figures.py` (TREE, COVERAGE, DATASETS, PLAN, MILESTONES) and rerun.
Later, once engineer-labelled photos exist: a filled confusion matrix and the measured threshold curve (missed High vs referral rate).
