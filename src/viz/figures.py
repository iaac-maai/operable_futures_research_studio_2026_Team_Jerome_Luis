"""Figures for the 29 Oct deliverables. Spec: spec/features/figures.md.

Run from the repository root:  py src/viz/figures.py   (writes PNGs to figures/)
Every figure is drawn from the repo's own rules and data map. None shows a measured result.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from triage.matrix import BAND_NAMES, MATRIX, PATTERN_NAMES, PATTERNS

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
    fig, ax = _canvas(13, 5.2, "From phone photo to triage",
                      "Learned models suggest; written rules decide; a human confirms every High and every referral")
    learned, rules, human = (VIOLET, "#ecebfb"), (AQUA, "#e3f5ee"), (MUTED, "#f0efec")
    steps = [
        ("Phone photo\ncoin for scale, element tag", human),
        ("Quality gate\nblur, light, coin visible", rules),
        ("Detect and segment\nYOLO element, U-Net crack", learned),
        ("Measurement\nwidth, length, angle", rules),
        ("Pattern model\ncrack type + confidence", learned),
        ("AI agent\nbuilding data over MCP", learned),
        ("Triage rules\nsrc/triage/matrix.py", rules),
        ("Engineer\nconfirms High and referrals", human),
    ]
    w, h, gap = 2.6, 1.2, 0.6
    xs = [i * (w + gap) for i in range(4)]
    pos = [(x, 2.6) for x in xs] + [(x, 0.4) for x in reversed(xs)]
    for (text, (edge, fill)), (x, y) in zip(steps, pos):
        _box(ax, x, y, w, h, text, fill, edge)
    for i in range(3):
        _arrow(ax, (pos[i][0] + w, 3.2), (pos[i + 1][0], 3.2))
    _arrow(ax, (pos[3][0] + w / 2, 2.6), (pos[4][0] + w / 2, 1.6))
    for i in range(4, 7):
        _arrow(ax, (pos[i][0], 1.0), (pos[i + 1][0] + w, 1.0))
    ax.set_xlim(-0.2, xs[-1] + w + 0.2)
    ax.set_ylim(-0.5, 4.1)
    ax.legend(handles=[Patch(facecolor=f, edgecolor=e, label=l) for l, (e, f) in
                       [("Learned model", learned), ("Written rule, auditable", rules), ("Human or input", human)]],
              loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    return fig


def decision_flow():
    fig, ax = _canvas(12, 6.4, "Decision logic: every doubt ends at an expert",
                      "Order of checks in triage.matrix.assess(); Low is reachable only after both checks say yes")
    q_fill, q_edge = "#f0efec", MUTED
    _box(ax, 0, 5, 3.6, 1, "Image usable?\nblur, light, coin visible", q_fill, q_edge)
    _box(ax, 0, 3.2, 3.6, 1, "Pattern known, confidence ≥ 0.8,\nwidth measured?", q_fill, q_edge)
    _box(ax, 0, 1.4, 3.6, 1, "Look up pattern × width\nrisk matrix (illustrative)", q_fill, q_edge)
    _box(ax, 5.2, 5, 2.6, 1, "Retake", LEVEL["Retake"], LEVEL["Retake"], color="white", weight="bold")
    _box(ax, 5.2, 3.2, 2.6, 1, "Expert needed", LEVEL["Expert needed"], LEVEL["Expert needed"],
         color="white", weight="bold")
    for i, lvl in enumerate(["Low", "Medium", "High"]):
        x = -0.6 + i * 2.5
        sub = {"Low": "routine monitoring", "Medium": "low-cost advice, recheck", "High": "engineer must confirm"}[lvl]
        _box(ax, x, -0.6, 2.2, 1, f"{lvl}\n{sub}", LEVEL[lvl], LEVEL[lvl], color=ON_FILL.get(lvl, "white"),
             weight="bold", size=9)
        _arrow(ax, (1.8, 1.4), (x + 1.1, 0.4))
    _box(ax, 9.2, 1.9, 2.6, 1.6, "Engineer review\nevery High and\nevery Expert needed", "#f0efec", INK_2,
         weight="bold")
    _arrow(ax, (3.6, 5.5), (5.2, 5.5), "no")
    _arrow(ax, (3.6, 3.7), (5.2, 3.7), "no")
    _arrow(ax, (1.8, 5), (1.8, 4.2), "yes", (0.25, 0))
    _arrow(ax, (1.8, 3.2), (1.8, 2.4), "yes", (0.25, 0))
    _arrow(ax, (7.8, 3.7), (9.2, 3.0))
    _arrow(ax, (6.6, -0.1), (9.2, 2.2))
    ax.set_xlim(-0.8, 12)
    ax.set_ylim(-0.9, 6.3)
    return fig


def risk_matrix():
    fig, ax = plt.subplots(figsize=(10, 4.6))
    bands = list(MATRIX)
    for r, band in enumerate(bands):
        for c, pattern in enumerate(PATTERNS):
            lvl = MATRIX[band][c]
            ax.add_patch(FancyBboxPatch((c + 0.04, r + 0.06), 0.92, 0.88, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor=LEVEL[lvl], edgecolor="none"))
            ax.text(c + 0.5, r + 0.5, lvl, ha="center", va="center", weight="bold",
                    color=ON_FILL.get(lvl, "white"))
    ax.set_xlim(0, len(PATTERNS))
    ax.set_ylim(len(bands), 0)
    ax.set_xticks([c + 0.5 for c in range(len(PATTERNS))], [PATTERN_NAMES[p] for p in PATTERNS])
    ax.set_yticks([r + 0.5 for r in range(len(bands))], [BAND_NAMES[b] for b in bands])
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.suptitle("Risk matrix: crack width × pattern", x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.02, "Read from src/triage/matrix.py. Illustrative thresholds, to be calibrated with a "
             "structural engineer. Boundary widths go to the wider band.", fontsize=9, color=INK_2)
    fig.subplots_adjust(left=0.13, right=0.98, top=0.8, bottom=0.1)
    return fig


TREE = {
    "A. Buildings deteriorate\nunwatched": [("A1 Ageing, no maintenance", "tool"), ("A2 Added floors, poor ground", "tool"),
                                            ("A3 Soil erosion", "later"), ("A4 Unauthorised building", "out"),
                                            ("A5 Earthquake trigger", "out")],
    "B. Residents cannot\nread the signs": [("B1 Harmless vs structural", "tool"), ("B2 Wrong all-clear", "tool"),
                                            ("B3 Photo quality, scale", "tool"), ("B4 Rebar, foundations", "out")],
    "C. Too few engineers": [("C1 No ranked list", "tool"), ("C2 Reports not acted on", "tool"),
                             ("C3 Backlog: 114 buildings", "tool")],
    "D. Warnings overridden": [("D1 Owner says safe", "out"), ("D2 Work resumes after seal", "out"),
                               ("D3 Fear of eviction", "out")],
    "E. Data is scarce": [("E1 Concrete, pavement only", "tool"), ("E2 No engineer labels", "tool")],
}
ATOMIC_FROM = {"B1", "B2", "B3", "C1"}
SCOPE = {"tool": ("#e3f5ee", AQUA, "Tool works on it"), "later": ("#fdf0d0", "#c98500", "Phase 3"),
         "out": ("#f0efec", MUTED, "Out of scope")}


def segmentation_tree():
    fig, ax = _canvas(15, 8.4, "Problem segmentation tree",
                      "Macro → meso → micro → atomic. Bold outline: feeds the atomic problem. "
                      "Sources in docs/sources.md")
    w, h, col = 2.6, 0.62, 3.0
    _box(ax, 4.2, 7.0, 6.6, 0.8, "Macro: people cannot judge whether cracks\nin ageing buildings are dangerous",
         "#dfeaf8", BLUE, size=10.5, weight="bold")
    for i, (meso, kids) in enumerate(TREE.items()):
        x = i * col
        _box(ax, x, 5.5, w, 0.85, meso, "#f0efec", INK_2, weight="bold")
        ax.plot([7.5, x + w / 2], [7.0, 6.35], color=MUTED, lw=1)
        for j, (kid, scope) in enumerate(kids):
            fill, edge, _ = SCOPE[scope]
            y = 4.6 - j * 0.8
            bold = kid[:2] in ATOMIC_FROM
            _box(ax, x + 0.15, y, w - 0.3, h, kid, fill, edge, size=8.8, lw=2.8 if bold else 1.2,
                 weight="bold" if bold else "normal")
            ax.plot([x + 0.07, x + 0.07, x + 0.15], [5.5, y + h / 2, y + h / 2], color=MUTED, lw=1)
    _box(ax, 3.2, -0.2, 8.6, 0.8, "Atomic: one photo, one crack, one element → level + one-sentence reason\n"
         "(from B1, B2, B3 and C1)", "#e3f5ee", AQUA, size=10, weight="bold", lw=2.8)
    ax.legend(handles=[Patch(facecolor=f, edgecolor=e, label=l) for f, e, l in SCOPE.values()],
              loc="upper right", bbox_to_anchor=(1.0, 1.02), ncol=3, frameon=False)
    ax.set_xlim(-0.2, 4 * col + w + 0.2)
    ax.set_ylim(-0.4, 8.0)
    return fig


STAGES = ["Quality gate", "YOLO detector", "U-Net segmenter", "Measurement (mm)", "Pattern model",
          "Agent: building data", "Triage rules sign-off", "Evaluation (ground truth)"]
SOURCES = ["SDNET2018", "CrackSeg9k", "PHI-Net", "CODEBRIM", "Brick masonry\n(Darbhanga)", "Masonry masks\n(Dais et al.)",
           "Pilot photos", "Engineer-\nlabelled photos", "Tripoli lists\n(106 / 114)", "Engineering\npartner"]
# From docs/data_map.md, section 1. Rows follow STAGES, columns follow SOURCES.
COVERAGE = [
    ["none", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["none", "none", "partial", "partial", "none", "none", "planned", "planned", "none", "none"],
    ["none", "covered", "none", "none", "none", "partial", "none", "planned", "none", "none"],
    ["none", "none", "none", "none", "none", "none", "planned", "planned", "none", "none"],
    ["partial", "none", "partial", "partial", "partial", "none", "none", "planned", "none", "none"],
    ["none", "none", "none", "none", "none", "none", "none", "none", "partial", "none"],
    ["none", "none", "none", "none", "none", "none", "none", "none", "none", "planned"],
    ["none", "none", "none", "none", "none", "none", "none", "planned", "partial", "planned"],
]
COVERAGE_LABEL = {"covered": "covers", "partial": "partly", "planned": "planned", "none": ""}


def data_coverage():
    fig, ax = plt.subplots(figsize=(15, 5.8))
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
DATASETS = [("SDNET2018", 56_000, "56,000+  ·  CC BY 4.0  ·  concrete only, no masks"),
            ("PHI-Net", 36_413, "36,413  ·  CC BY-NC-SA 4.0  ·  post-earthquake, no masks"),
            ("CrackSeg9k", 9_255, "9,255  ·  CC0  ·  pixel masks, mostly pavement"),
            ("Brick masonry (Darbhanga)", 4_259, "4,259  ·  CC BY 4.0  ·  brick, one heritage building"),
            ("Pilot phone photos", 0, "0  ·  about 30 cracks this week  ·  no risk labels"),
            ("Engineer-labelled phone photos", 0, "0  ·  to collect in Phase 2  ·  the target data")]


def dataset_sizes():
    fig, ax = plt.subplots(figsize=(11, 4.6))
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
    fig.suptitle("Public crack data is large, but none of it is the data we need",
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
    ("Deliverables", "29 Oct deliverables + first real-data test", 1, 1, False),
    ("Data", "SDNET2018 through the quality gate", 1, 1, False),
    ("Data", "Download CrackSeg9k, Darbhanga, CODEBRIM", 2, 2, False),
    ("Data", "Map public labels to the 5 patterns", 2, 3, False),
    ("Pilot", "Collect pilot photos (~30 cracks)", 2, 2, False),
    ("Pilot", "Prepare and label pilot photos", 2, 3, False),
    ("Pilot", "Tune quality gate on pilot photos", 3, 4, False),
    ("Pilot", "Coin detection + width measurement", 4, 6, False),
    ("Models", "U-Net on CrackSeg9k + masonry", 3, 5, False),
    ("Models", "Pattern model (pre-trained)", 5, 7, False),
    ("Models", "YOLO element detector", 6, 8, False),
    ("Engineering partner", "Contact partners", 1, 2, False),
    ("Engineering partner", "Calibration: matrix, thresholds", 3, 6, True),
    ("Engineering partner", "Engineer-labelled photos", 6, 10, True),
    ("Integration", "End-to-end pipeline on pilot", 7, 8, False),
    ("Integration", "Streamlit prototype", 8, 9, False),
    ("Integration", "Evaluate vs baseline", 9, 10, True),
    ("Integration", "Write-up and figures", 9, 10, False),
]
# (x in weeks from 26 Oct, label, at risk); 29 Oct is the Thursday of week 1.
MILESTONES = [(0.5, "29 Oct\ndeliverables", False), (4, "Pilot done,\ngate tuned", False),
              (6, "Matrix\nsigned off", True), (8, "End-to-end\ndemo", False), (10, "First measured\nresults", True)]
WORKSTREAM_COLOURS = {"Deliverables": BLUE, "Data": "#eb6834", "Pilot": AQUA, "Models": "#eda100",
                      "Engineering partner": "#e87ba4", "Integration": "#008300"}
WEEK_STARTS = ["26 Oct", "2 Nov", "9 Nov", "16 Nov", "23 Nov", "30 Nov", "7 Dec", "14 Dec", "21 Dec", "28 Dec"]


def timeline():
    fig, ax = plt.subplots(figsize=(14, 8))
    n = len(PLAN)
    ax.axvspan(8, 10, color="#f0efec", zorder=0)
    ax.text(9, 5, "winter break\n(assumption)", ha="center", va="center", fontsize=9, color=INK_2)
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
    for x, label, risk in MILESTONES:
        ax.plot(x, -0.9, marker="D", ms=10, color=LEVEL["High"] if not risk else "white",
                markeredgecolor=LEVEL["High"], mew=1.8, zorder=3)
        ax.text(x, -1.55, label, ha="center", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(0, 10.45)
    ax.set_ylim(n - 0.4, -2.2)
    ax.set_xticks([w + 0.5 for w in range(10)], [f"W{w + 1}\n{d}" for w, d in enumerate(WEEK_STARTS)])
    ax.set_yticks(range(n), [t[1] for t in PLAN])
    ax.xaxis.tick_top()
    for w in range(11):
        ax.axvline(w, color=GRID, lw=0.6, zorder=0)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    handles = [Patch(facecolor=c, edgecolor=c, label=s) for s, c in WORKSTREAM_COLOURS.items()]
    handles.append(Patch(facecolor="white", edgecolor=INK_2, hatch="///", label="At risk: needs engineering partner"))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, -0.01), ncol=4, frameon=False)
    fig.suptitle("10-week plan, 26 Oct 2026 to 3 Jan 2027", x=0.02, ha="left", fontsize=14, weight="bold")
    fig.text(0.02, 0.935, "The engineering partner is the critical path. Fallback if none by week 4: evaluate on "
             "pilot photos only; the matrix stays illustrative. Source: spec/constitution/roadmap.md",
             fontsize=9.5, color=INK_2)
    fig.subplots_adjust(left=0.24, right=0.98, top=0.84, bottom=0.12)
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
