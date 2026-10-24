import numpy as np
from PIL import Image

from experiments.real_data_quality import find_images, main

rng = np.random.default_rng(0)


def _save(d, n):
    d.mkdir(parents=True)
    for i in range(n):
        Image.fromarray(rng.integers(60, 200, (64, 64), dtype=np.uint8)).save(d / f"{i}.jpg")


def _fake_sdnet(root):
    """Tiny folder in the SDNET2018 layout with synthetic images (not real data)."""
    for surface in "DWP":
        for kind in "CU":
            _save(root / surface / f"{kind}{surface}", 3)
    (root / "README.txt").write_text("ignored")


def _fake_crackseg(root):
    """Tiny folder in the Ultralytics crack-seg layout (not real data): images/<split>, labels/<split>."""
    for split in ("train", "val", "test"):
        _save(root / "images" / split, 2)
        (root / "labels" / split).mkdir(parents=True)
        (root / "labels" / split / "0.txt").write_text("0 0.1 0.1 0.2 0.2\n")
        (root / "labels" / split / "1.txt").write_text("")  # empty label: no crack


def _fake_darbhanga(root):
    """Darbhanga layout: <split>/images with <split>/labels, and a test folder without labels."""
    _save(root / "train" / "images", 2)
    (root / "train" / "labels").mkdir()
    (root / "train" / "labels" / "0.txt").write_text("0 0.5 0.5 0.2 0.2\n")  # 1.jpg has no label: no crack
    _save(root / "test", 2)


def test_find_images_sdnet(tmp_path):
    _fake_sdnet(tmp_path)
    groups = find_images(tmp_path)
    assert len(groups) == 6
    assert len(groups[("SDNET2018 wall", "crack")]) == 3


def test_find_images_crackseg(tmp_path):
    root = tmp_path / "crack-seg"
    _fake_crackseg(root)
    assert {k: len(v) for k, v in find_images(root).items()} == {
        ("crack-seg (roads, walls)", "crack"): 3, ("crack-seg (roads, walls)", "no crack"): 3}


def test_find_images_darbhanga(tmp_path):
    root = tmp_path / "darbhanga"
    _fake_darbhanga(root)
    assert {k[1]: len(v) for k, v in find_images(root).items()} == {"crack": 1, "no crack": 1, "unlabelled": 2}


def test_main_runs_both_and_skips_empty_roots(tmp_path):
    _fake_sdnet(tmp_path / "sdnet")
    _fake_crackseg(tmp_path / "crack-seg")
    (tmp_path / "empty").mkdir()
    out, fig = tmp_path / "out.csv", tmp_path / "fig.png"
    rows = main([str(tmp_path / "sdnet"), str(tmp_path / "crack-seg"), str(tmp_path / "empty"),
                 "--per-group", "2", "--out", str(out), "--figure", str(fig)])
    assert len(rows) == 6 * 2 + 2 * 2
    assert out.exists() and fig.exists()
