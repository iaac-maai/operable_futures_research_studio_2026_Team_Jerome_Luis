# Tech stack

Status: planned, not final. Full pipeline: `spec/features/pipeline.md`.

- Language: Python.
- Quality gate: written rules on sharpness and brightness, measured at a fixed working size (`spec/features/quality_gate.md`).
- Material model: image classifier, concrete / not concrete / unsure, with confidence; trained first on public concrete and brick images. Residents are never asked the material (D25).
- Element model: image classifier on the element photo (column, beam, slab, wall), pre-trained on PHI-Net task 6 [55]. YOLO only if element boxes are needed later; the `ultralytics` package is AGPL-3.0 (`spec/decisions.md` D9).
- Segmentation: U-Net (marks crack pixels).
- Measurement: plain code (width from the printed scale card, coin as backup, with an uncertainty of ±1 pixel; length, orientation).
- Pattern model: classifies the crack pattern and reports its probability; pre-trained on PHI-Net tasks 3 and 8, the other patterns need our labels.
- Agent: adds construction type and footprint from a structural database over MCP.
- Rules: written triage rules in `src/triage/` (auditable, not learned): risk matrix v2 per crack; building risk score per building (`spec/features/building_score.md`).
- Monitoring: crack IDs, marker stickers and repeat photos (`spec/features/monitoring.md`).
- Interfaces: resident app and engineer review screen (Streamlit prototype).
- Learning loop: engineer corrections stored as labels; batch retraining of the learned models, checked on held-out data before use (human-in-the-loop learning).
- Tests: pytest.

## Data
See `docs/data_map.md`.
