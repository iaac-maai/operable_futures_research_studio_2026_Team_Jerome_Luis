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
-> pattern model and AI agent (building data over MCP) -> written triage rules -> Low, Medium, High, or "Expert needed".
It never gives a permit or a clearance. Any doubt goes to an expert, and an engineer confirms every High.

## Data
See `docs/data_map.md`. Public sets (SDNET2018, CrackSeg9k, PEER Hub ImageNet) cover concrete, pavement and post-earthquake images.
Engineer-labelled phone photos of columns, beams and brick walls are still to be collected. Raw data is not committed; `data/` stays empty in the repository.

## Method and status
The risk matrix and decision rules are implemented in `src/triage/` with tests. Thresholds are illustrative until calibrated with a structural engineer.
Models are not trained yet.

## Results
None yet. Success means beating the non-AI baseline (an engineer's visual check) on held-out, engineer-labelled photos, while missing almost no High cases.
We stop or redesign if the tool misses High cases that engineers would flag.

## Limitations
A surface photo cannot show rebar, concrete strength or foundations. Concrete and brick crack differently and need separate data.
Public crack data is mostly concrete and pavement.

## Repository map
- `AGENTS.md`: system constitution for coding agents
- `spec/constitution/`: mission, roadmap, tech stack
- `docs/`: segmentation tree and data map
- `src/triage/`: code (risk matrix and decision logic)
- `tests/`: tests, including the comparison against the non-AI baseline
- `notebook/`, `figures/`, `models/`, `data/`: notebooks, plots, model files, local data (large files are not committed)
- `requirements.txt`: Python packages

## AI usage disclosure
This repository was set up with help from Claude (Anthropic). Review everything before relying on it.

## Run the tests
    pip install -r requirements.txt
    pytest

## License
Code under the MIT License (see `LICENSE`). Datasets follow their own terms.
