"""First test on real data: quality-gate image checks on samples of public crack datasets.

Spec: spec/features/quality_gate.md. Usage, from the repository root:
    py src/experiments/real_data_quality.py data/raw/crack-seg data/raw/sdnet2018 --per-group 200
Recognised layouts (a root with no images is skipped):
- SDNET2018: <surface>/<C|U><surface letter>/*.jpg (e.g. D/CD, W/UW)
- METU: Positive/*.jpg (crack) and Negative/*.jpg (no crack)
- Haiti 2010 database: Photos/<building>/...; each photo takes its building's engineer rating from the
  database CSV (worse of RC and masonry-wall damage); photos outside a building folder are "not linked"
- PHI-Net as written by phinet_prepare.py: <task>/X_<split>.npy (uint8 RGB) with y_<split>.npy and README.txt;
  tasks 3 (spalling), 6 (components, no damage label) and 8 (damaged / undamaged) are checked
- YOLO style (Ultralytics crack-seg, Darbhanga): an "images" folder with a sibling "labels" folder.
  A non-empty label file means crack, a missing or empty one no crack; no labels folder means unlabelled.
Writes per-image results to data/processed/ (ignored) and a histogram to figures/.
"""

import argparse
import csv
import random
import re
import sys
import numpy as np
from collections import defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.phinet_prepare import class_names
from quality.gate import MAX_BRIGHTNESS, MIN_BRIGHTNESS, MIN_SHARPNESS, check, to_grey

SDNET_SURFACES = {"D": "bridge deck", "W": "wall", "P": "pavement"}
DATASET_NAMES = {"crack-seg": "crack-seg (roads, walls)", "darbhanga": "Darbhanga (brick masonry)",
                 "metu": "METU (building concrete)",
                 "strathclyde-brickwork": "Strathclyde (brick facades)", "haiti2010": "Haiti 2010 (engineer survey)",
                 "nepal2015": "Nepal 2015 (engineer survey)"}
# Panel order: fit to the concept, best first (docs/data_map.md, section 0).
FIT_ORDER = [("Haiti 2010 (engineer survey)", "high"), ("Nepal 2015 (engineer survey)", "high"),
             ("Darbhanga (brick masonry)", "medium"), ("Strathclyde (brick facades)", "medium"),
             ("PHI-Net t8 damage type", "medium"), ("PHI-Net t3 spalling", "medium"),
             ("PHI-Net t6 components", "medium"), ("METU (building concrete)", "low"), ("SDNET2018 wall", "low"), ("crack-seg (roads, walls)", "low"),
             ("SDNET2018 pavement", "off-concept"), ("SDNET2018 bridge deck", "off-concept")]
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


HAITI_CSV = "NEES_Database__The_Haiti_Earthquake_Database.csv"
DAMAGE_ORDER = ["light", "moderate", "severe"]


def _building_key(name: str) -> str:
    return re.sub(r"\(.*?\)|[^A-Z0-9]", "", name.upper())


def haiti_ratings(root: Path) -> dict[str, str]:
    """Building key -> worse of RC and masonry-wall damage, from the Haiti database CSV."""
    ratings = {}
    with (root / HAITI_CSV).open(encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f):
            building = (row.get("BuildingNumber") or "").strip()
            levels = [(row.get(k) or "").strip().lower() for k in ("RC Damage", "MW Damage")]
            levels = [lv for lv in levels if lv in DAMAGE_ORDER]
            if building and levels:
                ratings[_building_key(building)] = max(levels, key=DAMAGE_ORDER.index)
    return ratings


# PHI-Net task folder -> (group, label for each class name; None means no damage label)
PHINET = {"task3_spalling_condition": ("PHI-Net t3 spalling", {"Spalling": "spalling", "Non-spalling": "no spalling"}),
          "task6_component_type": ("PHI-Net t6 components", None),
          "task8_damage_type": ("PHI-Net t8 damage type", {"Undamaged state": "undamaged"})}


def phinet_images(root: Path) -> dict[tuple[str, str], list[tuple[Path, int]]]:
    """(npy file, row) per image of the PHI-Net tasks in PHINET; damage types other than undamaged are 'damaged'."""
    groups = defaultdict(list)
    for task, (group, labels) in PHINET.items():
        names = class_names((root / task / "README.txt").read_text(encoding="utf-8", errors="replace"))             if (root / task / "README.txt").is_file() else {}
        for x in sorted((root / task).glob("X_*.npy")):
            y = np.load(x.with_name("y_" + x.name[2:]), allow_pickle=False)
            for i, c in enumerate(y.tolist()):
                label = "unlabelled" if labels is None else labels.get(names.get(c, ""), "damaged")
                groups[(group, label)].append((x, i))
    return dict(groups)


def load_grey(item: Path | tuple[Path, int]) -> np.ndarray:
    """Grey image from a file, or from row i of a uint8 RGB npy array (PIL's L weights)."""
    if isinstance(item, Path):
        return to_grey(item)
    rgb = np.load(item[0], mmap_mode="r", allow_pickle=False)[item[1]].astype(np.float64)
    return rgb @ np.array([0.299, 0.587, 0.114])


def item_name(item: Path | tuple[Path, int], root: Path) -> str:
    return str(item.relative_to(root)) if isinstance(item, Path) else f"{item[0].relative_to(root)}#{item[1]}"


def find_images(root: Path) -> dict[tuple[str, str], list[Path]]:
    """Group images by (dataset group, crack / no crack / unlabelled) from the folder layout."""
    if any((root / task).is_dir() for task in PHINET):
        return phinet_images(root)
    groups = defaultdict(list)
    ratings = haiti_ratings(root) if (root / HAITI_CSV).is_file() else None
    for path in root.rglob("*.jp*g"):
        if ratings is not None:
            parts = path.relative_to(root).parts
            rating = ratings.get(_building_key(parts[1])) if len(parts) > 2 and parts[0] == "Photos" else None
            label = f"engineer: {rating}" if rating else "not linked to a building"
            groups[(DATASET_NAMES.get(root.name, root.name), label)].append(path)
            continue
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
                row = {"file": item_name(path, root), "group": group, "label": label}
                try:
                    r = check(load_grey(path), scale_visible=True)  # scale check not implemented; these sets have no scale card
                except (OSError, ValueError):  # a broken file is a retake, not a crash
                    rows.append({**row, "sharpness": 0.0, "brightness": 0.0, "image_ok": False,
                                 "failed": "unreadable file"})
                    continue
                rows.append({**row, "sharpness": round(r.sharpness, 1), "brightness": round(r.brightness, 1),
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

    rank = {g: i for i, (g, _) in enumerate(FIT_ORDER)}
    fit = dict(FIT_ORDER)
    groups = sorted({r["group"] for r in rows}, key=lambda g: (rank.get(g, len(rank)), g))
    cols = min(4, len(groups))  # landscape; panels keep their order, read left to right
    nrows = -(-len(groups) // cols)
    height = max(3.6 * nrows + 1.9, 0.5625 * 5.2 * cols)  # at least 16:9
    fig, axes = plt.subplots(nrows, cols, figsize=(5.2 * cols, height), squeeze=False)
    for ax in axes.flat[len(groups):]:
        ax.set_axis_off()
    bins = np.logspace(0, 4.5, 37)
    for ax, group in zip(axes.flat, groups):
        for label, colour in (("crack", BLUE), ("no crack", "#eb6834"), ("unlabelled", "#1baf7a"),
                              ("engineer: light", "#86b6ef"), ("engineer: moderate", "#3987e5"),
                              ("engineer: severe", "#184f95"), ("not linked to a building", "#898781"),
                              ("damaged", BLUE), ("undamaged", "#eb6834"), ("spalling", BLUE),
                              ("no spalling", "#eb6834")):
            vals = [max(r["sharpness"], 1) for r in rows if r["group"] == group and r["label"] == label]
            if vals:
                ax.hist(vals, bins=bins, histtype="step", lw=2, color=colour, label=label)
        ax.legend(frameon=False, fontsize=8.5, loc="upper right")
        ax.axvline(MIN_SHARPNESS, color=LEVEL["Category 3"], lw=1.2)
        ax.set_xscale("log")
        members = [r for r in rows if r["group"] == group]
        accepted = sum(r["image_ok"] for r in members) / len(members)
        ax.set_title(f"{groups.index(group) + 1} · {group}", loc="left", fontsize=10.5, weight="bold", pad=18)
        ax.text(0, 1.02, f"fit to concept: {fit.get(group, 'not ranked')}  ·  {accepted:.0%} accepted",
                transform=ax.transAxes, fontsize=8.5, color=INK_2, va="bottom")
        ax.set_xlabel("Sharpness (Laplacian variance, log)")
        ax.grid(axis="y", color=GRID, lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0][0].text(MIN_SHARPNESS / 1.12, 0.97, "blur limit\n(illustrative)", transform=axes[0][0].get_xaxis_transform(),
                    va="top", ha="right", fontsize=8, color=INK_2)
    for row in axes:
        row[0].set_ylabel("Images")
    width = 5.2 * cols  # title as in the other figures: bold capitals, 38 pt on a 24 in figure
    fig.text(0.02, 1 - 0.6 / height, "QUALITY GATE ON REAL IMAGES", fontsize=38 * width / 24, weight="bold",
             color="#111111", va="center")
    fig.text(0.985, 1 - 0.6 / height, "08", fontsize=40 * width / 24, weight="bold", color="#111111", va="center",
             ha="right")
    top = 1 - 1.75 / height
    fig.text(0.02, top + 0.015, f"Public dataset samples. Panels ordered by fit to our concept, best first (docs/data_map.md). "
             f"Images left of the red line would be asked to retake. Brightness limits "
             f"{MIN_BRIGHTNESS:g} to {MAX_BRIGHTNESS:g}.\nNot phone photos: tests the code, does not calibrate "
             "thresholds. PHI-Net images are 224 px crops, measured as they are (never scaled up).", fontsize=11, color=INK_2, va="bottom")
    fig.subplots_adjust(left=0.05, right=0.985, top=top - 0.05, bottom=0.07, wspace=0.16, hspace=0.62)
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
