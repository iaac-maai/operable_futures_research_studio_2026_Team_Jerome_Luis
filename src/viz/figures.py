"""Figures for the 29 Oct deliverables. Spec: spec/features/figures.md.

Run from the repository root:  py src/viz/figures.py   (writes PNGs to figures/)
Every figure is drawn from the repo's own rules and data map. None shows a measured result.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from triage.matrix import (_ESCALATOR_EFFECT, BAND_NAMES, BANDS, ELEMENT_RAISE, ELEMENTS, ESCALATORS, MATRIX,
                           PATTERN_NAMES, PATTERNS, VERSION)

# Palette: reference instance of the dataviz skill (light mode).
SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, AQUA, VIOLET = "#2a78d6", "#1baf7a", "#6250d6"
SEQ = {"covered": "#1c5cab", "partial": "#5598e7", "planned": "#b7d3f6", "none": SURFACE}
# Status colours are reserved for triage levels, always with a text label.
LEVEL = {"Low": "#0ca30c", "Medium": "#fab219", "High": "#d03b3b", "Expert needed": "#ec835a", "Retake": MUTED}
ON_FILL = {"Medium": INK}  # dark text on the yellow fill, white elsewhere

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "text.color": INK,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def _box(ax, x, y, w, h, text, fill, edge, size=9.5, color=INK, weight="normal", lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=fill, edgecolor=edge, linewidth=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color,
            weight=weight, wrap=True)


def _arrow(ax, start, end, label=None, label_offset=(0, 0.12)):
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="-|>", color=INK_2, lw=1.2,
                                                          shrinkA=0, shrinkB=0))
    if label:
        mx, my = (start[0] + end[0]) / 2 + label_offset[0], (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=9, color=INK_2)


def _canvas(w, h, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_axis_off()
    fig.suptitle(title, x=0.02, ha="left", fontsize=14, weight="bold")
    if subtitle:
        fig.text(0.02, 0.905, subtitle, ha="left", fontsize=10, color=INK_2)
    return fig, ax


def pipeline():
    """Pipeline v2 (spec/features/pipeline.md): ten stages, two users, and the human-in-the-loop learning loop."""
    fig, ax = _canvas(15, 7.4, "Second Look pipeline: from photo to engineer review and retraining",
                      "Every stage reports its result with a confidence. Learned models suggest, written rules decide, "
                      "an engineer confirms every High and every referral, and the corrections retrain the models")
    learned, rules, human, data = (VIOLET, "#ecebfb"), (AQUA, "#e3f5ee"), (MUTED, "#f0efec"), (BLUE, "#e4eefb")
    steps = [
        ("1  Capture (resident)", "photo + coin + element tag", human),
        ("2  Quality check", "usable? if not: Retake", rules),
        ("3  Material check", "concrete? confidence\nif not or unsure: Expert", learned),
        ("4  Find the crack", "crack pixels + element\nconfidence", learned),
        ("5  Measure", "width mm ± uncertainty\nlength, orientation", rules),
        ("6  Pattern", "crack type\nprobability", learned),
        ("7  Triage rules", "level + reason\noverall confidence", rules),
        ("8  Engineer review", "confirms or corrects\nevery High and referral", human),
        ("9  Corrections logged", "labelled examples\n(with consent)", data),
        ("10  Retraining", "new model version\nchecked before use", learned),
    ]
    w, h, gap = 2.55, 1.35, 0.5
    xs = [i * (w + gap) for i in range(5)]
    pos = [(x, 3.3) for x in xs] + [(x, 0.6) for x in reversed(xs)]
    for (title, sub, (edge, fill)), (x, y) in zip(steps, pos):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=fill, edgecolor=edge, linewidth=1.4))
        ax.text(x + w / 2, y + h - 0.3, title, ha="center", va="center", fontsize=10, weight="bold", color=INK)
        ax.text(x + w / 2, y + 0.48, sub, ha="center", va="center", fontsize=8.6, color=INK_2, linespacing=1.15)
    for i in range(4):
        _arrow(ax, (pos[i][0] + w, 3.3 + h / 2), (pos[i + 1][0], 3.3 + h / 2))
    _arrow(ax, (pos[4][0] + w / 2, 3.3), (pos[5][0] + w / 2, 0.6 + h))
    for i in range(5, 9):
        _arrow(ax, (pos[i][0], 0.6 + h / 2), (pos[i + 1][0] + w, 0.6 + h / 2))
    # learning loop: retraining feeds the learned models (stages 3, 4, 6)
    loop_x = pos[9][0] - 0.35
    ax.plot([pos[9][0] + w / 2, pos[9][0] + w / 2, loop_x], [0.6, 0.25, 0.25], color=VIOLET, lw=1.6, ls="--")
    ax.plot([loop_x, loop_x], [0.25, 5.0], color=VIOLET, lw=1.6, ls="--")
    for target in (2, 3):
        tx = pos[target][0] + w / 2
        ax.plot([loop_x, tx], [5.0, 5.0], color=VIOLET, lw=1.6, ls="--")
        _arrow(ax, (tx, 5.0), (tx, 3.3 + h))
    ax.plot([loop_x, pos[5][0] + w / 2], [0.25, 0.25], color=VIOLET, lw=1.6, ls="--")
    _arrow(ax, (pos[5][0] + w / 2, 0.25), (pos[5][0] + w / 2, 0.6))
    ax.text(loop_x + 0.1, 5.12, "human-in-the-loop learning: retrains stages 3, 4 and 6", fontsize=9, color=VIOLET,
            va="bottom")
    ax.text(pos[6][0] + w / 2, 0.08, "the risk matrix never changes automatically", fontsize=8.5, color=INK_2,
            ha="center", va="top")
    ax.set_xlim(-0.7, xs[-1] + w + 0.2)
    ax.set_ylim(-0.6, 5.7)
    ax.legend(handles=[Patch(facecolor=f, edgecolor=e, label=l) for l, (e, f) in
                       [("Learned model", learned), ("Written rule, auditable", rules), ("Human (resident, engineer)",
                                                                                         human), ("Data", data)]],
              loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False)
    return fig


def decision_flow():
    fig, ax = _canvas(13, 8.2, "Decision logic: every doubt ends at an expert",
                      "Order of checks in triage.matrix.assess(); Low is reachable only after all three checks say yes. "
                      "Thresholds illustrative")
    q_fill, q_edge = "#f0efec", MUTED
    _box(ax, 0, 6.6, 3.8, 1, "1  Image usable?\nblur, light, coin visible", q_fill, q_edge)
    _box(ax, 0, 4.8, 3.8, 1, "2  Reinforced concrete?\nmaterial confidence ≥ 0.8", q_fill, q_edge)
    _box(ax, 0, 3.0, 3.8, 1, "3  Element and pattern known and fit,\nconfidence ≥ 0.8, width measured?", q_fill, q_edge)
    _box(ax, 0, 1.2, 3.8, 1, "Matrix v2: pattern × width (upper end),\nthen element and warning signs raise", q_fill,
         q_edge, size=9)
    _box(ax, 5.4, 6.6, 2.8, 1, "Retake", LEVEL["Retake"], LEVEL["Retake"], color="white", weight="bold")
    _box(ax, 5.4, 4.8, 2.8, 1, "Expert needed\nmaterial not supported\nor unclear", LEVEL["Expert needed"],
         LEVEL["Expert needed"], color="white", weight="bold", size=9)
    _box(ax, 5.4, 3.0, 2.8, 1, "Expert needed\nmodel unsure", LEVEL["Expert needed"], LEVEL["Expert needed"],
         color="white", weight="bold", size=9)
    for i, lvl in enumerate(["Low", "Medium", "High"]):
        x = -0.6 + i * 2.6
        sub = {"Low": "routine monitoring", "Medium": "low-cost advice, recheck", "High": "engineer must confirm"}[lvl]
        _box(ax, x, -0.8, 2.3, 1, f"{lvl}\n{sub}", LEVEL[lvl], LEVEL[lvl], color=ON_FILL.get(lvl, "white"),
             weight="bold", size=9)
        _arrow(ax, (1.9, 1.2), (x + 1.15, 0.2))
    _box(ax, 9.6, 2.6, 2.9, 1.6, "Engineer review\nevery High and\nevery Expert needed", "#f0efec", INK_2,
         weight="bold")
    _box(ax, 9.6, 0.3, 2.9, 1.3, "Correction logged\n→ retrains the models", "#e4eefb", BLUE, size=9.5)
    for y in (7.1, 5.3, 3.5):
        _arrow(ax, (3.8, y), (5.4, y), "no")
    for y0, y1 in ((6.6, 5.8), (4.8, 4.0), (3.0, 2.2)):
        _arrow(ax, (1.9, y0), (1.9, y1), "yes", (0.28, 0))
    _arrow(ax, (8.2, 5.3), (9.6, 4.0))
    _arrow(ax, (8.2, 3.5), (9.6, 3.4))
    _arrow(ax, (6.9, -0.3), (9.6, 2.7))
    _arrow(ax, (11.05, 2.6), (11.05, 1.6))
    ax.set_xlim(-0.8, 12.8)
    ax.set_ylim(-1.1, 7.9)
    return fig


def risk_matrix():
    """Matrix v2: base level per pattern x width band, plus what can raise it (read from risk_matrix_v2.json)."""
    fig = plt.figure(figsize=(15, 7.2))
    ax = fig.add_axes([0.2, 0.12, 0.47, 0.66])
    for r, pattern in enumerate(PATTERNS):
        for c, band in enumerate(BANDS):
            lvl = MATRIX[band][r]
            ax.add_patch(FancyBboxPatch((c + 0.04, r + 0.07), 0.92, 0.86, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor=LEVEL[lvl], edgecolor="none"))
            ax.text(c + 0.5, r + 0.5, lvl, ha="center", va="center", weight="bold", fontsize=10.5,
                    color=ON_FILL.get(lvl, "white"))
    ax.set_xlim(0, len(BANDS))
    ax.set_ylim(len(PATTERNS), 0)
    ax.set_xticks([c + 0.5 for c in range(len(BANDS))], [BAND_NAMES[b] for b in BANDS], fontsize=10.5)
    ax.set_yticks([r + 0.5 for r in range(len(PATTERNS))], [PATTERN_NAMES[p] for p in PATTERNS], fontsize=10.5)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(len(BANDS) / 2, -0.75, "Crack width (upper end of the measurement)", ha="center", fontsize=10, color=INK_2)

    side = fig.add_axes([0.71, 0.12, 0.27, 0.66])
    side.set_axis_off()
    side.set_xlim(0, 1)
    side.set_ylim(0, 1)
    side.text(0, 0.98, "What raises the level (never lowers it)", fontsize=11.5, weight="bold", va="top")
    lines = [(f"It is a {ELEMENTS[e]}", f"+{n}") for e, n in ELEMENT_RAISE.items() if n]
    lines += [(name[0].upper() + name[1:], "to High" if effect == "High" else effect)
              for name, effect in ((ESCALATORS[k], _ESCALATOR_EFFECT[k]) for k in ESCALATORS)]
    for i, (text, effect) in enumerate(lines):
        y = 0.86 - i * 0.092
        side.add_patch(FancyBboxPatch((0, y - 0.035), 0.17, 0.07, boxstyle="round,pad=0,rounding_size=0.02",
                                      facecolor="#f0efec" if effect != "to High" else LEVEL["High"], edgecolor="none"))
        side.text(0.085, y, effect, ha="center", va="center", fontsize=9.5, weight="bold",
                  color=INK if effect != "to High" else "white")
        side.text(0.2, y, text, va="center", fontsize=9.8, color=INK)
    side.text(0, 0.03, "Levels stop at High. Any doubt (photo, material,\nelement, pattern, width) goes to Expert needed.",
              fontsize=9, color=INK_2, va="bottom")

    fig.suptitle(f"Risk matrix for reinforced concrete, v{VERSION}", x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.905, "Base level from crack pattern × width; the element and warning signs can only raise it. "
             "All values illustrative until calibrated with the engineering partners. Source: src/triage/risk_matrix_v2.json",
             fontsize=10, color=INK_2)
    return fig


# Only what the tool works on (decision D16); out-of-scope and Phase 3 items are in docs/segmentation_tree.md.
TREE = {
    "A. Buildings deteriorate unwatched": ["A1 Ageing, no maintenance", "A2 Added floors, poor ground"],
    "B. Residents cannot read the signs": ["B1 Harmless vs structural", "B2 Wrong all-clear", "B3 Photo quality, scale",
                                           "B4 Not every wall is concrete"],
    "C. Too few engineers": ["C1 No ranked list", "C2 Reports not acted on", "C3 Backlog: 114 buildings"],
    "D. Data is scarce": ["D1 Public data: bridges and roads", "D2 No engineer labels"],
}
ATOMIC_FROM = {"B1", "B2", "B3", "B4", "C1"}
TREE_YELLOW, TREE_NAVY = "#F2C14E", "#2F4B7C"


def _pill(ax, x, y, w, h, text, fill, ink, size):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                facecolor=fill, edgecolor="none", zorder=3))
    ax.text(x, y, text, ha="center", va="center", color=ink, fontsize=size, weight="bold", zorder=4)


def _elbow(ax, x0, y0, x1, y1, ymid, colour, r=0.28):
    """Vertical down from (x0, y0), across at ymid with rounded corners, down to (x1, y1)."""
    from matplotlib.path import Path as MPath

    dx = x1 - x0
    if abs(dx) < 1e-6:
        verts, codes = [(x0, y0), (x1, y1)], [MPath.MOVETO, MPath.LINETO]
    else:
        s, r = (1 if dx > 0 else -1), min(r, abs(dx) / 2)
        verts = [(x0, y0), (x0, ymid + r), (x0, ymid), (x0 + s * r, ymid), (x1 - s * r, ymid), (x1, ymid),
                 (x1, ymid - r), (x1, y1)]
        codes = [MPath.MOVETO, MPath.LINETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3, MPath.CURVE3,
                 MPath.LINETO]
    from matplotlib.patches import PathPatch
    ax.add_patch(PathPatch(MPath(verts, codes), facecolor="none", edgecolor=colour, lw=2.2, zorder=1,
                           capstyle="round"))


def _tag(ax, x, y, text, colour):
    ax.add_patch(plt.Circle((x, y), 0.33, facecolor="white", edgecolor=colour, lw=2.2, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=11, weight="bold", color=TREE_NAVY, zorder=4)


def segmentation_tree():
    """Flowchart style: pill nodes, rounded connectors with letter tags, circle leaves with caps labels.
    Yellow marks the path into the atomic problem, navy the supporting context."""
    import textwrap

    fig, ax = plt.subplots(figsize=(18, 10.2))
    ax.set_axis_off()
    fig.suptitle("Problem segmentation tree", x=0.02, ha="left", fontsize=15, weight="bold")
    fig.text(0.02, 0.925, "Macro problem → four branches (meso) → causes and needs (micro) → the atomic problem we work "
             "on first. Yellow: path into the atomic problem. Navy: supporting context. Sources in docs/sources.md",
             fontsize=10.5, color=INK_2)
    leaf_gap, group_gap, r_leaf = 1.75, 0.9, 0.62
    y_top, y_meso, y_leaf, y_atomic, y_final = 11.0, 8.6, 5.7, 2.55, 1.15
    xs, x = {}, 0.0
    for meso, kids in TREE.items():
        xs[meso] = []
        for _ in kids:
            xs[meso].append(x)
            x += leaf_gap
        x += group_gap
    width = x - group_gap - leaf_gap
    centre = width / 2
    feeds = {code[0] for code in ATOMIC_FROM}

    _pill(ax, centre, y_top, 14.2, 0.95, "PEOPLE CANNOT JUDGE WHETHER THE CRACKS IN THEIR AGEING BUILDINGS ARE DANGEROUS",
          TREE_YELLOW, TREE_NAVY, 12.5)
    n = len(TREE)
    for i, (meso, kids) in enumerate(TREE.items()):
        letter = meso[0]
        on_path = letter in feeds
        colour = TREE_YELLOW if on_path else TREE_NAVY
        mx = sum(xs[meso]) / len(xs[meso])
        # outer branches leave the top pill further out and turn higher, so no two connectors cross
        offset = (i - (n - 1) / 2) * 1.15
        ymid = y_top - 0.95 if abs(offset) > 1 else y_top - 1.55
        x0 = centre + offset
        _elbow(ax, x0, y_top - 0.48, mx, y_meso + 0.36, ymid, colour)
        _tag(ax, (x0 + mx) / 2, ymid, letter, colour)
        title = meso.split(". ", 1)[1].upper()
        _pill(ax, mx, y_meso, max(3.0, 0.172 * len(title)), 0.72, title, colour,
              TREE_NAVY if on_path else "white", 10.5)
        for lx, kid in zip(xs[meso], kids):
            code, label = kid.split(" ", 1)
            leaf_on_path = code in ATOMIC_FROM
            lc = TREE_YELLOW if leaf_on_path else TREE_NAVY
            _elbow(ax, mx, y_meso - 0.36, lx, y_leaf + r_leaf, y_meso - 1.15, lc)
            ax.add_patch(plt.Circle((lx, y_leaf), r_leaf, facecolor="white", edgecolor=lc, lw=3, zorder=3))
            ax.text(lx, y_leaf, code, ha="center", va="center", fontsize=15, weight="bold", color=TREE_NAVY, zorder=4)
            ax.text(lx, y_leaf - r_leaf - 0.2, textwrap.fill(label.upper(), 14, break_on_hyphens=False),
                    ha="center", va="top", fontsize=8.8, color=INK, linespacing=1.15)
            if leaf_on_path:
                _elbow(ax, lx, y_leaf - r_leaf - 1.0, centre, y_atomic + 0.4, y_atomic + 0.85, TREE_YELLOW)
    _pill(ax, centre, y_atomic, 16.5, 0.8, "ATOMIC PROBLEM: ONE PHOTO, ONE CRACK, ONE CONCRETE ELEMENT → LEVEL, CONFIDENCE, REASON",
          TREE_YELLOW, TREE_NAVY, 12)
    _elbow(ax, centre, y_atomic - 0.4, centre, y_final + 0.36, y_final + 0.9, TREE_NAVY)
    _pill(ax, centre, y_final, 11.5, 0.72, "SECOND LOOK:  LOW · MEDIUM · HIGH · EXPERT NEEDED · RETAKE",
          TREE_NAVY, "white", 11.5)
    ax.set_xlim(-2.0, width + 2.0)
    ax.set_ylim(0.6, 11.6)
    ax.set_aspect("equal")
    return fig


STAGES = ["Quality gate", "Material check", "YOLO detector", "U-Net segmenter", "Measurement (mm)", "Pattern model",
          "Agent: building data", "Triage rules sign-off", "Engineer review + retraining", "Evaluation (ground truth)"]
SOURCES = ["SDNET2018", "CrackSeg9k", "crack-seg\n(Ultralytics)", "PHI-Net", "CODEBRIM", "Haiti + Nepal\nsurveys",
           "Brick masonry\n(Darbhanga)", "Masonry masks\n(Dais et al.)", "Pilot photos", "Engineer-\nlabelled photos",
           "Tripoli lists\n(106 / 114)", "Engineering\npartner"]
# From docs/data_map.md, section 1. Rows follow STAGES, columns follow SOURCES.
COVERAGE = [
    ["none", "none", "none", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["partial", "none", "none", "partial", "partial", "none", "partial", "partial", "planned", "planned", "none", "none"],
    ["none", "none", "partial", "partial", "partial", "none", "partial", "none", "planned", "planned", "none", "none"],
    ["none", "covered", "covered", "none", "none", "none", "none", "partial", "none", "planned", "none", "none"],
    ["none", "none", "none", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["partial", "none", "none", "partial", "partial", "partial", "partial", "none", "none", "planned", "none", "none"],
    ["none", "none", "none", "none", "none", "partial", "none", "none", "none", "none", "partial", "none"],
    ["none", "none", "none", "none", "none", "partial", "none", "none", "none", "none", "none", "planned"],
    ["none", "none", "none", "none", "none", "none", "none", "none", "none", "planned", "none", "planned"],
    ["none", "none", "none", "none", "none", "partial", "none", "none", "none", "planned", "partial", "planned"],
]
COVERAGE_LABEL = {"covered": "covers", "partial": "partly", "planned": "planned", "none": ""}


def data_coverage():
    fig, ax = plt.subplots(figsize=(18, 6.8))
    for r, row in enumerate(COVERAGE):
        for c, state in enumerate(row):
            ax.add_patch(FancyBboxPatch((c + 0.04, r + 0.08), 0.92, 0.84, boxstyle="round,pad=0,rounding_size=0.05",
                                        facecolor=SEQ[state], edgecolor=GRID if state == "none" else "none", lw=0.8))
            ax.text(c + 0.5, r + 0.5, COVERAGE_LABEL[state], ha="center", va="center", fontsize=9,
                    color="white" if state in ("covered", "partial") else INK)
    ax.set_xlim(0, len(SOURCES))
    ax.set_ylim(len(STAGES), 0)
    ax.set_xticks([c + 0.5 for c in range(len(SOURCES))], SOURCES)
    ax.set_yticks([r + 0.5 for r in range(len(STAGES))], STAGES)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(handles=[Patch(facecolor=SEQ[k], edgecolor=GRID, label=l) for k, l in
                       [("covered", "Covers the need"), ("partial", "Partly"), ("planned", "Planned, does not exist yet"),
                        ("none", "Nothing")]],
              loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False)
    fig.suptitle("Data map: which source feeds which pipeline stage", x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.905, "Public data covers only U-Net training; every other stage needs our own photos or an "
             "engineer. From docs/data_map.md (25 Oct 2026).", fontsize=10, color=INK_2)
    fig.subplots_adjust(left=0.13, right=0.99, top=0.76, bottom=0.1)
    return fig


# From docs/data_map.md, section 2 (checked on the source pages, 24 Oct 2026).
DATASETS = [("SDNET2018", 56_000, "56,000+  ·  CC BY 4.0  ·  mostly bridges and pavement (off-concept)"),
            ("METU", 40_000, "40,000  ·  CC BY 4.0  ·  concrete walls of campus buildings"),
            ("PHI-Net", 36_413, "36,413  ·  CC BY-NC-SA 4.0  ·  post-earthquake, no masks"),
            ("CrackSeg9k", 9_255, "9,255  ·  CC0  ·  pixel masks, mostly pavement"),
            ("crack-seg (Ultralytics)", 4_029, "4,029  ·  Public Domain  ·  polygons, roads and walls"),
            ("Haiti 2010 survey", 6_526, "6,526 photos of 183 buildings  ·  engineer-rated  ·  licence not stated"),
            ("Brick masonry (Darbhanga)", 4_259, "4,259  ·  CC BY 4.0  ·  brick, one heritage building"),
            ("Brick facades (Strathclyde)", 700, "700  ·  CC BY 4.0  ·  brick facades"),
            ("Pilot phone photos", 0, "0  ·  about 30 cracks this week  ·  no risk labels"),
            ("Engineer-labelled phone photos", 0, "0  ·  to collect in Phase 2  ·  the target data")]


def dataset_sizes():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    names = [d[0] for d in DATASETS]
    ys = range(len(DATASETS))
    ax.barh(ys, [d[1] for d in DATASETS], height=0.42, color=BLUE)
    for y, (_, n, label) in zip(ys, DATASETS):
        ax.text(n + 800, y, label, va="center", fontsize=9.5, color=INK)
    ax.set_yticks(list(ys), names)
    ax.invert_yaxis()
    ax.set_xlim(0, 110_000)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1000:.0f}K" if v else "0"))
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("Images")
    fig.suptitle("Public crack data is large; the closest to our homes are small engineer surveys",
                 x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.875, "Image counts and licences from each dataset's page. Not plotted: CODEBRIM (36.4 GB, count "
             "not stated, non-commercial) and the Dais et al. masonry subset.", fontsize=9.5, color=INK_2)
    fig.subplots_adjust(left=0.24, right=0.98, top=0.8, bottom=0.14)
    return fig


def confusion_template():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw={"width_ratios": [1, 1.6]})
    cells = [  # (row, col, title, meaning, colour)
        (0, 0, "TP", "danger caught,\nengineer visits", LEVEL["Low"]),
        (0, 1, "FN", "missed danger:\nwrong all-clear. Stop condition", LEVEL["High"]),
        (1, 0, "FP", "unneeded visit,\ncosts engineer time", LEVEL["Medium"]),
        (1, 1, "TN", "correctly kept off\nthe engineer's list", LEVEL["Low"]),
    ]
    for r, c, title, meaning, colour in cells:
        a1.add_patch(FancyBboxPatch((c + 0.04, r + 0.04), 0.92, 0.92, boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=colour, edgecolor="none"))
        ink = INK if colour == LEVEL["Medium"] else "white"
        a1.text(c + 0.5, r + 0.36, title, ha="center", va="center", fontsize=18, weight="bold", color=ink)
        a1.text(c + 0.5, r + 0.66, meaning, ha="center", va="center", fontsize=9, color=ink)
    a1.set_xlim(0, 2)
    a1.set_ylim(2, 0)
    a1.set_xticks([0.5, 1.5], ["Tool flags\n(High or Expert needed)", "Tool does not flag\n(Low or Medium)"])
    a1.set_yticks([0.5, 1.5], ["Engineer:\nHigh", "Engineer:\nLow or Medium"])
    a1.xaxis.tick_top()
    a1.set_title("Table 1: the safety question", loc="left", weight="bold", pad=44)

    kinds = {"correct": ("#e3f5ee", INK), "over-cautious": ("#fdf0d0", INK), "false alarm": ("#fdf0d0", INK),
             "referral": ("#fbe3d9", INK), "retake": ("#f0efec", INK_2),
             "false all-clear": (LEVEL["High"], "white"), "missed danger": (LEVEL["High"], "white"),
             "missed danger\n(worst)": ("#9e2424", "white")}
    grid = [["correct", "over-cautious", "false alarm", "referral", "retake"],
            ["false all-clear", "correct", "over-cautious", "referral", "retake"],
            ["missed danger\n(worst)", "missed danger", "correct", "referral", "retake"]]
    for r, row in enumerate(grid):
        for c, kind in enumerate(row):
            fill, ink = kinds[kind]
            a2.add_patch(FancyBboxPatch((c + 0.04, r + 0.06), 0.92, 0.88, boxstyle="round,pad=0,rounding_size=0.05",
                                        facecolor=fill, edgecolor="none"))
            a2.text(c + 0.5, r + 0.5, kind, ha="center", va="center", fontsize=9, color=ink,
                    weight="bold" if "missed" in kind or "all-clear" in kind else "normal")
    a2.set_xlim(0, 5)
    a2.set_ylim(3, 0)
    a2.set_xticks([c + 0.5 for c in range(5)], ["Low", "Medium", "High", "Expert\nneeded", "Retake"])
    a2.set_yticks([0.5, 1.5, 2.5], ["Low", "Medium", "High"])
    a2.xaxis.tick_top()
    a2.set_xlabel("Tool output")
    a2.xaxis.set_label_position("top")
    a2.set_ylabel("Engineer on site")
    a2.set_title("Table 2: full confusion matrix", loc="left", weight="bold", pad=44)
    for ax in (a1, a2):
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
    fig.suptitle("How the tool will be scored", x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.02, "Template: counts come from a held-out set of engineer-labelled photos, which does not "
             "exist yet. The non-AI baseline (engineer looks at the photo only) is scored the same way. "
             "spec/features/evaluation.md", fontsize=9, color=INK_2)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.74, bottom=0.1, wspace=0.25)
    return fig


# From spec/constitution/roadmap.md. (workstream, task, first week, last week, at risk)
PLAN = [
    ("Deliverables", "29 Oct deliverables + real-data test (done)", 1, 1, False),
    ("Deliverables", "State-of-the-art review (reference thesis)", 1, 1, False),
    ("Deliverables", "Expert package to the professor (Mon 2 Nov)", 1, 1, False),
    ("Deliverables", "Midterm deck + problem & data brief", 1, 2, False),
    ("Deliverables", "Lean Canvas", 6, 7, False),
    ("Deliverables", "Pitch deck, final presentation", 7, 8, False),
    ("Deliverables", "Blog post", 8, 9, False),
    ("Data", "Quality gate on public sets (done)", 1, 1, False),
    ("Data", "Material check: concrete vs not, first test", 1, 1, False),
    ("Data", "Map public labels to the 7 patterns", 2, 3, False),
    ("Pilot", "Collect pilot photos (~30 cracks)", 2, 2, False),
    ("Pilot", "Prepare, label, tune quality gate", 2, 3, False),
    ("Pilot", "Coin + width measurement (1st feature)", 3, 4, False),
    ("Models", "U-Net on CrackSeg9k + crack-seg", 3, 4, False),
    ("Models", "Pattern model (pre-trained)", 4, 5, False),
    ("Models", "YOLO crack and element detector", 4, 6, False),
    ("Agent and MCP", "First MCP connection attempt", 3, 3, False),
    ("Agent and MCP", "Plan/build harness, MCP to all sources", 4, 5, False),
    ("Engineering partners", "Scope with EWB + structural engineer", 1, 2, False),
    ("Engineering partners", "Calibration: matrix, thresholds", 3, 5, True),
    ("Engineering partners", "Engineer-labelled photos + baseline", 4, 6, True),
    ("Integration", "Engineer review screen (mock-up)", 1, 2, False),
    ("Integration", "Beta: end-to-end on pilot photos", 4, 4, False),
    ("Integration", "Corrections logged + retraining loop", 5, 6, True),
    ("Integration", "Comparison vs non-AI baseline", 6, 6, True),
    ("Integration", "Proof of concept, limits + ethics", 7, 7, False),
    ("Integration", "Streamlit UI, realistic testing", 7, 8, False),
]
# (x in weeks from Monday 26 Oct, label, at risk); x = (days after 26 Oct + 0.5) / 7, from the syllabus.
MILESTONES = [(0.5, "29 Oct\ndata map", False), (1.07, "2 Nov\nexpert package", False), (1.64, "6 Nov\nmidterm", False),
              (2.5, "12 Nov\n1st feature", False), (3.64, "20 Nov\nbeta", False),
              (4.5, "26 Nov\nharness + MCP", False), (5.5, "3 Dec\nbaseline", True),
              (6.5, "10 Dec\nPoC + ethics", False), (7.5, "17 Dec\nfinal", False), (8.5, "24 Dec\nblog", False)]
WORKSTREAM_COLOURS = {"Deliverables": BLUE, "Data": "#eb6834", "Pilot": AQUA, "Models": "#eda100",
                      "Agent and MCP": VIOLET, "Engineering partners": "#e87ba4", "Integration": "#008300"}
WEEK_STARTS = ["26 Oct", "2 Nov", "9 Nov", "16 Nov", "23 Nov", "30 Nov", "7 Dec", "14 Dec", "21 Dec"]


def timeline():
    weeks = len(WEEK_STARTS)
    fig, ax = plt.subplots(figsize=(14, 10.2))
    n = len(PLAN)
    ax.axvspan(3, 4, color="#f0efec", zorder=0)
    ax.text(3.5, n - 0.9, "hackathon\n(no studio)", ha="center", va="center", fontsize=8.5, color=INK_2)
    previous = None
    for i, (stream, task, start, end, risk) in enumerate(PLAN):
        colour = WORKSTREAM_COLOURS[stream]
        if stream != previous and previous is not None:
            ax.axhline(i - 0.5, color=GRID, lw=0.8, zorder=1)
        previous = stream
        ax.add_patch(FancyBboxPatch((start - 1 + 0.06, i - 0.26), end - start + 1 - 0.12, 0.52,
                                    boxstyle="round,pad=0,rounding_size=0.12", zorder=2,
                                    facecolor=colour if not risk else "white", edgecolor=colour,
                                    hatch="///" if risk else None, lw=1.6))
    for k, (x, label, risk) in enumerate(MILESTONES):
        ax.plot(x, -0.8, marker="D", ms=10, color=LEVEL["High"] if not risk else "white",
                markeredgecolor=LEVEL["High"], mew=1.8, zorder=3)
        ax.text(x, -1.85 if k % 2 == 0 else -2.75, label, ha="center", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(0, weeks)
    ax.set_ylim(n - 0.4, -3.3)
    ax.set_xticks([w + 0.5 for w in range(weeks)], [f"W{w + 1}\n{d}" for w, d in enumerate(WEEK_STARTS)])
    ax.set_yticks(range(n), [t[1] for t in PLAN])
    ax.xaxis.tick_top()
    for w in range(weeks + 1):
        ax.axvline(w, color=GRID, lw=0.6, zorder=0)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    handles = [Patch(facecolor=c, edgecolor=c, label=s) for s, c in WORKSTREAM_COLOURS.items()]
    handles.append(Patch(facecolor="white", edgecolor=INK_2, hatch="///", label="At risk: needs engineering partners"))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.4, -0.01), ncol=4, frameon=False)
    fig.suptitle("Plan to the final presentation, 26 Oct to 24 Dec 2026", x=0.02, ha="left", fontsize=14,
                 weight="bold")
    fig.text(0.02, 0.9, "Milestones from the studio syllabus. Engineering partners: Engineers Without Borders and a "
             "third-party structural engineer.\nFallback if no engineer ratings by 26 Nov: compare on pilot photos "
             "only; the matrix stays illustrative. Source: spec/constitution/roadmap.md", fontsize=9.5, color=INK_2)
    fig.subplots_adjust(left=0.25, right=0.98, top=0.8, bottom=0.11)
    return fig


FIGURES = {
    "01_pipeline.png": pipeline,
    "02_decision_flow.png": decision_flow,
    "03_risk_matrix.png": risk_matrix,
    "04_segmentation_tree.png": segmentation_tree,
    "05_data_coverage.png": data_coverage,
    "06_dataset_sizes.png": dataset_sizes,
    "07_confusion_template.png": confusion_template,
    "09_timeline.png": timeline,
}


def main(out_dir: Path = Path(__file__).resolve().parents[2] / "figures") -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, make in FIGURES.items():
        fig = make()
        path = out_dir / name
        fig.savefig(path, dpi=200)
        plt.close(fig)
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in main():
        print(p)
