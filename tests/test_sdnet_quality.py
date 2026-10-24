import numpy as np
from PIL import Image

from experiments.sdnet_quality import find_images, main


def _fake_sdnet(root):
    """Tiny folder in the SDNET2018 layout with synthetic images (not real data)."""
    rng = np.random.default_rng(0)
    for surface in "DWP":
        for kind in "CU":
            d = root / surface / f"{kind}{surface}"
            d.mkdir(parents=True)
            for i in range(3):
                Image.fromarray(rng.integers(60, 200, (64, 64), dtype=np.uint8)).save(d / f"{i}.jpg")
    (root / "README.txt").write_text("ignored")


def test_find_images_groups_by_folder(tmp_path):
    _fake_sdnet(tmp_path)
    groups = find_images(tmp_path)
    assert len(groups) == 6
    assert len(groups[("wall", "crack")]) == 3


def test_main_writes_csv_and_figure(tmp_path):
    _fake_sdnet(tmp_path / "sdnet")
    out, fig = tmp_path / "out.csv", tmp_path / "fig.png"
    rows = main([str(tmp_path / "sdnet"), "--per-group", "2", "--out", str(out), "--figure", str(fig)])
    assert len(rows) == 12
    assert out.exists() and fig.exists()
