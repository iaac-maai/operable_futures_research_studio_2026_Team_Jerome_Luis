import zipfile

import numpy as np

from experiments.phinet_prepare import MEAN_BGR, class_names, prepare, to_uint8_rgb


def test_class_names_from_readme():
    readme = "# Label Registration Information\n\t0: Combined damage    (COMB)\n\t1: Flexural damage    (FLEX)\n"
    assert class_names(readme) == {0: "Combined damage", 1: "Flexural damage"}


def test_undo_vgg_preprocessing_is_lossless():
    rgb = np.random.default_rng(0).integers(0, 256, (2, 4, 4, 3), dtype=np.uint8)
    stored = rgb[..., ::-1].astype(np.float32) - MEAN_BGR  # how PHI-Net stores it
    assert np.array_equal(to_uint8_rgb(stored), rgb)


def test_prepare_writes_uint8_arrays_and_labels(tmp_path):
    rgb = np.random.default_rng(1).integers(0, 256, (6, 8, 8, 3), dtype=np.uint8)
    x = rgb[..., ::-1].astype(np.float32) - MEAN_BGR
    y = np.eye(2)[[0, 1, 0, 1, 1, 0]]
    zips = tmp_path / "zips"
    zips.mkdir()
    with zipfile.ZipFile(zips / "task9_test_task.zip", "w") as z:
        for name, arr in [("task9/task9_X_train.npy", x), ("task9/task9_y_train.npy", y)]:
            path = tmp_path / name.split("/")[1]
            np.save(path, arr)
            z.write(path, name)
        z.writestr("task9/README.txt", "\t0: Alpha (A)\n\t1: Beta (B)\n")
    (zips / "task1_still_downloading.zip").write_bytes(b"PK\x03\x04 partial")
    rows = prepare(zips, tmp_path / "out")
    assert len(rows) == 1
    out = tmp_path / "out" / "task9_test_task"
    assert np.array_equal(np.load(out / "X_train.npy"), rgb)
    assert np.load(out / "y_train.npy").tolist() == [0, 1, 0, 1, 1, 0]
    assert rows[0]["classes"] == {"Alpha": 3, "Beta": 3}
    assert (tmp_path / "out" / "samples" / "task9_test_task_train.png").exists()


def test_prepare_joins_a_task_split_over_two_zips(tmp_path):
    rgb = np.random.default_rng(2).integers(0, 256, (4, 8, 8, 3), dtype=np.uint8)
    zips = tmp_path / "zips"
    zips.mkdir()
    np.save(tmp_path / "x.npy", rgb[..., ::-1].astype(np.float32) - MEAN_BGR)
    np.save(tmp_path / "y.npy", np.eye(3)[[2, 0, 1, 2]])
    with zipfile.ZipFile(zips / "task1_scene_1.zip", "w") as z:  # labels and README in part 1
        z.write(tmp_path / "y.npy", "task1_y_train.npy")
        z.writestr("README.txt", "\t0: Object level (O)\n\t1: Pixel level (P)\n\t2: Structural level (S)\n")
    with zipfile.ZipFile(zips / "task1_scene_2.zip", "w") as z:  # images in part 2
        z.write(tmp_path / "x.npy", "task1_X_train.npy")
    rows = prepare(zips, tmp_path / "out")
    assert [r["zip"] for r in rows] == ["task1_scene"]
    assert rows[0]["classes"] == {"Object level": 1, "Pixel level": 1, "Structural level": 2}
    assert np.array_equal(np.load(tmp_path / "out" / "task1_scene" / "X_train.npy"), rgb)
