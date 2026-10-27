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
