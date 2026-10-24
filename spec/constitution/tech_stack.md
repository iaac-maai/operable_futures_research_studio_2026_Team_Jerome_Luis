# Tech stack

Status: planned, not final.

- Language: Python.
- Detector: YOLO (finds the structural element and the crack). The `ultralytics` package is AGPL-3.0 (`spec/decisions.md` D9).
- Quality gate: written rules on sharpness and brightness, measured at a fixed working size (`spec/features/quality_gate.md`).
- Segmentation: U-Net (marks crack pixels).
- Measurement: plain code (width from the coin scale, length, angle).
- Pattern model: classifies crack type and reports confidence.
- Agent: adds construction type and footprint from a structural database over MCP.
- Rules: written triage rules in `src/triage/` (auditable, not learned).
- Interface: Streamlit prototype.
- Tests: pytest.

## Data
See `docs/data_map.md`.
