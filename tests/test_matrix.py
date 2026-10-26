import itertools
import math

import pytest

from triage.matrix import CONFIDENCE_THRESHOLD, MATRIX, PATTERNS, assess, triage, width_band


def test_bad_photo_asks_for_retake():
    assert triage("wall_vertical", 1.0, 0.99, image_ok=False) == "Retake"


def test_low_confidence_is_never_low():
    assert triage("plaster_crazing", 0.1, 0.5, image_ok=True) == "Expert needed"


def test_unknown_pattern_goes_to_expert():
    assert triage("unknown", 1.0, 0.99, image_ok=True) == "Expert needed"


def test_diagonal_crack_over_1mm_is_high():
    assert triage("diagonal", 1.5, 0.9, image_ok=True) == "High"


def test_fine_plaster_crazing_is_low():
    assert triage("plaster_crazing", 0.2, 0.9, image_ok=True) == "Low"


@pytest.mark.parametrize("confidence", [math.nan, math.inf, -0.1, 1.5, None, "0.9", True])
def test_invalid_confidence_goes_to_expert(confidence):
    assert triage("plaster_crazing", 0.1, confidence, image_ok=True) == "Expert needed"


@pytest.mark.parametrize("width", [math.nan, math.inf, -5, None, "0.1"])
def test_invalid_width_goes_to_expert(width):
    assert triage("plaster_crazing", width, 0.9, image_ok=True) == "Expert needed"


@pytest.mark.parametrize("image_ok", [None, 1, "yes"])
def test_image_ok_must_be_true(image_ok):
    assert triage("plaster_crazing", 0.1, 0.9, image_ok=image_ok) == "Retake"


def test_threshold_cannot_be_lowered_by_caller():
    with pytest.raises(TypeError):
        triage("plaster_crazing", 0.1, 0.01, image_ok=True, threshold=0)


@pytest.mark.parametrize("width, band", [(0.0, "under_0.3"), (0.3, "0.3_to_1"), (1.0, "1_to_3"), (3.0, "over_3")])
def test_boundary_goes_to_wider_band(width, band):
    assert width_band(width) == band


def test_low_is_earned():
    """Low only when image usable, confidence at or over threshold and the matrix says Low."""
    widths = [0, 0.1, 0.3, 0.5, 1, 2, 3, 10, -1, math.nan]
    confidences = [0, 0.5, CONFIDENCE_THRESHOLD - 0.01, CONFIDENCE_THRESHOLD, 0.95, 1, math.nan]
    for pattern, width, conf, ok in itertools.product(PATTERNS + ["unknown"], widths, confidences, [True, False]):
        if triage(pattern, width, conf, ok) == "Low":
            assert ok and conf >= CONFIDENCE_THRESHOLD and width >= 0
            assert MATRIX[width_band(width)][PATTERNS.index(pattern)] == "Low"


@pytest.mark.parametrize("args", [("column_or_beam", 2, 0.9, True), ("unknown", 1, 0.9, True), ("wall_vertical", 1, 0.1, True)])
def test_high_and_referrals_need_engineer(args):
    result = assess(*args)
    assert result.level in {"High", "Expert needed"}
    assert result.engineer_review


@pytest.mark.parametrize("args", [("plaster_crazing", 0.1, 0.9, True), ("wall_vertical", 0.5, 0.9, True), ("wall_vertical", 0.5, 0.9, False)])
def test_low_medium_retake_do_not_flag_engineer(args):
    assert not assess(*args).engineer_review


def test_every_result_has_a_reason_and_no_safe_claim():
    result = assess("diagonal", 1.5, 0.9, True)
    assert result.reason == "diagonal (shear) crack, 1.5 mm wide (1 to 3 mm band): High."
    for pattern, width in itertools.product(PATTERNS, [0.1, 0.5, 2, 5]):
        assert "safe" not in assess(pattern, width, 0.9, True).reason.lower()


@pytest.mark.parametrize("material", ["brick", "stone", "unknown", ""])
def test_unsupported_material_goes_to_expert(material):
    result = assess("plaster_crazing", 0.1, 0.99, True, material=material, material_confidence=0.95)
    assert result.level == "Expert needed" and result.engineer_review
    assert "Material not supported" in result.reason


@pytest.mark.parametrize("material_confidence", [0.5, 0.79, math.nan, -1, 1.2, None])
def test_unsure_material_goes_to_expert(material_confidence):
    result = assess("plaster_crazing", 0.1, 0.99, True, material="concrete", material_confidence=material_confidence)
    assert result.level == "Expert needed" and "Material unclear" in result.reason


def test_confident_concrete_reaches_the_matrix():
    assert triage("plaster_crazing", 0.1, 0.99, True, material="concrete", material_confidence=0.9) == "Low"


def test_bad_photo_is_retake_before_material_check():
    assert triage("plaster_crazing", 0.1, 0.99, False, material="brick", material_confidence=0.2) == "Retake"
