import itertools
import math

import pytest

from triage.matrix import (CONFIDENCE_THRESHOLD, ELEMENTS, ESCALATORS, LEVELS, MATRIX, NEXT_STEPS, PATTERNS, VERSION,
                           assess, triage, width_band)


def test_bad_photo_asks_for_retake():
    assert triage("flexural", "beam", 1.0, 0.99, image_ok=False) == "Retake"


def test_low_confidence_is_never_low():
    assert triage("surface_map", "infill_wall", 0.1, 0.5, image_ok=True) == "Expert needed"


@pytest.mark.parametrize("pattern, element", [("unknown", "beam"), ("flexural", "roof"), ("flexural", "")])
def test_unknown_pattern_or_element_goes_to_expert(pattern, element):
    assert triage(pattern, element, 1.0, 0.99, image_ok=True) == "Expert needed"


@pytest.mark.parametrize("pattern, element", [("column_horizontal", "slab"), ("column_horizontal", "beam"),
                                              ("joint", "infill_wall"), ("joint", "slab")])
def test_pattern_not_allowed_on_element_goes_to_expert(pattern, element):
    result = assess(pattern, element, 0.5, 0.99, True)
    assert result.level == "Expert needed" and "does not fit" in result.reason


def test_diagonal_shear_crack_in_a_beam_over_0_3mm_is_high():
    assert triage("diagonal_shear", "beam", 0.5, 0.9, image_ok=True) == "Category 3"


def test_fine_surface_map_cracking_is_low():
    assert triage("surface_map", "infill_wall", 0.2, 0.9, image_ok=True) == "Category 1"


@pytest.mark.parametrize("confidence", [math.nan, math.inf, -0.1, 1.5, None, "0.9", True])
def test_invalid_confidence_goes_to_expert(confidence):
    assert triage("surface_map", "slab", 0.1, confidence, image_ok=True) == "Expert needed"


@pytest.mark.parametrize("width, uncertainty", [(math.nan, 0), (math.inf, 0), (-5, 0), (None, 0), ("0.1", 0),
                                                (0.1, -0.1), (0.1, math.nan), (0.1, None)])
def test_invalid_width_goes_to_expert(width, uncertainty):
    assert triage("surface_map", "slab", width, 0.9, True, width_uncertainty_mm=uncertainty) == "Expert needed"


@pytest.mark.parametrize("image_ok", [None, 1, "yes"])
def test_image_ok_must_be_true(image_ok):
    assert triage("surface_map", "slab", 0.1, 0.9, image_ok=image_ok) == "Retake"


def test_threshold_cannot_be_lowered_by_caller():
    with pytest.raises(TypeError):
        triage("surface_map", "slab", 0.1, 0.01, image_ok=True, threshold=0)


@pytest.mark.parametrize("width, band", [(0.0, "under_0.3"), (0.3, "0.3_to_1"), (1.0, "1_to_3"), (3.0, "over_3")])
def test_boundary_goes_to_wider_band(width, band):
    assert width_band(width) == band


def test_upper_bound_of_width_is_used():
    """0.2 mm measured, +/- 0.2 mm: could be 0.4 mm, so the 0.3 to 1 band applies."""
    assert triage("flexural", "beam", 0.2, 0.9, True) == "Category 1"
    result = assess("flexural", "beam", 0.2, 0.9, True, width_uncertainty_mm=0.2)
    assert result.level == "Category 2" and "up to 0.4 mm" in result.reason


def test_column_raises_one_level():
    assert triage("flexural", "beam", 0.5, 0.9, True) == "Category 2"
    assert triage("flexural", "column", 0.5, 0.9, True) == "Category 3"


@pytest.mark.parametrize("escalator", [e for e in ESCALATORS])
def test_every_escalator_raises_and_never_lowers(escalator):
    base = LEVELS.index(triage("surface_map", "infill_wall", 0.1, 0.9, True))
    raised = LEVELS.index(triage("surface_map", "infill_wall", 0.1, 0.9, True, escalators=(escalator,)))
    assert raised > base


@pytest.mark.parametrize("escalator", ["offset", "sagging"])
def test_offset_and_sagging_go_straight_to_high(escalator):
    result = assess("surface_map", "slab", 0.1, 0.9, True, escalators=(escalator,))
    assert result.level == "Category 3" and ESCALATORS[escalator] in result.reason


def test_escalators_stack_and_cap_at_high():
    assert triage("surface_map", "slab", 0.1, 0.9, True, escalators=("growing",)) == "Category 2"
    assert triage("surface_map", "slab", 0.1, 0.9, True, escalators=("growing", "rust_stain")) == "Category 3"
    assert triage("surface_map", "slab", 0.1, 0.9, True, escalators=("growing", "rust_stain", "recent_earthquake")) == "Category 3"


def test_repeated_escalator_counts_once():
    assert triage("surface_map", "slab", 0.1, 0.9, True, escalators=("growing", "growing")) == "Category 2"


def test_unknown_escalator_is_an_error_not_a_guess():
    with pytest.raises(ValueError):
        triage("surface_map", "slab", 0.1, 0.9, True, escalators=("looks fine",))


def test_low_is_earned():
    """Category 1 only when image usable, material concrete, confidence at or over threshold, no escalator,
    not a column, and the matrix says Category 1 for the upper bound of the width."""
    widths = [0, 0.1, 0.3, 0.5, 1, 2, 3, 10, -1, math.nan]
    confidences = [0, 0.5, CONFIDENCE_THRESHOLD - 0.01, CONFIDENCE_THRESHOLD, 0.95, 1, math.nan]
    for pattern, element, width, conf, ok in itertools.product(PATTERNS + ["unknown"], list(ELEMENTS) + ["roof"],
                                                                widths, confidences, [True, False]):
        if triage(pattern, element, width, conf, ok) == "Category 1":
            assert ok and conf >= CONFIDENCE_THRESHOLD and width >= 0 and element != "column"
            assert MATRIX[width_band(width)][PATTERNS.index(pattern)] == "Category 1"


@pytest.mark.parametrize("args", [("flexural", "beam", 2, 0.9, True), ("unknown", "beam", 1, 0.9, True),
                                  ("flexural", "beam", 1, 0.1, True)])
def test_high_and_referrals_need_engineer(args):
    result = assess(*args)
    assert result.level in {"Category 3", "Expert needed"}
    assert result.engineer_review


@pytest.mark.parametrize("args", [("surface_map", "slab", 0.1, 0.9, True), ("flexural", "beam", 0.5, 0.9, True),
                                  ("flexural", "beam", 0.5, 0.9, False)])
def test_low_medium_retake_do_not_flag_engineer(args):
    assert not assess(*args).engineer_review


def test_every_result_has_a_reason_a_next_step_and_no_safe_claim():
    result = assess("diagonal_shear", "beam", 1.5, 0.9, True, escalators=("rust_stain",), location="middle")
    assert result.reason == ("diagonal shear crack in a beam, 1.5 mm wide, 1 to 3 mm band: Category 3; "
                             "raised because rust staining along the crack.")
    assert result.next_step == NEXT_STEPS["Category 3"]
    for pattern, element, width in itertools.product(PATTERNS, ELEMENTS, [0.1, 0.5, 2, 5]):
        r = assess(pattern, element, width, 0.9, True)
        assert "safe" not in r.reason.lower() and r.next_step


def test_matrix_is_marked_illustrative():
    assert "illustrative" in VERSION


@pytest.mark.parametrize("material", ["brick", "stone", "unknown", ""])
def test_unsupported_material_goes_to_expert(material):
    result = assess("surface_map", "slab", 0.1, 0.99, True, material=material, material_confidence=0.95)
    assert result.level == "Expert needed" and result.engineer_review
    assert "Material not supported" in result.reason


@pytest.mark.parametrize("material_confidence", [0.5, 0.79, math.nan, -1, 1.2, None])
def test_unsure_material_goes_to_expert(material_confidence):
    result = assess("surface_map", "slab", 0.1, 0.99, True, material="concrete", material_confidence=material_confidence)
    assert result.level == "Expert needed" and "Material unclear" in result.reason


def test_confident_concrete_reaches_the_matrix():
    assert triage("surface_map", "slab", 0.1, 0.99, True, material="concrete", material_confidence=0.9) == "Category 1"


def test_bad_photo_is_retake_before_material_check():
    assert triage("surface_map", "slab", 0.1, 0.99, False, material="brick", material_confidence=0.2) == "Retake"


# matrix v3: location on the element and the new warning signs (spec/features/risk_matrix.md, D28)
def test_end_zone_raises_cracks_along_bars_and_diagonal_shear():
    assert triage("along_bar", "beam", 0.2, 0.9, True, location="middle") == "Category 2"
    assert triage("along_bar", "beam", 0.2, 0.9, True, location="end_zone") == "Category 3"
    assert triage("diagonal_shear", "slab", 0.1, 0.9, True, location="end_zone") == "Category 3"


def test_end_zone_does_not_raise_other_patterns():
    assert triage("flexural", "beam", 0.5, 0.9, True, location="end_zone") == "Category 2"
    assert triage("surface_map", "slab", 0.1, 0.9, True, location="end_zone") == "Category 1"


def test_unknown_location_counts_as_end_zone():
    result = assess("along_bar", "beam", 0.2, 0.9, True)
    assert result.level == "Category 3" and "location is unknown" in result.reason
    assert triage("along_bar", "beam", 0.2, 0.9, True, location="unknown") == "Category 3"


def test_unknown_location_name_is_an_error_not_a_guess():
    with pytest.raises(ValueError):
        triage("along_bar", "beam", 0.2, 0.9, True, location="near the window")


@pytest.mark.parametrize("sign", ["thin_cover", "crossing_bar_crack", "damp"])
def test_new_v3_signs_raise_one_level(sign):
    assert triage("flexural", "beam", 0.5, 0.9, True, escalators=(sign,)) == "Category 3"
    assert triage("surface_map", "slab", 0.1, 0.9, True, escalators=(sign,)) == "Category 2"


def test_every_location_and_sign_has_a_basis():
    from triage.matrix import BASIS, LOCATIONS
    for key in list(LOCATIONS) + list(ESCALATORS):
        assert BASIS[key].strip()


def test_assumptions_are_marked_as_assumptions():
    from triage.matrix import BASIS
    assert "assumption" in BASIS["damp"] and "assumption" in BASIS["end_zone"]
