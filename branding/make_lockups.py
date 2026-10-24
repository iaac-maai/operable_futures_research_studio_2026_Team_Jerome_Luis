"""Build the logo lockups (mark + "second look" wordmark) as SVG, text converted to outlines.

Same sizes and spacing as the logo canvas: mark on top, wordmark below, Space Grotesk SemiBold,
letter-spacing -0.03 em. Writes a light (ink on white) and a dark (white on ink) file per idea.

Usage, from the repository root (the font is not committed; download it from Google Fonts, SIL OFL):
    py branding/make_lockups.py <path to SpaceGrotesk SemiBold .ttf>
Needs: fonttools, uharfbuzz.
"""

import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

INK, WHITE = "#141414", "#FFFFFF"
TRACKING = -0.03  # em, as on the canvas
MARGIN = 48
OUT = Path(__file__).resolve().parent / "logos"

# Mark artwork from the canvas; {ink} and {ground} are filled per version.
MARK_LENSES = """<circle cx="32" cy="32" r="{r}" fill="none" stroke="{ink}" stroke-width="{w}"/>
<circle cx="96" cy="32" r="{r}" fill="none" stroke="{ink}" stroke-width="{w}"/>
<polyline points="{pts}" fill="none" stroke="{ground}" stroke-width="{gap}" stroke-linejoin="miter"/>
<polyline points="{pts}" fill="none" stroke="{ink}" stroke-width="{crack}" stroke-linejoin="miter"/>"""
MARK_STAIR = """<g stroke="{ink}" stroke-width="1.2" opacity="0.28" fill="none">
<rect x="6" y="6" width="108" height="108"/>
<path d="M6 20H114M6 34H114M6 48H114M6 62H114M6 76H114M6 90H114M6 104H114"/>
<path d="M34 6V20M80 6V20M20 20V34M57 20V34M96 20V34M34 34V48M80 34V48M20 48V62M57 48V62M96 48V62M34 62V76M80 62V76M20 76V90M57 76V90M96 76V90M34 90V104M80 90V104M20 104V114M57 104V114M96 104V114"/>
</g>
<path d="M26 20 H94 V48 H80 V62 H57 V76 H34 V90 H26 V100 H96" fill="none" stroke="{ink}" stroke-width="10" stroke-linejoin="miter" stroke-linecap="square"/>"""
CRACK = "4,26 22,38 34,34 50,56 70,62 84,80 100,84 116,106"
MARK_COIN = f"""<defs><clipPath id="lens{{key}}"><circle cx="60" cy="60" r="27"/></clipPath></defs>
<polyline points="{CRACK}" fill="none" stroke="{{ink}}" stroke-width="2.5" stroke-linejoin="miter"/>
<circle cx="60" cy="60" r="30" fill="{{ground}}" stroke="{{ink}}" stroke-width="6"/>
<g clip-path="url(#lens{{key}})"><polyline points="{CRACK}" fill="none" stroke="{{ink}}" stroke-width="2.5" stroke-linejoin="miter" transform="translate(60 60) scale(1.9) translate(-60 -60)"/></g>"""
MARK_PATH = """<polyline points="12,14 26,30 18,42 36,54 30,66 48,80" fill="none" stroke="{ink}" stroke-width="5" stroke-linejoin="miter"/>
<polyline points="48,80 104,80" fill="none" stroke="{ink}" stroke-width="9"/>
<polyline points="88,64 106,80 88,96" fill="none" stroke="{ink}" stroke-width="9" stroke-linejoin="miter"/>"""

BIG_LENSES = dict(r=24, w=8, pts="88,2 95,17 90,27 103,40 97,62", gap=7, crack=2.5)
WORD_LENSES = dict(r=22, w=11, pts="88,4 95,18 90,28 103,40 97,60", gap=8, crack=3)


class Font:
    def __init__(self, path: Path):
        self.tt = TTFont(path)
        self.upem = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.ascent, self.descent = self.tt["hhea"].ascent, -self.tt["hhea"].descent
        blob = hb.Blob.from_file_path(str(path))
        self.hb = hb.Font(hb.Face(blob))

    def shape(self, text: str, size: float):
        """Return (svg path d, width incl. tracking after every character) for text at size px, baseline y=0."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": False})
        scale, track = size / self.upem, TRACKING * size
        names = self.tt.getGlyphOrder()
        d, x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = SVGPathPen(self.glyphs)
            self.glyphs[names[info.codepoint]].draw(
                TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale)))
            d.append(pen.getCommands())
            x += pos.x_advance * scale + track
        return " ".join(c for c in d if c), x

    def line_box(self, size: float):
        """Baseline offset from the top of a line-height:1 box, as a browser centres the font's ascent+descent."""
        content = (self.ascent + self.descent) * size / self.upem
        return (size - content) / 2 + self.ascent * size / self.upem


def lockup(font, mark_svg, mark_vb, mark_w, mark_h, gap, size, word_parts, ink, ground):
    """mark centred above the wordmark; word_parts = list of ('text', str) or ('svg', inner, vb_w, vb_h, w, h, margin)."""
    pieces, x = [], 0.0
    for part in word_parts:
        if part[0] == "text":
            d, w = font.shape(part[1], size)
            pieces.append(("text", d, x))
            x += w
        else:
            _, inner, vbw, vbh, w, h, m = part
            pieces.append(("svg", inner, x + m, vbw, vbh, w, h))
            x += w + 2 * m
    word_w = x
    width = max(mark_w, word_w) + 2 * MARGIN
    top_text = MARGIN + mark_h + gap
    baseline = top_text + font.line_box(size)
    height = top_text + size + MARGIN
    word_x0 = (width - word_w) / 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" '
           f'width="{width:.0f}" height="{height:.0f}" role="img" aria-label="Second Look">',
           f'<rect width="{width:.1f}" height="{height:.1f}" fill="{ground}"/>',
           f'<g transform="translate({(width - mark_w) / 2:.2f} {MARGIN}) scale({mark_w / mark_vb[0]:.5f} {mark_h / mark_vb[1]:.5f})">'
           f'{mark_svg}</g>']
    for p in pieces:
        if p[0] == "text":
            out.append(f'<path transform="translate({word_x0 + p[2]:.2f} {baseline:.2f})" fill="{ink}" d="{p[1]}"/>')
        else:
            _, inner, px, vbw, vbh, w, h = p
            out.append(f'<g transform="translate({word_x0 + px:.2f} {baseline - h:.2f}) scale({w / vbw:.5f} {h / vbh:.5f})">'
                       f'{inner}</g>')
    out.append("</svg>")
    return "\n".join(out)


def build(font_path: Path) -> list[Path]:
    font = Font(font_path)
    written = []
    for tone, ink, ground in (("", INK, WHITE), ("_dark", WHITE, INK)):
        c = dict(ink=ink, ground=ground)
        word = [("text", "second look")]
        specs = {
            "01_two_lenses": (MARK_LENSES.format(**c, **BIG_LENSES), (128, 64), 280, 140, 40, 72,
                              [("text", "second l"), ("svg", MARK_LENSES.format(**c, **WORD_LENSES), 128, 64, 84, 42, 2),
                               ("text", "k")]),
            "02_stairstep_2": (MARK_STAIR.format(**c), (120, 120), 230, 230, 36, 64, [("text", "Second Look")]),
            "03_coin_lens": (MARK_COIN.format(**c, key=tone or "_light"), (120, 120), 230, 230, 36, 64, word),
            "04_crack_path": (MARK_PATH.format(**c), (120, 120), 230, 230, 36, 64, word),
        }
        for name, (mark, vb, mw, mh, gap, size, parts) in specs.items():
            path = OUT / f"{name}_lockup{tone}.svg"
            path.write_text(lockup(font, mark, vb, mw, mh, gap, size, parts, ink, ground) + "\n", encoding="utf-8")
            written.append(path)
    return written


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    for p in build(Path(sys.argv[1])):
        print(p)
