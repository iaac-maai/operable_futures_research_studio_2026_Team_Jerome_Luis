# Tech stack

Status: planned, not final. Full pipeline: `spec/features/pipeline.md`.

- Language: Python.
- Quality gate: written rules on sharpness and brightness, measured at a fixed working size (`spec/features/quality_gate.md`).
- Material check: image classifier, concrete / not concrete / unsure, with confidence; trained first on public concrete and brick images.
- Detector: YOLO (finds the structural element and the crack). The `ultralytics` package is AGPL-3.0 (`spec/decisions.md` D9).
- Segmentation: U-Net (marks crack pixels).
- Measurement: plain code (width from the coin scale with an uncertainty range, length, orientation).
- Pattern model: classifies crack type and reports its probability.
- Agent: adds construction type and footprint from a structural database over MCP.
- Rules: written triage rules in `src/triage/` (auditable, not learned).
- Interfaces: resident app and engineer review screen (Streamlit prototype).
- Learning loop: engineer corrections stored as labels; batch retraining of the learned models, checked on held-out data before use (human-in-the-loop learning).
- Tests: pytest.

## Data
See `docs/data_map.md`.
