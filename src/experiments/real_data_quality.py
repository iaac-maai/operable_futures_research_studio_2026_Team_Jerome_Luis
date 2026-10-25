"""First test on real data: quality-gate image checks on samples of public crack datasets.

Spec: spec/features/quality_gate.md. Usage, from the repository root:
    py src/experiments/real_data_quality.py data/raw/crack-seg data/raw/sdnet2018 --per-group 200
Recognised layouts (a root with no images is skipped):
- SDNET2018: <surface>/<C|U><surface letter>/*.jpg (e.g. D/CD, W/UW)
- METU: Positive/*.jpg (crack) and Negative/*.jpg (no crack)
- YOLO style (Ultralytics crack-seg, Darbhanga): an "images" folder with a sibling "labels" folder.
  A non-empty label file means crack, a missing or empty one no crack; no labels folder means unlabelled.
Writes per-image results to data/processed/ (ignored) and a histogram to figures/.
"""

import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality.gate import MAX_BRIGHTNESS, MIN_BRIGHTNESS, MIN_SHARPNESS, check, to_grey

SDNET_SURFACES = {"D": "bridge deck", "W": "wall", "P": "pavement"}
DATASET_NAMES = {"crack-seg": "crack-seg (roads, walls)", "darbhanga": "Darbhanga (brick masonry)",
                 "metu": "METU (building concrete)",
                 "strathclyde-brickwork": "Strathclyde (brick facades)"}
ROOT = Path(__file__).resolve().parents[2]


def yolo_label(path: Path) -> str | None:
    """crack / no crack from a YOLO label file next to an 'images' folder; None if there is no 'images' folder."""
    parts = list(path.parts)
    if "images" not in parts:
        return None
    i = len(parts) - 1 - parts[::-1].index("images")
    label_dir = Path(*parts[:i], "labels", *parts[i + 1:-1])
    if not label_dir.is_dir():
        return "unlabelled"
    label = label_dir / (path.stem + ".txt")
    return "crack" if label.is_file() and label.read_text().strip() else "no crack"


def find_images(root: Path) -> dict[tuple[str, str], list[Path]]:
    """Group images by (dataset group, crack / no crack / unlabelled) from the folder layout."""
    groups = defaultdict(list)
    for path in root.rglob("*.jp*g"):
        name = path.parent.name.upper()
        if len(name) == 2 and name[0] in "CU" and name[1] in SDNET_SURFACES:
            groups[(f"SDNET2018 {SDNET_SURFACES[name[1]]}", "crack" if name[0] == "C" else "no crack")].append(path)
        elif name in ("POSITIVE", "NEGATIVE"):  # METU layout
            groups[(DATASET_NAMES.get(root.name, root.name), "crack" if name == "POSITIVE" else "no crack")].append(path)
        else:
            groups[(DATASET_NAMES.get(root.name, root.name), yolo_label(path) or "unlabelled")].append(path)
    return dict(groups)


def run(roots: list[Path], per_group: int, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for root in roots:
        for (group, label), paths in sorted(find_images(root).items()):
            for path in rng.sample(sorted(paths), min(per_group, len(paths))):
                r = check(to_grey(path), coin_visible=True)  # coin check not implemented; these sets have no coin
                rows.append({"file": str(path.relative_to(root)), "group": group, "label": label,
                             "sharpness": round(r.sharpness, 1), "brightness": round(r.brightness, 1),
                             "image_ok": r.image_ok, "failed": ";".join(r.failed)})
    return rows


def summary(rows: list[dict]) -> str:
    groups = defaultdict(list)
    for r in rows:
        groups[(r["group"], r["label"])].append(r)
    lines = ["| Group | Label | n | Pass rate | Median sharpness | Median brightness | Main failure |",
             "|---|---|---|---|---|---|---|"]
    for (group, label), rs in sorted(groups.items()):
        fails = defaultdict(int)
        for r in rs:
            for f in filter(None, r["failed"].split(";")):
                fails[f] += 1
        main = max(fails, key=fails.get) if fails else "-"
        med = lambda k: sorted(r[k] for r in rs)[len(rs) // 2]
        lines.append(f"| {group} | {label} | {len(rs)} | {sum(r['image_ok'] for r in rs) / len(rs):.0%} "
                     f"| {med('sharpness')} | {med('brightness')} | {main} |")
    return "\n".join(lines)


def histogram(rows: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    from viz.figures import BLUE, GRID, INK_2, LEVEL

    groups = sorted({r["group"] for r in rows})
    cols = min(3, len(groups))
    nrows = -(-len(groups) // cols)
    fig, axes = plt.subplots(nrows, cols, figsize=(max(11, 4.4 * cols), 3.3 * nrows + 1.6), squeeze=False)
    for ax in axes.flat[len(groups):]:
        ax.set_axis_off()
    bins = np.logspace(0, 4.5, 37)
    for ax, group in zip(axes.flat, groups):
        for label, colour in (("crack", BLUE), ("no crack", "#eb6834"), ("unlabelled", "#1baf7a")):
            vals = [max(r["sharpness"], 1) for r in rows if r["group"] == group and r["label"] == label]
            if vals:
                ax.hist(vals, bins=bins, histtype="step", lw=2, color=colour, label=label)
        ax.legend(frameon=False, fontsize=8.5, loc="upper right")
        ax.axvline(MIN_SHARPNESS, color=LEVEL["High"], lw=1.2)
        ax.set_xscale("log")
        ax.set_title(group, loc="left", fontsize=10.5, weight="bold")
        ax.set_xlabel("Sharpness (Laplacian variance, log)")
        ax.grid(axis="y", color=GRID, lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0][0].text(MIN_SHARPNESS * 1.12, 0.97, "blur limit\n(illustrative)", transform=axes[0][0].get_xaxis_transform(),
                    va="top", fontsize=8, color=INK_2)
    for row in axes:
        row[0].set_ylabel("Images")
    fig.suptitle("Quality gate on real images: public dataset samples", x=0.02, ha="left", fontsize=14, weight="bold")
    top = 1 - 1.3 / (3.3 * nrows + 1.6)
    fig.text(0.02, top + 0.02, f"Images left of the red line would be asked to retake. Brightness limits "
             f"{MIN_BRIGHTNESS:g} to {MAX_BRIGHTNESS:g}.\nNot phone photos: tests the code, does not calibrate "
             "thresholds.", fontsize=9.5, color=INK_2, va="bottom")
    fig.subplots_adjust(left=0.07, right=0.98, top=top - 0.04, bottom=0.08, wspace=0.18, hspace=0.55)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main(argv=None) -> list[dict]:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("roots", type=Path, nargs="+")
    p.add_argument("--per-group", type=int, default=200)
    p.add_argument("--out", type=Path, default=ROOT / "data" / "processed" / "real_data_quality.csv")
    p.add_argument("--figure", type=Path, default=ROOT / "figures" / "08_real_data_quality_gate.png")
    args = p.parse_args(argv)
    rows = run(args.roots, args.per_group)
    if not rows:
        sys.exit(f"No images found under {', '.join(map(str, args.roots))}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    histogram(rows, args.figure)
    print(summary(rows))
    return rows


if __name__ == "__main__":
    main()
