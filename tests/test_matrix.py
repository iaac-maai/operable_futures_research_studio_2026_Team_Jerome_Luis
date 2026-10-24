from triage.matrix import triage


def test_bad_photo_asks_for_retake():
    assert triage("wall_vertical", 1.0, 0.99, image_ok=False) == "Retake"


def test_low_confidence_is_never_low():
    assert triage("plaster_crazing", 0.1, 0.5, image_ok=True) == "Expert needed"


def test_unknown_pattern_goes_to_expert():
    assert triage("unknown", 1.0, 0.99, image_ok=True) == "Expert needed"


def test_diagonal_crack_over_1mm_is_high():
    assert triage("diagonal_step", 1.5, 0.9, image_ok=True) == "High"


def test_fine_plaster_crazing_is_low():
    assert triage("plaster_crazing", 0.2, 0.9, image_ok=True) == "Low"
