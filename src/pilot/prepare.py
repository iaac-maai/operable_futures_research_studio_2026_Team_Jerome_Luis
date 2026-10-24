"""Prepare pilot photos: strip all metadata (incl. GPS) and rename. Spec: spec/features/photo_protocol.md.

Usage, from the repository root:
    py src/pilot/prepare.py <folder with phone photos> data/pilot/photos
"""

import argparse
import csv
from pathlib import Path

from PIL import Image, ImageOps

EXTENSIONS = {".jpg", ".jpeg", ".png"}  # set iPhones to "Most compatible" (JPEG); HEIC is not read


def strip_and_save(src: Path, dst: Path) -> None:
    """Re-encode pixels only, so no EXIF, GPS or maker notes survive. Orientation is applied first."""
    with Image.open(src) as img:
        clean = ImageOps.exif_transpose(img).convert("RGB")
    Image.frombytes(clean.mode, clean.size, clean.tobytes()).save(dst, "JPEG", quality=95)


def prepare(src_dir: Path, out_dir: Path) -> list[tuple[str, str]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    photos = sorted(p for p in src_dir.iterdir() if p.suffix.lower() in EXTENSIONS)
    index = []
    for i, src in enumerate(photos, 1):
        name = f"P{i:04d}.jpg"
        strip_and_save(src, out_dir / name)
        index.append((name, src.name))
    with (out_dir.parent / "photo_index.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["photo_id", "original_name"])
        w.writerows((n[:-4], o) for n, o in index)
    return index


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("src", type=Path)
    p.add_argument("out", type=Path)
    args = p.parse_args()
    print(f"{len(prepare(args.src, args.out))} photos prepared in {args.out}")
