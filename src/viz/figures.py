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


# Pipeline v3 (spec/features/pipeline.md). Boxes: (row, column) -> (kind, title, body, status).
# Rows follow PHI-Net task 1 scene levels: 0 = S structural, 1 = O object, 2 = P pixel [55].
PIPE_LANES = [("S", "STRUCTURAL", "from far:\nthe building"), ("O", "OBJECT", "mid-range:\none element"),
              ("P", "PIXEL", "close-up:\nthe crack")]
PIPE_PHASES = [("1  Capture", "photos and answers"), ("2  Check", "written rules"),
               ("3  Perceive", "learned models, each with a confidence"), ("4  Decide", "written rules, auditable"),
               ("5  Act", "people")]
PIPE_BOXES = {
    (0, 0): ("human", "Building case (once)", "questionnaire: age, storeys, added floors,\ntypology + changes, open ground floor\n+ facade photo + map data (MCP)", "spec"),
    (0, 1): ("rule", "Completeness check", "every answer known or 'unknown'\nunknown counts as a risk flag\nand stays visible as unknown", "spec"),
    (0, 2): ("learned", "Building reading", "now: the questionnaire answers\nlater: model on the facade photo\n(storeys, typology; PHI-Net task 5)", "spec"),
    (0, 3): ("rule", "Building risk score", "worst crack level → P1 · P2 · P3\n+1 tier if ≥ 2 risk flags\n+1 tier if Medium+ in ≥ 2 elements", "spec"),
    (0, 4): ("human", "Engineer", "ranked list of buildings + dossier\nconfirms or corrects every High\nand every referral; rates on site", "spec"),
    (1, 0): ("human", "Element photo", "the whole element\nwith the scale card\nno question to the resident", "spec"),
    (1, 1): ("rule", "Scale and angle", "scale card visible?\nphone parallel to the wall?\nno → retake", "spec"),
    (1, 2): ("learned", "Material + element", "material model: concrete or not\nelement model: column, beam, slab, wall\n(PHI-Net task 6) · each + confidence", "spec"),
    (1, 3): ("rule", "Element rules", "not concrete or unsure → Expert\npattern does not fit element → Expert\ncolumn → +1 level", "code"),
    (2, 0): ("human", "Crack close-up", "scale card + 2 marker stickers\nburst of photos, flash on and off\nresident or field worker", "spec"),
    (2, 1): ("rule", "Photo checks", "sharp and lit? ≥ 3 px across the crack?\nno → retake closer; still no →\nwidth band read on the card", "partly"),
    (2, 2): ("learned", "Crack reading", "crack pixels → width mm ± 1 px\npattern model (PHI-Net tasks 3, 8)\nfield worker until confident", "spec"),
    (2, 3): ("rule", "Crack level + growth", "matrix v2 → level, reason, next step\ngrowth counts only if larger\nthan the measurement uncertainty", "partly"),
    (2, 4): ("human", "Resident", "level, reason, next step,\nrecheck date\nnever 'safe', never a clearance", "partly"),
}
PIPE_STATUS = {"code": ("in code", "#2F4B7C", "#2F4B7C", "white"),
               "partly": ("partly in code", "#dfe6f2", "#2F4B7C", "#2F4B7C"),
               "spec": ("specified", "#FFFFFF", MUTED, INK_2)}


def pipeline():
    """Pipeline v3: three scales (S, O, P) x five phases, scene check, monitoring and learning loops, status."""
    kinds = {"learned": (VIOLET, "#ecebfb"), "rule": (AQUA, "#e3f5ee"), "human": (MUTED, "#f0efec")}
    x0, w, y0, h = [0, 4.1, 9.35, 13.45, 17.55], 3.5, [7.0, 4.25, 1.5], 2.05
    rx, rw = 8.0, 0.95  # scene check
    fig, ax = plt.subplots(figsize=(21, 12.6))
    ax.set_axis_off()
    fig.suptitle("Second Look pipeline v3: three scales, a building risk score and monitoring", x=0.02, ha="left",
                 fontsize=17, weight="bold")
    fig.text(0.02, 0.905, "Scales as in PHI-Net task 1: S structural (the building), O object (the element), P pixel "
             "(the crack) [53][55]. Learned models report a confidence; written rules decide; any doubt goes to an "
             "engineer.\nResidents are never asked the material, the element or the crack pattern: models identify "
             "them. Status on 27 Oct 2026. Source: spec/features/pipeline.md", fontsize=11, color=INK_2,
             linespacing=1.5)

    def arrow(p0, p1, colour=INK_2, ls="-", lw=1.5):
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=colour, lw=lw, ls=ls,
                                                          shrinkA=0, shrinkB=0, mutation_scale=15))

    for c, (head, sub) in enumerate(PIPE_PHASES):
        ax.text(x0[c] + w / 2, 9.85, head, ha="center", fontsize=13, weight="bold", color=INK)
        ax.text(x0[c] + w / 2, 9.5, sub, ha="center", fontsize=9.5, color=INK_2)
    for r, (code, name, what) in enumerate(PIPE_LANES):
        y = y0[r]
        ax.add_patch(FancyBboxPatch((-2.25, y), 1.75, h, boxstyle="round,pad=0,rounding_size=0.1",
                                    facecolor=TREE_NAVY, edgecolor="none"))
        ax.text(-1.375, y + h - 0.5, code, ha="center", va="center", color=TREE_YELLOW, fontsize=26, weight="bold")
        ax.text(-1.375, y + h / 2 - 0.15, name, ha="center", va="center", color="white", fontsize=10, weight="bold")
        ax.text(-1.375, y + 0.42, what, ha="center", va="center", color="#dfe6f2", fontsize=9, linespacing=1.2)
    for (r, c), (kind, title, body, status) in PIPE_BOXES.items():
        edge, fill = kinds[kind]
        x, y = x0[c], y0[r]
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.1", facecolor=fill,
                                    edgecolor=edge, lw=1.6))
        ax.text(x + w / 2, y + h - 0.42, title, ha="center", va="center", fontsize=11.3, weight="bold", color=INK)
        ax.text(x + w / 2, y + 0.8, body, ha="center", va="center", fontsize=9.3, color=INK_2, linespacing=1.25)
        label, chip_fill, chip_edge, chip_ink = PIPE_STATUS[status]
        cw = 0.2 + 0.085 * len(label)
        ax.add_patch(FancyBboxPatch((x + w - 0.15 - cw, y + h - 0.15), cw, 0.3,
                                    boxstyle="round,pad=0,rounding_size=0.15", facecolor=chip_fill,
                                    edgecolor=chip_edge, lw=1.1, zorder=4))
        ax.text(x + w - 0.15 - cw / 2, y + h, label, ha="center", va="center", fontsize=8, color=chip_ink,
                weight="bold", zorder=5)
        if c == 1:  # Check -> scene check -> Perceive
            arrow((x + w, y + h / 2), (rx, y + h / 2))
            arrow((rx + rw, y + h / 2), (x0[2], y + h / 2))
        elif c < 3 and (r, c + 1) in PIPE_BOXES:
            arrow((x + w, y + h / 2), (x0[c + 1], y + h / 2))

    # scene check: PHI-Net task 1
    ax.add_patch(FancyBboxPatch((rx, y0[2]), rw, y0[0] + h - y0[2], boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor=kinds["learned"][1], edgecolor=kinds["learned"][0], lw=1.6))
    ax.text(rx + rw / 2, (y0[2] + y0[0] + h) / 2, "SCENE CHECK (PHI-Net task 1):  is this photo S, O or P?\n"
            "now: the app's guided capture sets it  ·  later: a scene model", rotation=90, ha="center",
            va="center", fontsize=9.3, weight="bold", color=INK, linespacing=1.6)

    # between the rows: material and element down to the crack level; crack results up to the building score
    arrow((x0[3] + w / 2, y0[1]), (x0[3] + w / 2, y0[2] + h))
    ax.text(x0[3] + w / 2 + 0.12, y0[2] + h + 0.35, "material, element", fontsize=9.3, color=INK_2, va="center")
    gx = x0[3] + w + 0.3
    ax.plot([x0[3] + w, gx, gx], [y0[2] + 0.55, y0[2] + 0.55, y0[0] + 0.55], color=INK_2, lw=1.5)
    arrow((gx, y0[0] + 0.55), (x0[3] + w, y0[0] + 0.55))
    ax.text(gx + 0.08, y0[1] + 0.3, "crack levels,\ngrowth, damage\nspread across\nelements", fontsize=9.3,
            color=INK_2, va="center", linespacing=1.2)
    arrow((x0[3] + w, y0[0] + 1.45), (x0[4], y0[0] + 1.45))
    arrow((x0[3] + w, y0[2] + 1.45), (x0[4], y0[2] + 1.45))

    # learning loop: engineer corrections retrain the learned models of phase 3
    ly, lx = 10.6, x0[4] + 0.45
    ax.plot([lx, lx], [y0[0] + h + 0.15, ly], color=VIOLET, lw=1.8, ls="--")
    ax.plot([lx, x0[2] + w / 2], [ly, ly], color=VIOLET, lw=1.8, ls="--")
    arrow((x0[2] + w / 2, ly), (x0[2] + w / 2, 10.2), colour=VIOLET, ls="--", lw=1.8)
    ax.text((x0[2] + w / 2 + lx) / 2, ly + 0.42, "LEARNING LOOP: engineer corrections and on-site ratings become "
            "labels and retrain the learned models (phase 3)", ha="center", fontsize=9.8, color=VIOLET, weight="bold")
    ax.text((x0[2] + w / 2 + lx) / 2, ly + 0.14, "each new version is checked on held-out photos before use; "
            "written rules change only by a reviewed decision", ha="center", fontsize=9.3, color=VIOLET)

    # monitoring loop: the same crack again on its recheck date
    my = 0.85
    ax.plot([x0[4] + w / 2, x0[4] + w / 2], [y0[2], my], color=BLUE, lw=1.8, ls="--")
    ax.plot([x0[4] + w / 2, x0[0] + w / 2], [my, my], color=BLUE, lw=1.8, ls="--")
    arrow((x0[0] + w / 2, my), (x0[0] + w / 2, y0[2]), colour=BLUE, ls="--", lw=1.8)
    ax.text((x0[0] + x0[4]) / 2 + w / 2, my - 0.3, "MONITORING LOOP: on the recheck date (Low: 6 months, Medium: "
            "1 month) the same crack ID and stickers are photographed again, with the last photo as an overlay",
            ha="center", fontsize=9.8, color=BLUE, weight="bold")
    ax.text((x0[0] + x0[4]) / 2 + w / 2, my - 0.58, "growth larger than the measurement uncertainty raises the "
            "crack level, and through it the building risk score", ha="center", fontsize=9.3, color=BLUE)

    handles = []
    for (klabel, kkey), skey in zip([("Learned model (reports a confidence)", "learned"),
                                     ("Written rule, auditable", "rule"), ("People and their inputs", "human")],
                                    ["code", "partly", "spec"]):
        e, f = kinds[kkey]
        handles.append(Patch(facecolor=f, edgecolor=e, label=klabel))
        slabel, sf, se, _ = PIPE_STATUS[skey]
        handles.append(Patch(facecolor=sf, edgecolor=se, label=f"Status: {slabel}" + (" (designed, not coded yet)" if skey == "spec" else "")))
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False,
              fontsize=10.5)
    ax.set_xlim(-2.4, x0[4] + w + 0.2)
    ax.set_ylim(-0.1, 11.3)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.85, bottom=0.08)
    return fig


def decision_flow():
    fig, ax = _canvas(13, 8.2, "Decision logic: every doubt ends at an expert",
                      "Order of checks in triage.matrix.assess(); Low is reachable only after all three checks say yes. "
                      "Thresholds illustrative")
    q_fill, q_edge = "#f0efec", MUTED
    _box(ax, 0, 6.6, 3.8, 1, "1  Image usable?\nblur, light, scale card visible", q_fill, q_edge)
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


# Segmentation tree v3 (docs/segmentation_tree.md; decisions D16, D21, D25). Only what the tool works on.
# Leaf: (code, label, path, scale, evidence). Paths: "crack" feeds the atomic problem, "building" feeds the building
# risk score, "context" explains the need. Scale as in PHI-Net task 1 [55]. Evidence: source numbers in
# docs/sources.md, expert input (studio professor, 27 Oct), measured (our data map) or assumption (to test).
TREE = [
    ("A", "Buildings change unwatched", "building", [
        ("A1", "Ageing, no maintenance", "building", "S", "[3] [9]"),
        ("A2", "Floors added on top", "building", "S", "expert input"),
        ("A3", "Structure or use changed", "building", "S", "expert input"),
    ]),
    ("B", "Residents cannot read the signs", "crack", [
        ("B1", "Harmless vs structural", "crack", "P", "assumption"),
        ("B2", "No record of growth", "crack", "P", "expert input, [46]"),
        ("B3", "Cheap phones, no scale", "crack", "P", "expert input, [46]"),
        ("B4", "Is it concrete? Can't tell", "crack", "O", "assumption"),
        ("B5", "Which element? Can't tell", "crack", "O", "assumption"),
        ("B6", "One crack hides the pattern", "building", "S", "expert input"),
    ]),
    ("C", "Too few engineers", "building", [
        ("C1", "No ranked list of buildings", "building", "S", "assumption"),
        ("C2", "Reports not acted on", "context", "", "[3] [7] [10]"),
        ("C3", "Backlog: 114 buildings", "context", "", "[3] [5]"),
    ]),
    ("D", "Data is scarce", "context", [
        ("D1", "Public data: bridges, roads", "context", "", "measured: data map"),
        ("D2", "No crack labels by engineers", "context", "", "measured: data map"),
    ]),
]
TREE_YELLOW, TREE_NAVY, TREE_GREY = "#F2C14E", "#2F4B7C", "#a8a7a1"
TREE_PATH = {"crack": TREE_YELLOW, "building": TREE_NAVY, "context": TREE_GREY}


def _pill(ax, x, y, w, h, text, fill, ink, size):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                facecolor=fill, edgecolor="none", zorder=3))
    ax.text(x, y, text, ha="center", va="center", color=ink, fontsize=size, weight="bold", zorder=4)


def _elbow(ax, x0, y0, x1, y1, ymid, colour, r=0.28):
    """Vertical down from (x0, y0), across at ymid with rounded corners, down to (x1, y1)."""
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch

    dx = x1 - x0
    if abs(dx) < 1e-6:
        verts, codes = [(x0, y0), (x1, y1)], [MPath.MOVETO, MPath.LINETO]
    else:
        s, r = (1 if dx > 0 else -1), min(r, abs(dx) / 2)
        verts = [(x0, y0), (x0, ymid + r), (x0, ymid), (x0 + s * r, ymid), (x1 - s * r, ymid), (x1, ymid),
                 (x1, ymid - r), (x1, y1)]
        codes = [MPath.MOVETO, MPath.LINETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3, MPath.CURVE3,
                 MPath.LINETO]
    ax.add_patch(PathPatch(MPath(verts, codes), facecolor="none", edgecolor=colour, lw=2.2, zorder=1,
                           capstyle="round"))


def _tag(ax, x, y, text, colour, r=0.33, size=11):
    ax.add_patch(plt.Circle((x, y), r, facecolor="white", edgecolor=colour, lw=2.2, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=size, weight="bold", color=TREE_NAVY, zorder=4)


def segmentation_tree():
    """Flowchart tree: macro pill, four branch pills, leaf circles with scale badge and evidence, then the crack
    path converges into the atomic problem and the building path into the building risk score."""
    import textwrap

    fig, ax = plt.subplots(figsize=(22, 11.6))
    ax.set_axis_off()
    fig.suptitle("Problem segmentation tree", x=0.02, ha="left", fontsize=16, weight="bold")
    fig.text(0.02, 0.915, "Macro problem → four branches → causes and needs → the atomic problem (one crack) and the "
             "building risk score (one building). Under each node: its evidence, as a source number (docs/sources.md),"
             "\nexpert input (studio professor, 27 Oct), measured (our data map) or an assumption still to test. "
             "S, O, P: the scale of the photo, as in PHI-Net task 1 (structural, object, pixel).", fontsize=11,
             color=INK_2, linespacing=1.5)
    leaf_gap, group_gap, r_leaf = 1.85, 0.9, 0.58
    y_top, y_meso, y_leaf = 12.2, 10.0, 7.3
    xs, x = {}, 0.0
    for letter, _, _, kids in TREE:
        xs[letter] = []
        for _ in kids:
            xs[letter].append(x)
            x += leaf_gap
        x += group_gap
    width = x - group_gap - leaf_gap
    centre = width / 2
    y_label = y_leaf - r_leaf - 0.18
    y_start = y_label - 1.05  # below label and evidence

    _pill(ax, centre, y_top, 14.6, 0.95, "PEOPLE CANNOT JUDGE WHETHER THE CRACKS IN THEIR AGEING BUILDINGS ARE "
          "DANGEROUS", TREE_YELLOW, TREE_NAVY, 12.5)
    n = len(TREE)
    crack_x, building_x = [], []
    for i, (letter, title, path, kids) in enumerate(TREE):
        colour = TREE_PATH[path]
        mx = sum(xs[letter]) / len(xs[letter])
        offset = (i - (n - 1) / 2) * 1.25
        ymid = y_top - 0.95 if abs(offset) > 1 else y_top - 1.55
        _elbow(ax, centre + offset, y_top - 0.48, mx, y_meso + 0.36, ymid, colour)
        _tag(ax, (centre + offset + mx) / 2, ymid, letter, colour)
        pill_ink = TREE_NAVY if path == "crack" else ("white" if path == "building" else INK)
        _pill(ax, mx, y_meso, max(3.0, 0.165 * len(title)), 0.72, title.upper(), colour, pill_ink, 10.5)
        for lx, (code, label, leaf_path, scale, evidence) in zip(xs[letter], kids):
            lc = TREE_PATH[leaf_path]
            _elbow(ax, mx, y_meso - 0.36, lx, y_leaf + r_leaf, y_meso - 1.15, lc)
            ax.add_patch(plt.Circle((lx, y_leaf), r_leaf, facecolor="white", edgecolor=lc, lw=3, zorder=3))
            ax.text(lx, y_leaf, code, ha="center", va="center", fontsize=14, weight="bold", color=TREE_NAVY,
                    zorder=4)
            if scale:
                _tag(ax, lx + 0.5, y_leaf + 0.5, scale, lc, r=0.24, size=9)
            ax.text(lx, y_label, textwrap.fill(label.upper(), 15, break_on_hyphens=False), ha="center",
                    va="top", fontsize=8.8, color=INK, linespacing=1.15)
            ax.text(lx, y_label - 0.62, evidence, ha="center", va="top", fontsize=8.3, color=INK_2, style="italic")
            if leaf_path == "crack":
                crack_x.append(lx)
            elif leaf_path == "building":
                building_x.append(lx)

    # crack path: converge into the atomic problem
    ax_c = sum(crack_x) / len(crack_x)
    y_atomic, atomic_w = 4.35, max(crack_x) - min(crack_x) + 1.3
    for lx in crack_x:
        _elbow(ax, lx, y_start, ax_c, y_atomic + 0.55, y_atomic + 0.95, TREE_YELLOW)
    ax.add_patch(FancyBboxPatch((ax_c - atomic_w / 2, y_atomic - 0.55), atomic_w, 1.1,
                                boxstyle="round,pad=0,rounding_size=0.55", facecolor=TREE_YELLOW, edgecolor="none",
                                zorder=3))
    ax.text(ax_c, y_atomic + 0.2, "ATOMIC PROBLEM: IS THIS CRACK DANGEROUS, AND IS IT GROWING?", ha="center",
            va="center", fontsize=10.5, weight="bold", color=TREE_NAVY, zorder=4)
    ax.text(ax_c, y_atomic - 0.22, "one crack in one concrete element, with a scale, seen again → level, confidence, "
            "reason, growth", ha="center", va="center", fontsize=9.3, color=TREE_NAVY, zorder=4)

    # building path: straight down into the building risk score, joined by the atomic problem
    y_build = 2.45
    for lx in building_x:
        ax.plot([lx, lx], [y_start, y_build + 0.55], color=TREE_NAVY, lw=2.2, zorder=1)
    ax.annotate("", xy=(ax_c, y_build + 0.55), xytext=(ax_c, y_atomic - 0.55),
                arrowprops=dict(arrowstyle="-|>", color=TREE_YELLOW, lw=2.4, shrinkA=0, shrinkB=0,
                                mutation_scale=18), zorder=2)
    ax.add_patch(FancyBboxPatch((-0.6, y_build - 0.55), width + 1.2, 1.1, boxstyle="round,pad=0,rounding_size=0.55",
                                facecolor=TREE_NAVY, edgecolor="none", zorder=3))
    ax.text(centre, y_build + 0.2, "BUILDING RISK SCORE: WHICH BUILDING DOES AN ENGINEER VISIT FIRST?   "
            "P1 · P2 · P3", ha="center", va="center", fontsize=11, weight="bold", color="white", zorder=4)
    ax.text(centre, y_build - 0.22, "crack levels and growth from the atomic problem + building data (age, added floors, "
            "structure or use changed) + damage spread across elements", ha="center", va="center", fontsize=9.5,
            color="#dfe6f2", zorder=4)

    ax.legend(handles=[Line2D([], [], color=TREE_YELLOW, lw=4, label="Crack path → atomic problem (scales P, O)"),
                       Line2D([], [], color=TREE_NAVY, lw=4, label="Building path → building risk score (scale S)"),
                       Line2D([], [], color=TREE_GREY, lw=4, label="Context: why the need exists, not an input")],
              loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False, fontsize=11)
    ax.set_xlim(-1.0, width + 1.0)
    ax.set_ylim(0.9, 12.9)
    ax.set_aspect("equal")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.03)
    return fig


STAGES = ["Quality gate", "Material model (O)", "Element model (O)", "Crack segmentation (P)", "Measurement in mm (P)",
          "Pattern model (P)", "Building risk score (S)", "Agent: building data", "Triage rules sign-off",
          "Engineer review + retraining", "Evaluation (ground truth)"]
SOURCES = ["SDNET2018", "CrackSeg9k", "crack-seg\n(Ultralytics)", "METU", "PHI-Net", "CODEBRIM", "Haiti + Nepal\nsurveys",
           "Brick masonry\n(Darbhanga)", "Brick facades\n(Strathclyde)", "Masonry masks\n(Dais et al.)", "Pilot photos",
           "Engineer-\nlabelled photos", "Tripoli lists\n(106 / 114)", "Engineering\npartner"]
# From docs/data_map.md, section 1. Rows follow STAGES, columns follow SOURCES.
COVERAGE = [
    ["none", "none", "none", "none", "none", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["partial", "none", "none", "partial", "none", "partial", "none", "partial", "partial", "partial", "planned", "planned", "none", "none"],
    ["none", "none", "none", "none", "partial", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["none", "covered", "covered", "none", "none", "none", "none", "none", "none", "partial", "none", "planned", "none", "none"],
    ["none", "none", "none", "none", "none", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["none", "none", "none", "none", "partial", "partial", "none", "none", "none", "none", "none", "planned", "none", "none"],
    ["none", "none", "none", "none", "none", "none", "partial", "none", "none", "none", "none", "none", "partial", "planned"],
    ["none", "none", "none", "none", "none", "none", "partial", "none", "none", "none", "none", "none", "partial", "none"],
    ["none", "none", "none", "none", "none", "none", "partial", "none", "none", "none", "none", "none", "none", "planned"],
    ["none", "none", "none", "none", "none", "none", "none", "none", "none", "none", "none", "planned", "none", "planned"],
    ["none", "none", "none", "none", "none", "none", "partial", "none", "none", "none", "none", "planned", "partial", "planned"],
]
COVERAGE_LABEL = {"covered": "covers", "partial": "partly", "planned": "planned", "none": ""}


def data_coverage():
    fig, ax = plt.subplots(figsize=(21, 7.8))
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
    fig.text(0.02, 0.905, "Public data covers only crack segmentation (P); every other stage needs our own photos or an "
             "engineer. From docs/data_map.md, section 1 (27 Oct 2026).", fontsize=10, color=INK_2)
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
    ("Data", "Material model: concrete vs not, first test", 1, 1, False),
    ("Data", "Map public labels to the 7 patterns", 2, 3, False),
    ("Pilot", "Collect pilot photos: S, O, P scales", 2, 2, False),
    ("Pilot", "Prepare, label, tune quality gate", 2, 3, False),
    ("Pilot", "Scale card + width ± uncertainty (1st feature)", 3, 4, False),
    ("Models", "U-Net on CrackSeg9k + crack-seg", 3, 4, False),
    ("Models", "Element model (PHI-Net task 6)", 3, 4, False),
    ("Models", "Pattern model (PHI-Net tasks 3, 8)", 4, 5, False),
    ("Agent and MCP", "First MCP: OpenStreetMap building data", 3, 3, False),
    ("Agent and MCP", "Plan/build harness, MCP to all sources", 4, 5, False),
    ("Engineering partners", "Scope with EWB + structural engineer", 1, 2, False),
    ("Engineering partners", "Calibration: matrix, thresholds", 3, 5, True),
    ("Engineering partners", "Engineer-labelled photos + baseline", 4, 6, True),
    ("Integration", "Engineer review screen (mock-up)", 1, 2, False),
    ("Integration", "Building questionnaire + risk score (code)", 2, 3, False),
    ("Integration", "Beta: end-to-end on pilot photos", 4, 4, False),
    ("Integration", "Monitoring: crack IDs, stickers, revisit", 5, 5, False),
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
    fig, ax = plt.subplots(figsize=(14, 10.9))
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
