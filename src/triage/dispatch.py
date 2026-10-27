"""Report and dispatch: whether a resident's crack report sends a field worker, and how soon.

Spec: spec/features/dispatch.md. Decision D27. Every value is illustrative until calibrated.
It returns a visit priority, never a triage level: the five levels are given only after the field visit.
"""

import hashlib
import math
from dataclasses import dataclass

from triage.matrix import CONFIDENCE_THRESHOLD, ESCALATORS

URGENT_SIGNS = {"offset", "sagging"}  # straight to High in matrix v2
WATCH_SIGNS = {"growing", "rust_stain", "sticking_openings", "recent_earthquake"}  # residents can report these
URGENT_WIDTH_MM = 1.0  # upper end of the width; from 1 mm matrix v2 can reach High
VISIT_WIDTH_MM = 0.3  # first band edge of matrix v2
MAX_RETAKES = 2
BUILDING_FLAGS_FOR_VISIT = 2  # as in the building risk score (D22)
AUDIT_ONE_IN = 10

NEXT_STEPS = {
    "V1": "A field worker will visit within a week. An engineer has been told today.",
    "V2": "A field worker will visit within a month. If the crack changes before then, photograph it again.",
    "V3": "Not assessed yet: no field worker has seen this crack. Photograph it again in 1 month, and at once if it "
          "grows, if doors or windows stick, or after an earthquake.",
    "Retake": "Retake the photo with the scale card, following the guide.",
}


@dataclass(frozen=True)
class Dispatch:
    tier: str  # V1 (visit within 1 week), V2 (within 1 month), V3 (no visit yet) or Retake
    reason: str
    next_step: str


def _known(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x >= 0


def _dispatch(tier: str, reason: str) -> Dispatch:
    return Dispatch(tier, reason, NEXT_STEPS[tier])


def screen(image_ok: bool, crack_confidence: float, width_upper_mm: float | None = None, *, signs=(),
           building_flags: int = 0, retakes: int = 0) -> Dispatch:
    """First match wins (spec table). width_upper_mm is None when no scale is visible."""
    signs = set(signs)
    unknown = signs - set(ESCALATORS)
    if unknown:
        raise ValueError(f"unknown warning sign(s): {sorted(unknown)}")
    if signs & URGENT_SIGNS:
        return _dispatch("V1", f"{ESCALATORS[sorted(signs & URGENT_SIGNS)[0]].capitalize()}: an engineer must see it soon.")
    if image_ok is not True:
        if retakes >= MAX_RETAKES:
            return _dispatch("V2", "The photo could not be used after two retakes: a field worker will take it.")
        return _dispatch("Retake", "Photo not usable (blur, light or scale card missing): retake it.")
    width_known = _known(width_upper_mm)
    if width_known and width_upper_mm >= URGENT_WIDTH_MM:
        return _dispatch("V1", f"The crack may be {width_upper_mm:.1f} mm wide or more: a wide crack is seen soon.")
    watch = sorted(signs & WATCH_SIGNS)
    if "growing" in watch and len(watch) > 1:
        return _dispatch("V1", "The crack is growing and there is another warning sign.")
    if watch:
        return _dispatch("V2", f"Warning sign reported: {ESCALATORS[watch[0]]}.")
    if not _known(crack_confidence) or crack_confidence < CONFIDENCE_THRESHOLD:
        return _dispatch("V2", "The app is not sure what it sees: a field worker will look.")
    if not width_known:
        return _dispatch("V2", "No scale in the photo, so the width is unknown: a field worker will measure it.")
    if width_upper_mm >= VISIT_WIDTH_MM:
        return _dispatch("V2", f"The crack may be {width_upper_mm:.1f} mm wide or more: a field worker will measure it.")
    if building_flags >= BUILDING_FLAGS_FOR_VISIT:
        return _dispatch("V2", "Hairline crack, but the building has two or more risk flags.")
    return _dispatch("V3", "Hairline crack, no warning sign, few building risk flags: it can wait for a recheck.")


def audit(report_id: str) -> bool:
    """About 1 V3 report in AUDIT_ONE_IN is visited anyway, always the same ones (fixed hash of the report ID)."""
    return int(hashlib.sha256(report_id.encode("utf-8")).hexdigest(), 16) % AUDIT_ONE_IN == 0
