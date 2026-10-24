"""Risk matrix and decision rules. Thresholds are illustrative until calibrated with a structural engineer."""

PATTERNS = ["plaster_crazing", "wall_vertical", "diagonal_step", "column_or_beam", "spalling_rust"]
# rows: width bands; columns: PATTERNS
MATRIX = {
    "under_0.3": ["Low", "Low", "Medium", "Medium", "Medium"],
    "0.3_to_1": ["Low", "Medium", "Medium", "High", "High"],
    "1_to_3": ["Medium", "Medium", "High", "High", "High"],
    "over_3": ["Medium", "High", "High", "High", "High"],
}


def width_band(width_mm: float) -> str:
    if width_mm < 0.3:
        return "under_0.3"
    if width_mm < 1:
        return "0.3_to_1"
    if width_mm <= 3:
        return "1_to_3"
    return "over_3"


def triage(pattern: str, width_mm: float, confidence: float, image_ok: bool, threshold: float = 0.8) -> str:
    """Return Low, Medium, High, 'Retake' or 'Expert needed'. Any doubt goes to an expert."""
    if not image_ok:
        return "Retake"
    if pattern not in PATTERNS or confidence < threshold:
        return "Expert needed"
    return MATRIX[width_band(width_mm)][PATTERNS.index(pattern)]
