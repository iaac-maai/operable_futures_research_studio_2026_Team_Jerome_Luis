"""First test on real data: quality-gate image checks on a sample of SDNET2018.

Spec: spec/features/quality_gate.md. Usage, from the repository root:
    py src/experiments/sdnet_quality.py data/raw/sdnet2018 --per-group 100
Expects the SDNET2018 layout: <surface>/<C|U><surface letter>/*.jpg (e.g. D/CD, W/UW).
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

SURFACES = {"D": "bridge deck", "W": "wall", "P": "pavement"}
ROOT = Path(__file__).resolve().parents[2]


def find_images(root: Path) -> dict[tuple[str, str], list[Path]]:
    """Group images by (surface, crack / no crack) from the folder name, e.g. CD = cracked deck."""
    groups = defaultdict(list)
    for path in root.rglob("*.jp*g"):
        name = path.parent.name.upper()
        if len(name) == 2 and name[0] in "CU" and name[1] in SURFACES:
            groups[(SURFACES[name[1]], "crack" if name[0] == "C" else "no crack")].append(path)
    return dict(groups)


def run(root: Path, per_group: int, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for (surface, label), paths in sorted(find_images(root).items()):
        for path in rng.sample(sorted(paths), min(per_group, len(paths))):
            r = check(to_grey(path), coin_visible=True)  # coin check not implemented; SDNET has no coin
            rows.append({"file": str(path.relative_to(root)), "surface": surface, "label": label,
                         "sharpness": round(r.sharpness, 1), "brightness": round(r.brightness, 1),
                         "image_ok": r.image_ok, "failed": ";".join(r.failed)})
    return rows


def summary(rows: list[dict]) -> str:
    groups = defaultdict(list)
    for r in rows:
        groups[(r["surface"], r["label"])].append(r)
    lines = ["| Surface | Label | n | Pass rate | Median sharpness | Median brightness | Main failure |",
             "|---|---|---|---|---|---|---|"]
    for (surface, label), rs in sorted(groups.items()):
        fails = defaultdict(int)
        for r in rs:
            for f in filter(None, r["failed"].split(";")):
                fails[f] += 1
        main = max(fails, key=fails.get) if fails else "-"
        med = lambda k: sorted(r[k] for r in rs)[len(rs) // 2]
        lines.append(f"| {surface} | {label} | {len(rs)} | {sum(r['image_ok'] for r in rs) / len(rs):.0%} "
                     f"| {med('sharpness')} | {med('brightness')} | {main} |")
    return "\n".join(lines)


def histogram(rows: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    from viz.figures import BLUE, GRID, INK_2, LEVEL

    surfaces = sorted({r["surface"] for r in rows})
    fig, axes = plt.subplots(1, len(surfaces), figsize=(4.2 * len(surfaces), 3.8), sharey=True, squeeze=False)
    bins = np.logspace(0, 4, 33)
    for ax, surface in zip(axes[0], surfaces):
        for label, colour in (("crack", BLUE), ("no crack", "#eb6834")):
            vals = [max(r["sharpness"], 1) for r in rows if r["surface"] == surface and r["label"] == label]
            ax.hist(vals, bins=bins, histtype="step", lw=2, color=colour, label=label)
        ax.axvline(MIN_SHARPNESS, color=LEVEL["High"], lw=1.2)
        ax.text(MIN_SHARPNESS * 1.1, ax.get_ylim()[1] * 0.92, "blur limit\n(illustrative)", fontsize=8, color=INK_2)
        ax.set_xscale("log")
        ax.set_title(surface, loc="left", fontsize=11, weight="bold")
        ax.set_xlabel("Sharpness (Laplacian variance, log scale)")
        ax.grid(axis="y", color=GRID, lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0][0].set_ylabel("Images")
    axes[0][-1].legend(frameon=False)
    fig.suptitle("Quality gate on real images: SDNET2018 sample", x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.87, f"Brightness limits {MIN_BRIGHTNESS:g} to {MAX_BRIGHTNESS:g}. "
             "Camera tiles, not phone photos: tests the code, does not calibrate thresholds.",
             fontsize=9.5, color=INK_2)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.76, bottom=0.17, wspace=0.08)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main(argv=None) -> list[dict]:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("root", type=Path)
    p.add_argument("--per-group", type=int, default=100)
    p.add_argument("--out", type=Path, default=ROOT / "data" / "processed" / "sdnet_quality.csv")
    p.add_argument("--figure", type=Path, default=ROOT / "figures" / "08_sdnet_quality_gate.png")
    args = p.parse_args(argv)
    rows = run(args.root, args.per_group)
    if not rows:
        sys.exit(f"No SDNET2018 images found under {args.root}")
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
