"""Text as SVG outlines, so every word renders the same in any browser and inside <img>.

Fonts are SIL OFL, fetched from google/fonts on first use into .github/sky/fonts (gitignored).
Shaping is HarfBuzz, so kerning, ligatures and the Urdu Nastaliq name come out right.
"""
import os
import urllib.request
from functools import lru_cache

import uharfbuzz as hb

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
GF = "https://raw.githubusercontent.com/google/fonts/main/"
FONTS = {
    # name: (path in google/fonts, variation axes)
    "display": ("ofl/cormorantgaramond/CormorantGaramond[wght].ttf", {"wght": 600}),
    "display-bold": ("ofl/cormorantgaramond/CormorantGaramond[wght].ttf", {"wght": 700}),
    "serif": ("ofl/ebgaramond/EBGaramond[wght].ttf", {"wght": 500}),
    "serif-bold": ("ofl/ebgaramond/EBGaramond[wght].ttf", {"wght": 700}),
    "mono": ("ofl/ibmplexmono/IBMPlexMono-Medium.ttf", {}),
    "urdu": ("ofl/notonastaliqurdu/NotoNastaliqUrdu[wght].ttf", {"wght": 700}),
}


def _ensure(rel):
    path = os.path.join(FONT_DIR, os.path.basename(rel))
    if not os.path.exists(path):
        os.makedirs(FONT_DIR, exist_ok=True)
        url = GF + rel.replace("[", "%5B").replace("]", "%5D")
        with urllib.request.urlopen(url, timeout=60) as r, open(path, "wb") as fh:
            fh.write(r.read())
    return path


class _Pen:
    def __init__(self, x, y, s):
        self.d, self.x, self.y, self.s = [], x, y, s

    def _p(self, px, py):
        return f"{self.x + px * self.s:.1f} {self.y - py * self.s:.1f}"

    def moveTo(self, p):
        self.d.append("M" + self._p(*p))

    def lineTo(self, p):
        self.d.append("L" + self._p(*p))

    def qCurveTo(self, *pts):
        # HarfBuzz hands quadratic segments one control point at a time
        for i in range(0, len(pts) - 1):
            c = pts[i]
            e = pts[i + 1] if i + 1 == len(pts) - 1 else ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
            self.d.append("Q" + self._p(*c) + " " + self._p(*e))

    def curveTo(self, c1, c2, e):
        self.d.append("C" + self._p(*c1) + " " + self._p(*c2) + " " + self._p(*e))

    def closePath(self):
        self.d.append("Z")

    def endPath(self):
        pass


@lru_cache(None)
def _font(name):
    rel, axes = FONTS[name]
    blob = hb.Blob.from_file_path(_ensure(rel))
    face = hb.Face(blob)
    font = hb.Font(face)
    if axes:
        font.set_variations(axes)
    return font, face.upem


def _shape(text, name, features=None):
    font, upem = _font(name)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    return font, upem, buf.glyph_infos, buf.glyph_positions


def width(text, name, size, tracking=0.0):
    _, upem, _, pos = _shape(text, name)
    return sum(p.x_advance for p in pos) * size / upem + tracking * size * max(len(pos) - 1, 0)


def path(text, name, size, x, y, anchor="start", tracking=0.0):
    """SVG path data for `text` with its baseline at y. anchor: start, middle or end."""
    font, upem, infos, pos = _shape(text, name)
    s = size / upem
    w = width(text, name, size, tracking)
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    d, cx = [], x0
    for info, p in zip(infos, pos):
        pen = _Pen(cx + p.x_offset * s, y - p.y_offset * s, s)
        font.draw_glyph_with_pen(info.codepoint, pen)
        d += pen.d
        cx += p.x_advance * s + tracking * size
    return "".join(d)


def fit(text, name, size, max_width, tracking=0.0):
    """The largest size up to `size` at which `text` fits in `max_width`."""
    w = width(text, name, size, tracking)
    return size if w <= max_width else size * max_width / w


def glyph_d(name, gid):
    """One glyph's outline in font units, y pointing down, rounded to whole units."""
    font, _ = _font(name)
    pen = _Pen(0, 0, 1)
    font.draw_glyph_with_pen(gid, pen)
    out = []
    for seg in pen.d:
        cmd, rest = seg[0], seg[1:]
        nums = " ".join(str(round(float(v))) for v in rest.replace(",", " ").split()) if rest else ""
        out.append(cmd + nums)
    return "".join(out)


def runs(text, name, tracking=0.0):
    """(gid, x, y) in font units for each glyph, and the font's units per em."""
    _, upem, infos, pos = _shape(text, name)
    out, cx = [], 0
    for info, p in zip(infos, pos):
        out.append((info.codepoint, cx + p.x_offset, -p.y_offset))
        cx += p.x_advance + tracking * upem
    return out, upem, cx
