"""Truck-art SVG toolkit: document builder, text-as-paths, brush strokes.

Every word is drawn as glyph outlines (shaped by HarfBuzz) so the lettering renders
identically everywhere GitHub shows an image; glyphs are defined once per file and reused.
"""
import io
import math
import os
import random

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("TA_FONTS", os.path.join(HERE, "fonts"))

# ---------------------------------------------------------------- palette
INK = "#120d0a"      # outline black (warm)
NIGHT = "#0d0b16"    # panel ground
CREAM = "#f6e7c1"
PAPER = "#fbf3dc"
RED = "#e0262b"
DRED = "#9b0f1a"
SAFFRON = "#ffb400"
GOLD = "#f2c14e"
DGOLD = "#b8860b"
GREEN = "#1fa34a"
DGREEN = "#0b6b3a"
LGREEN = "#7fdc5a"
BLUE = "#1f4fd8"
DBLUE = "#13277a"
TEAL = "#16b3c4"
PINK = "#ff3e8a"
MAGENTA = "#c2187a"
ORANGE = "#ff6a00"
PURPLE = "#6a2bb8"
WHITE = "#ffffff"
SILVER = "#dfe6ee"


def n(v):
    """Compact number for SVG output."""
    v = round(v, 1)
    if v == int(v):
        return str(int(v))
    return f"{v:.1f}"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


# ---------------------------------------------------------------- fonts
class Font:
    def __init__(self, file, key, wght=None):
        path = file if os.path.isabs(file) else os.path.join(FONT_DIR, file)
        tt = TTFont(path)
        if "fvar" in tt and wght:
            from fontTools.varLib.instancer import instantiateVariableFont
            tt = instantiateVariableFont(tt, {"wght": wght})
        buf = io.BytesIO()
        tt.save(buf)
        data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.key = key
        self.upem = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.hb = hb.Font(hb.Face(data))
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or int(self.upem * 0.7)
        self.xh = getattr(os2, "sxHeight", 0) or int(self.upem * 0.5)
        self.asc = self.tt["hhea"].ascent
        self.desc = self.tt["hhea"].descent
        self._paths = {}
        self._bounds = {}

    def glyph_d(self, gid):
        if gid not in self._paths:
            pen = SVGPathPen(self.gs, ntos=lambda v: n(v))
            self.gs[self.order[gid]].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
            self._paths[gid] = pen.getCommands()
        return self._paths[gid]

    def glyph_bounds(self, gid):
        if gid not in self._bounds:
            bp = BoundsPen(self.gs)
            self.gs[self.order[gid]].draw(bp)
            self._bounds[gid] = bp.bounds  # y-up font units, or None
        return self._bounds[gid]

    def shape(self, text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, features or {"kern": True, "liga": True})
        out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((info.codepoint, pos.x_advance, pos.x_offset, pos.y_offset, info.cluster))
        return out

    def layout(self, text, size, ls=0.0, features=None):
        """Glyph placements in px relative to the pen origin, plus advance width and ink box."""
        s = size / self.upem
        x = 0.0
        out = []
        x0 = y0 = 1e9
        x1 = y1 = -1e9
        glyphs = self.shape(text, features)
        for i, (gid, adv, xo, yo, cl) in enumerate(glyphs):
            gx = (x + xo * s)
            gy = -yo * s
            b = self.glyph_bounds(gid)
            if b:
                bx0, by0, bx1, by1 = b
                x0 = min(x0, gx + bx0 * s)
                x1 = max(x1, gx + bx1 * s)
                y0 = min(y0, gy - by1 * s)
                y1 = max(y1, gy - by0 * s)
                out.append((gid, gx, gy, cl))
            x += adv * s
            if i < len(glyphs) - 1:
                x += ls * size
        if x0 > x1:
            x0 = x1 = y0 = y1 = 0
        return out, x, (x0, y0, x1, y1)

    def width(self, text, size, ls=0.0):
        return self.layout(text, size, ls)[1]


# ---------------------------------------------------------------- document
class Doc:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.defs, self.css, self.body = [], [], []
        self._ids = {}
        self._glyphs = set()
        self._keyframes = set()

    def uid(self, prefix="i"):
        self._ids[prefix] = self._ids.get(prefix, 0) + 1
        return f"{prefix}{self._ids[prefix]}"

    def add(self, *parts):
        self.body.extend(parts)

    def define(self, *parts):
        self.defs.extend(parts)

    def style(self, css):
        self.css.append(css)

    def keyframes(self, name, frames):
        if name not in self._keyframes:
            self._keyframes.add(name)
            self.css.append(f"@keyframes {name}{{{frames}}}")

    # ---- text as paths
    def _glyph(self, font, gid):
        ref = f"{font.key}{gid}"
        if ref not in self._glyphs:
            self._glyphs.add(ref)
            self.defs.append(f'<path id="{ref}" d="{font.glyph_d(gid)}"/>')
        return ref

    def text_def(self, font, text, x, y, size, anchor="start", ls=0.0, features=None, per_glyph=None):
        """Define a text run in <defs>; returns (id, ink box, advance). Draw it with paint layers via use_text().
        per_glyph: optional list of extra attributes applied cyclically to visible glyphs."""
        places, adv, box = font.layout(text, size, ls, features)
        if anchor == "middle":
            dx = -adv / 2
        elif anchor == "end":
            dx = -adv
        elif anchor == "ink-middle":
            dx = -(box[0] + box[2]) / 2
        else:
            dx = 0
        s = size / font.upem
        rid = self.uid("t")
        uses = []
        for k, (gid, gx, gy, cl) in enumerate(places):
            ref = self._glyph(font, gid)
            extra = ""
            if per_glyph:
                extra = " " + per_glyph[k % len(per_glyph)]
            uses.append(f'<use href="#{ref}" transform="translate({n(gx)} {n(gy)}) scale({s:.5f})"{extra}/>')
        self.defs.append(f'<g id="{rid}" transform="translate({n(x + dx)} {n(y)})">{"".join(uses)}</g>')
        bx = (x + dx + box[0], y + box[1], x + dx + box[2], y + box[3])
        return rid, bx, adv

    def text(self, font, text, x, y, size, fill=INK, anchor="start", ls=0.0, extra=""):
        rid, box, adv = self.text_def(font, text, x, y, size, anchor, ls)
        self.add(f'<use href="#{rid}" fill="{fill}"{extra}/>')
        return box

    def painted(self, font, text, x, y, size, fill, outline=INK, ow=None, shadow=(4, 5), shadow_fill=INK,
                inline=None, iw=None, anchor="middle", ls=0.0, extra_layers="", fills=None, halo=None, hw=None):
        """Sign-painter lettering: offset shadow, fat outline, optional halo, fill (or per-letter fills), inline."""
        rid, box, adv = self.text_def(font, text, x, y, size, anchor, ls)
        ow = ow if ow is not None else size * 0.12
        out = []
        if shadow:
            out.append(f'<use href="#{rid}" fill="{shadow_fill}" stroke="{shadow_fill}" stroke-width="{n(ow * 2)}" '
                       f'stroke-linejoin="round" transform="translate({n(shadow[0])} {n(shadow[1])})"/>')
        out.append(f'<use href="#{rid}" fill="{outline}" stroke="{outline}" stroke-width="{n(ow * 2)}" stroke-linejoin="round"/>')
        if halo:
            out.append(f'<use href="#{rid}" fill="{halo}" stroke="{halo}" stroke-width="{n(hw or ow * 0.8)}" stroke-linejoin="round"/>')
        if fills:
            cid, _, _ = self.text_def(font, text, x, y, size, anchor, ls,
                                      per_glyph=[f'fill="{c}"' for c in fills])
            out.append(f'<use href="#{cid}"/>')
        else:
            out.append(f'<use href="#{rid}" fill="{fill}"/>')
        if extra_layers:
            out.append(extra_layers.replace("@RID", rid))
        if inline:
            out.append(f'<use href="#{rid}" fill="none" stroke="{inline}" stroke-width="{n(iw or size * 0.025)}" '
                       f'stroke-linejoin="round" opacity=".9"/>')
        self.add(*out)
        return rid, box

    def render(self):
        css = "".join(self.css)
        css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" role="img" aria-labelledby="ttl dsc">'
                f'<title id="ttl">{esc(self.title)}</title><desc id="dsc">{esc(self.desc)}</desc>'
                f'<style>{css}</style><defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = self.render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        return len(data.encode())


# ---------------------------------------------------------------- geometry
def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
            u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1])


def bez_d(p0, p1, p2, p3, t):
    u = 1 - t
    return (3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
            3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]))


def smooth_closed(pts):
    """Closed polygon -> smooth path through edge midpoints (quadratic)."""
    m = len(pts)
    mids = [((pts[i][0] + pts[(i + 1) % m][0]) / 2, (pts[i][1] + pts[(i + 1) % m][1]) / 2) for i in range(m)]
    d = [f"M{n(mids[-1][0])} {n(mids[-1][1])}"]
    for i in range(m):
        d.append(f"Q{n(pts[i][0])} {n(pts[i][1])} {n(mids[i][0])} {n(mids[i][1])}")
    return "".join(d) + "Z"


def poly_d(pts, close=True):
    d = "M" + " ".join(f"{n(x)} {n(y)}" for x, y in pts)
    return d + ("Z" if close else "")


def brush(p0, p1, p2, p3, w, peak=0.45, steps=12, tip0=0.0, tip1=0.0):
    """Tapered one-stroke brush mark along a cubic; returns path d. peak = where it is fattest."""
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        u = 0.5 * t / peak if t < peak else 0.5 + 0.5 * (t - peak) / (1 - peak)
        ww = w * math.sin(math.pi * u) ** 0.85
        if i == 0:
            ww = max(ww, tip0)
        if i == steps:
            ww = max(ww, tip1)
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_d(p0, p1, p2, p3, t)
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        left.append((x + nx * ww / 2, y + ny * ww / 2))
        right.append((x - nx * ww / 2, y - ny * ww / 2))
    pts = left + right[::-1]
    return smooth_closed(pts)


def arc_brush(cx, cy, r, a0, a1, w, peak=0.5, steps=12):
    """Brush stroke along a circular arc (degrees)."""
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        u = 0.5 * t / peak if t < peak else 0.5 + 0.5 * (t - peak) / (1 - peak)
        ww = w * math.sin(math.pi * u) ** 0.8
        a = math.radians(a0 + (a1 - a0) * t)
        left.append((cx + (r + ww / 2) * math.cos(a), cy + (r + ww / 2) * math.sin(a)))
        right.append((cx + (r - ww / 2) * math.cos(a), cy + (r - ww / 2) * math.sin(a)))
    return smooth_closed(left + right[::-1])


def rot(p, a, c=(0, 0)):
    a = math.radians(a)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def polar(cx, cy, r, a):
    a = math.radians(a)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def petal_d(cx, cy, length, width, angle, base=0.0, roundness=0.55):
    """Teardrop petal from (cx,cy) pointing at angle (deg)."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    bx, by = cx + ux * base, cy + uy * base
    tx, ty = bx + ux * length, by + uy * length
    c1 = (bx + ux * length * roundness + px * width, by + uy * length * roundness + py * width)
    c2 = (bx + ux * length * roundness - px * width, by + uy * length * roundness - py * width)
    k = 0.9
    return (f"M{n(bx)} {n(by)}C{n(bx + px * width * k)} {n(by + py * width * k)} {n(c1[0])} {n(c1[1])} {n(tx)} {n(ty)}"
            f"C{n(c2[0])} {n(c2[1])} {n(bx - px * width * k)} {n(by - py * width * k)} {n(bx)} {n(by)}Z")


class RNG(random.Random):
    def j(self, v, amt):
        return v + self.uniform(-amt, amt)
