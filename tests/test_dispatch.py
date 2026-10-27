import math

import pytest

from triage.dispatch import NEXT_STEPS, audit, screen

HAIRLINE = dict(image_ok=True, crack_confidence=0.95, width_upper_mm=0.2)


@pytest.mark.parametrize("sign", ["offset", "sagging"])
def test_offset_or_sagging_is_urgent_even_with_a_bad_photo(sign):
    assert screen(False, 0.1, None, signs=[sign]).tier == "V1"


def test_bad_photo_asks_for_retake_then_sends_a_field_worker():
    assert screen(False, 0.95, 0.2).tier == "Retake"
    assert screen(False, 0.95, 0.2, retakes=1).tier == "Retake"
    assert screen(False, 0.95, 0.2, retakes=2).tier == "V2"


@pytest.mark.parametrize("width", [1.0, 2.5, 6.0])
def test_wide_crack_is_urgent(width):
    assert screen(True, 0.95, width).tier == "V1"


def test_growing_plus_another_sign_is_urgent():
    assert screen(**HAIRLINE, signs=["growing", "sticking_openings"]).tier == "V1"


@pytest.mark.parametrize("kwargs", [
    dict(HAIRLINE, signs=["growing"]),
    dict(HAIRLINE, signs=["rust_stain"]),
    dict(HAIRLINE, signs=["recent_earthquake"]),
    dict(HAIRLINE, signs=["damp"]),
    dict(HAIRLINE, signs=["thin_cover"]),
    dict(HAIRLINE, crack_confidence=0.5),
    dict(HAIRLINE, crack_confidence=math.nan),
    dict(HAIRLINE, width_upper_mm=None),
    dict(HAIRLINE, width_upper_mm=-1.0),
    dict(HAIRLINE, width_upper_mm=0.3),
    dict(HAIRLINE, building_flags=2),
])
def test_doubt_or_any_sign_means_a_visit_within_a_month(kwargs):
    assert screen(**kwargs).tier == "V2"


def test_only_a_confident_hairline_with_nothing_else_can_wait():
    d = screen(**HAIRLINE, building_flags=1)
    assert d.tier == "V3"
    assert "Category 1" not in d.next_step and "safe" not in d.next_step.lower()


def test_every_result_has_a_reason_and_a_next_step():
    for d in (screen(False, 0.9), screen(**HAIRLINE), screen(True, 0.9, 2.0), screen(True, 0.9, None)):
        assert d.reason and d.next_step == NEXT_STEPS[d.tier]


def test_unknown_sign_is_rejected():
    with pytest.raises(ValueError):
        screen(**HAIRLINE, signs=["looks_fine"])


def test_audit_picks_about_one_in_ten_and_always_the_same():
    picked = [audit(f"R{i:05d}") for i in range(5000)]
    assert 0.07 < sum(picked) / len(picked) < 0.13
    assert picked == [audit(f"R{i:05d}") for i in range(5000)]
