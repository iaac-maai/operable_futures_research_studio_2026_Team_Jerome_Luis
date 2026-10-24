# Second Look

A second look at cracks in buildings nobody inspects. Phone photo in, risk level out, engineer confirms every High.

IAAC Barcelona, MaAI, Research Studio "Operable Futures", 2026-27.
Team: Jerome Eid (@jeromgeid-ui), Luis Sebastian Wulf (@wulfluis).
Project stage: Stage 4, Operation and End-of-Life.

## Problem
Residents of old buildings see cracks every day but cannot tell a harmless one from a sign of structural failure, and engineers are too few to inspect every building.
Tripoli, February 2026: two blocks collapsed on 8 February (14 to 15 dead, per AFP and Reuters), and 114 buildings were ordered evacuated.
Rana Plaza, Dhaka, 2013: cracks were visible the day before the collapse.

## What it does
Phone photo (with a coin for scale) -> quality gate -> YOLO (finds element and crack) -> U-Net (crack pixels) -> measurement (width, length, angle)
-> pattern model and AI agent (building data over MCP) -> written triage rules -> Low, Medium, High, "Expert needed" or "Retake", each with a one-sentence reason.
It never gives a permit or a clearance. Any doubt goes to an expert, and an engineer confirms every High.

## Data
See `docs/data_map.md`. Public sets (SDNET2018, CC BY 4.0; CrackSeg9k, CC0; PEER Hub ImageNet, CC BY-NC-SA 4.0) cover concrete, pavement and post-earthquake images.
Engineer-labelled phone photos of columns, beams and brick walls are still to be collected. Raw data is not committed; `data/` stays empty in the repository.

## Method and status
The risk matrix and decision rules are implemented in `src/triage/` with tests. Thresholds are illustrative until calibrated with a structural engineer.
The confusion tables (true and false positives and negatives, with missed High as the key error) are defined in `spec/features/evaluation.md` and coded in `src/triage/evaluate.py`.
The quality gate (`src/quality/`) ran as a first test on 8,288 real images from two public datasets; it found and fixed a resolution bug in the blur check (`docs/experiments/`).
Models are not trained yet. Decisions are logged in `spec/decisions.md`. The 10-week plan is in `spec/constitution/roadmap.md`.

## Results
None yet. Success means beating the non-AI baseline (an engineer's visual check) on held-out, engineer-labelled photos, while missing almost no High cases (a target, not a result).
We stop or redesign if the tool misses High cases that engineers would flag.

## Limitations
A surface photo cannot show rebar, concrete strength or foundations. Concrete and brick crack differently and need separate data.
Public crack data is mostly concrete and pavement.

## Repository map
- `AGENTS.md`: system constitution for coding agents
- `spec/constitution/`: mission, roadmap, tech stack
- `spec/features/`: triage and evaluation specs; `spec/decisions.md`: decisions log
- `docs/`: segmentation tree, data map, sources
- `src/triage/`: risk matrix, decision logic and evaluation tables
- `tests/`: tests (the comparison against the non-AI baseline runs once engineer-labelled photos exist)
- `notebook/`, `figures/`, `models/`, `data/`: notebooks, plots, model files, local data (large files are not committed)
- `requirements.txt`: Python packages

## AI usage disclosure
This repository was set up with help from Claude (Anthropic). Review everything before relying on it.

## Run the tests
    pip install -r requirements.txt
    pytest

## License
Code under the MIT License (see `LICENSE`). Datasets follow their own terms.
