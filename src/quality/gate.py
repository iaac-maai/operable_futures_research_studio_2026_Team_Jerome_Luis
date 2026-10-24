"""Quality gate: written rules for whether a photo is usable. Spec: spec/features/quality_gate.md.

Thresholds are illustrative until tuned on our own phone photos.
"""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

MIN_SHARPNESS = 100.0
MIN_BRIGHTNESS = 40.0
MAX_BRIGHTNESS = 220.0


@dataclass(frozen=True)
class GateResult:
    image_ok: bool
    sharpness: float
    brightness: float
    failed: list[str] = field(default_factory=list)


def to_grey(path: str | Path) -> np.ndarray:
    with Image.open(path) as img:
        return np.asarray(img.convert("L"), dtype=np.float64)


def sharpness(grey: np.ndarray) -> float:
    """Variance of the 4-neighbour Laplacian over the interior pixels."""
    lap = (grey[:-2, 1:-1] + grey[2:, 1:-1] + grey[1:-1, :-2] + grey[1:-1, 2:] - 4 * grey[1:-1, 1:-1])
    return float(lap.var())


def check(grey: np.ndarray, coin_visible: bool | None = None) -> GateResult:
    """Every check must pass; a missing coin result counts as a fail."""
    s, b = sharpness(grey), float(grey.mean())
    failed = []
    if s < MIN_SHARPNESS:
        failed.append("blurred")
    if b < MIN_BRIGHTNESS:
        failed.append("too dark")
    if b > MAX_BRIGHTNESS:
        failed.append("too bright")
    if coin_visible is not True:
        failed.append("coin not confirmed")
    return GateResult(not failed, s, b, failed)
