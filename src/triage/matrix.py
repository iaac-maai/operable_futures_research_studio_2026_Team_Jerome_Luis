"""Risk matrix and decision rules. Thresholds are illustrative until calibrated with a structural engineer.

Spec: spec/features/triage.md. Decisions: spec/decisions.md.
"""

import math
from dataclasses import dataclass

PATTERNS = ["plaster_crazing", "wall_vertical", "diagonal", "column_or_beam", "spalling_rust"]
PATTERN_NAMES = {
    "plaster_crazing": "plaster crazing",
    "wall_vertical": "vertical wall crack",
    "diagonal": "diagonal (shear) crack",
    "column_or_beam": "column or beam crack",
    "spalling_rust": "spalling with rust",
}
SUPPORTED_MATERIALS = {"concrete"}  # reinforced concrete only (decision D17)
# rows: width bands; columns: PATTERNS
MATRIX = {
    "under_0.3": ["Low", "Low", "Medium", "Medium", "Medium"],
    "0.3_to_1": ["Low", "Medium", "Medium", "High", "High"],
    "1_to_3": ["Medium", "Medium", "High", "High", "High"],
    "over_3": ["Medium", "High", "High", "High", "High"],
}
BAND_NAMES = {"under_0.3": "under 0.3 mm", "0.3_to_1": "0.3 to 1 mm", "1_to_3": "1 to 3 mm", "over_3": "over 3 mm"}
CONFIDENCE_THRESHOLD = 0.8  # illustrative; fixed here so callers cannot lower it
MATERIAL_THRESHOLD = 0.8  # illustrative; below it the material counts as unsure
NEEDS_ENGINEER = {"High", "Expert needed"}


@dataclass(frozen=True)
class Result:
    level: str  # Low, Medium, High, Retake or Expert needed
    reason: str
    engineer_review: bool


def width_band(width_mm: float) -> str:
    """Lower bound inclusive: a crack on a boundary goes to the wider band."""
    if width_mm < 0.3:
        return "under_0.3"
    if width_mm < 1:
        return "0.3_to_1"
    if width_mm < 3:
        return "1_to_3"
    return "over_3"


def _valid(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _result(level: str, reason: str) -> Result:
    return Result(level, reason, level in NEEDS_ENGINEER)


def assess(pattern: str, width_mm: float, confidence: float, image_ok: bool, *,
           material: str = "concrete", material_confidence: float = 1.0) -> Result:
    """Return level, one-sentence reason and engineer-review flag. Any doubt goes to an expert.
    Order (spec/features/pipeline.md): photo usable -> material supported -> pattern -> confidence -> width."""
    if image_ok is not True:
        return _result("Retake", "Photo not usable (blur, light or coin missing): retake it.")
    if not _valid(material_confidence) or not MATERIAL_THRESHOLD <= material_confidence <= 1:
        return _result("Expert needed", "Material unclear from the photo: an engineer decides.")
    if material not in SUPPORTED_MATERIALS:
        return _result("Expert needed", f"Material not supported ({material}): an engineer decides.")
    if pattern not in PATTERNS:
        return _result("Expert needed", "Crack pattern not recognised.")
    if not _valid(confidence) or not 0 <= confidence <= 1:
        return _result("Expert needed", "Model confidence missing or invalid.")
    if confidence < CONFIDENCE_THRESHOLD:
        return _result("Expert needed", f"Model not confident enough ({confidence:.2f}).")
    if not _valid(width_mm) or width_mm < 0:
        return _result("Expert needed", "Crack width could not be measured.")
    band = width_band(width_mm)
    level = MATRIX[band][PATTERNS.index(pattern)]
    reason = f"{PATTERN_NAMES[pattern]}, {width_mm:g} mm wide ({BAND_NAMES[band]} band): {level}."
    return _result(level, reason)


def triage(pattern: str, width_mm: float, confidence: float, image_ok: bool, **material) -> str:
    """Return Low, Medium, High, 'Retake' or 'Expert needed'."""
    return assess(pattern, width_mm, confidence, image_ok, **material).level
