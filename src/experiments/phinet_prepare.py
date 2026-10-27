"""Prepare PHI-Net task zips for viewing and training. Spec: docs/data_map.md (PHI-Net) [53][55].

Usage, from the repository root:
    py -I src/experiments/phinet_prepare.py data/raw/phinet/zips data/raw/phinet
For every task zip it writes data/raw/phinet/<task>/: X_<split>.npy as uint8 RGB (the zips store float32 BGR with the
ImageNet mean subtracted, VGG style; undoing it is lossless after rounding), y_<split>.npy as class numbers,
README.txt and license.txt, and figures-free sample sheets in data/raw/phinet/samples/ (PHI-Net is CC BY-NC-SA 4.0:
the sheets stay in data/, never in the repository).
"""

import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

MEAN_BGR = np.array([103.939, 116.779, 123.68], dtype=np.float32)
CHUNK = 256


def class_names(readme: str) -> dict[int, str]:
    """'0: Combined damage (COMB)' lines -> {0: 'Combined damage'}."""
    return {int(n): name.strip() for n, name in re.findall(r"^\s*(\d+)\s*:\s*([^(\n]+)", readme, flags=re.M)}


def to_uint8_rgb(x: np.ndarray) -> np.ndarray:
    """Undo VGG preprocessing: add the BGR mean back, BGR -> RGB, round to uint8."""
    return np.clip(np.rint(x.astype(np.float32) + MEAN_BGR), 0, 255).astype(np.uint8)[..., ::-1]


def convert_member(z: zipfile.ZipFile, member: str, tmp: Path, out: Path) -> tuple:
    z.extract(member, tmp)
    src = np.load(tmp / member, mmap_mode="r", allow_pickle=False)
    dst = np.lib.format.open_memmap(out, mode="w+", dtype=np.uint8, shape=src.shape)
    for i in range(0, len(src), CHUNK):
        dst[i:i + CHUNK] = to_uint8_rgb(np.asarray(src[i:i + CHUNK]))
    dst.flush()
    shape = src.shape
    del src, dst
    (tmp / member).unlink()
    return shape


def sample_sheet(x: np.ndarray, y: np.ndarray, names: dict[int, str], path: Path, per_class: int = 6) -> None:
    rng = np.random.default_rng(0)
    classes = sorted(set(y.tolist()))
    size, pad, head = 160, 6, 22
    sheet = Image.new("RGB", (190 + per_class * (size + pad), len(classes) * (size + pad + head)), "white")
    draw = ImageDraw.Draw(sheet)
    for r, c in enumerate(classes):
        idx = np.flatnonzero(y == c)
        pick = rng.choice(idx, min(per_class, len(idx)), replace=False)
        y0 = r * (size + pad + head)
        draw.text((6, y0 + 4), f"{c}: {names.get(c, '?')} (n={len(idx)})", fill="black")
        for k, i in enumerate(pick):
            sheet.paste(Image.fromarray(x[i]).resize((size, size)), (190 + k * (size + pad), y0 + head))
    sheet.save(path)


def prepare(zips: Path, out: Path) -> list[dict]:
    rows = []
    (out / "samples").mkdir(parents=True, exist_ok=True)
    tmp = out / "_tmp"
    for zpath in sorted(zips.glob("task*.zip")):
        try:
            z = zipfile.ZipFile(zpath)
        except zipfile.BadZipFile:
            print(zpath.stem, "incomplete or broken zip, skipped", flush=True)
            continue
        names = z.namelist()
        task = re.match(r"(task\d+)", zpath.stem).group(1)
        dest = out / zpath.stem
        dest.mkdir(parents=True, exist_ok=True)
        readme = next((n for n in names if n.lower().endswith("readme.txt")), None)
        text = z.read(readme).decode("utf-8", "replace") if readme else ""
        labels = class_names(text)
        for n in names:
            if n.lower().endswith(("readme.txt", "license.txt")):
                (dest / Path(n).name).write_bytes(z.read(n))
        for member in sorted(n for n in names if re.search(r"_X_\w+\.npy$", n)):
            split = re.search(r"_X_(\w+)\.npy$", member).group(1)
            x_out = dest / f"X_{split}.npy"
            shape = np.load(x_out, mmap_mode="r").shape if x_out.exists() else convert_member(z, member, tmp, x_out)
            y_member = member.replace("_X_", "_y_")
            y = np.load(z.open(y_member), allow_pickle=False)
            y = y.argmax(axis=1) if y.ndim == 2 else y.ravel()
            np.save(dest / f"y_{split}.npy", y.astype(np.int64))
            x = np.load(x_out, mmap_mode="r")
            sample_sheet(x, y, labels, out / "samples" / f"{zpath.stem}_{split}.png")
            counts = {labels.get(int(k), str(k)): int((y == k).sum()) for k in sorted(set(y.tolist()))}
            rows.append({"zip": zpath.stem, "task": task, "split": split, "n": int(shape[0]),
                         "size": f"{shape[1]}x{shape[2]}", "classes": counts})
            print(zpath.stem, split, shape, counts, flush=True)
    if tmp.exists():
        for p in sorted(tmp.rglob("*"), reverse=True):
            p.rmdir() if p.is_dir() else p.unlink()
        tmp.rmdir()
    return rows


if __name__ == "__main__":
    import json

    result = prepare(Path(sys.argv[1]), Path(sys.argv[2]))
    (Path(sys.argv[2]) / "summary.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
