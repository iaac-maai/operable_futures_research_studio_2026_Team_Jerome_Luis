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
WORK_SIZE = 512  # long side in px for measuring; sharpness depends on resolution (decision D8)


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


def to_work_size(grey: np.ndarray) -> np.ndarray:
    """Scale down so the long side is WORK_SIZE; smaller images are returned unchanged."""
    h, w = grey.shape
    if max(h, w) <= WORK_SIZE:
        return grey
    img = Image.fromarray(np.clip(grey, 0, 255).astype(np.uint8))
    img.thumbnail((WORK_SIZE, WORK_SIZE), Image.Resampling.LANCZOS)
    return np.asarray(img, dtype=np.float64)


def check(grey: np.ndarray, coin_visible: bool | None = None) -> GateResult:
    """Every check must pass; a missing coin result counts as a fail."""
    work = to_work_size(grey)
    s, b = sharpness(work), float(work.mean())
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
