import pytest

pytest.importorskip("matplotlib")

from viz.figures import FIGURES, main


def test_all_figures_render(tmp_path):
    paths = main(tmp_path)
    assert [p.name for p in paths] == list(FIGURES)
    assert all(p.stat().st_size > 10_000 for p in paths)
