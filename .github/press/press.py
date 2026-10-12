"""Newspaper pieces: newsprint, rules, columns of text and the animations.

Every animation is written so that its resting state is the finished page. If a browser turns motion
off, or pauses an image before it plays, the reader still sees every word and figure.
"""
import base64
import io
import random

import numpy as np
from PIL import Image, ImageFilter

import svg
import type as T

INK, RED, PAPER = "#1d1b18", "#b3261e", "#efe6d2"


def newsprint(w, h, seed, fold=True):
    """Off-white newsprint: grain, fibres, a little yellowing at the edges and a fold down the middle."""
    rng = np.random.default_rng(seed)
    base = np.array([239, 230, 210], np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    grain = rng.normal(0, 5.5, (h, w))
    blot = np.asarray(Image.fromarray((rng.random((h // 24 + 2, w // 24 + 2)) * 255).astype(np.uint8))
                      .resize((w, h), Image.BICUBIC), np.float32) / 255 - 0.5
    edge = np.minimum(np.minimum(xx, w - xx), np.minimum(yy, h - yy)) / min(w, h)
    yellow = np.clip(0.12 - edge, 0, 0.12) / 0.12
    img = base[None, None] + grain[..., None] + blot[..., None] * 9
    img = img - yellow[..., None] * np.array([10, 16, 34], np.float32)
    # fibres: short faint strokes in random directions
    fib = Image.new("L", (w, h), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(fib)
    for _ in range(w * h // 900):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        a, L = rng.uniform(0, np.pi), rng.uniform(4, 14)
        d.line([(x, y), (x + L * np.cos(a), y + L * np.sin(a))], fill=int(rng.uniform(20, 60)), width=1)
    fib = np.asarray(fib.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    img = img - fib[..., None] * 18
    if fold:
        crease = np.exp(-((xx - w / 2) / 2.2) ** 2)
        shade = np.exp(-((xx - w / 2 - 6) / 10) ** 2)
        img = img - crease[..., None] * 14 - shade[..., None] * 6 + np.exp(-((xx - w / 2 + 4) / 3) ** 2)[..., None] * 6
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def jpeg(img, q=80):
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = """
@keyframes tick{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def open_page(w, h, title, desc, paper_uri, extra_css=""):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
             f'aria-labelledby="t d"><title id="t">{svg.escape(title)}</title><desc id="d">{svg.escape(desc)}</desc>',
             f"<style>{CSS}{extra_css}</style>",
             '<defs><filter id="ink" x="-2%" y="-2%" width="104%" height="104%">'
             '<feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="3" result="n"/>'
             '<feDisplacementMap in="SourceGraphic" in2="n" scale="0.9"/></filter>'
             '<filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
             '<filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
             '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="8" result="n"/>'
             '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 1.25" result="m"/>'
             '<feComposite in="SourceGraphic" in2="m" operator="in"/></filter></defs>',
             f'<image href="{paper_uri}" width="{w}" height="{h}" preserveAspectRatio="none"/>']
    return parts


def text(s, font, size, x, y, fill=INK, anchor="start", opacity=1.0):
    return svg.text(s, font, size, x, y, fill, anchor, None, 0.0, opacity)


def rule(x1, x2, y, weight=1.0, fill=INK):
    return f'<rect x="{x1:.1f}" y="{y - weight / 2:.1f}" width="{x2 - x1:.1f}" height="{weight:.2f}" fill="{fill}"/>'


def wrap(s, font, size, width):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if T.width(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def column(paragraphs, font, size, lead, x, y, width, fill=INK, indent=True):
    """Set paragraphs as one column. Returns (svg, y after the last line)."""
    out = []
    for k, para in enumerate(paragraphs):
        lines = wrap(("    " if indent and k else "") + para, font, size, width)
        for line in lines:
            out.append(text(line, font, size, x, y, fill))
            y += lead
        y += lead * 0.25
    return "".join(out), y


def flow(paragraphs, font, size, lead, x, y, width, cols, gap, max_lines):
    """Flow paragraphs across `cols` columns of at most `max_lines` lines each."""
    lines = []
    for k, para in enumerate(paragraphs):
        for line in wrap(para, font, size, width):
            lines.append(line)
        lines.append(None)                          # paragraph gap
    while lines and lines[-1] is None:
        lines.pop()
    out, c, row = [], 0, 0
    for line in lines:
        if row >= max_lines:
            c, row = c + 1, 0
            if c >= cols:
                raise ValueError(f"text does not fit in {cols} columns of {max_lines} lines")
            if line is None:
                continue
        if line is not None:
            out.append(text(line, font, size, x + c * (width + gap), y + row * lead))
            row += 1
        else:
            row += 0.4
    return "".join(out)


_N = [0]


def _uid(p):
    _N[0] += 1
    return f"{p}{_N[0]}"


def highlighter(x, y, w, h, period=9.0, delay=0.0, color="#f4d03f"):
    """A marker swipe behind a phrase; it re-draws itself every `period` seconds."""
    k = _uid("hl")
    css = (f"@keyframes {k}{{0%,100%{{transform:scaleX(1)}}3%{{transform:scaleX(0)}}14%{{transform:scaleX(1)}}}}"
           f".{k}{{transform-box:fill-box;transform-origin:left center;animation:{k} {period}s ease-in-out "
           f"{delay}s infinite}}")
    return (f"<style>{css}</style><rect class=\"{k}\" x=\"{x:.1f}\" y=\"{y:.1f}\" width=\"{w:.1f}\" height=\"{h:.1f}\" "
            f"fill=\"{color}\" opacity=\".72\" rx=\"2\" filter=\"url(#rough)\" style=\"mix-blend-mode:multiply\"/>")


def stamp(cx, cy, lines, rot=-9, period=11.0, delay=1.5, size=26):
    """A red rubber stamp that thuds down now and then. At rest it is simply there."""
    k = _uid("st")
    widths = [T.width(s, "head-bold", size) for s in lines]
    w = max(widths) + 40
    h = len(lines) * size * 1.15 + 26
    css = (f"@keyframes {k}{{0%,58%,100%{{transform:rotate({rot}deg) scale(1);opacity:.92}}"
           f"60%{{transform:rotate({rot - 4}deg) scale(1.9);opacity:0}}64%{{transform:rotate({rot}deg) scale(.94);"
           f"opacity:.95}}67%{{transform:rotate({rot}deg) scale(1.02)}}70%{{transform:rotate({rot}deg) scale(1)}}}}"
           f".{k}{{transform-box:fill-box;transform-origin:center;transform:rotate({rot}deg);opacity:.92;"
           f"animation:{k} {period}s ease-out {delay}s infinite}}")
    out = [f"<style>{css}</style><g class=\"{k}\"><g filter=\"url(#rough)\">",
           f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="none" '
           f'stroke="{RED}" stroke-width="4"/>',
           f'<rect x="{cx - w / 2 + 6:.1f}" y="{cy - h / 2 + 6:.1f}" width="{w - 12:.1f}" height="{h - 12:.1f}" rx="3" '
           f'fill="none" stroke="{RED}" stroke-width="1.5"/>']
    y = cy - h / 2 + 13 + size * 0.95
    for s in lines:
        out.append(text(s, "head-bold", size, cx, y, RED, "middle"))
        y += size * 1.15
    out.append("</g></g>")
    return "".join(out)


def splitflap(x, y, value, cw=30, ch=44, period=10.0, delay=0.0, size=30):
    """A split-flap board showing `value`. Every `period` seconds the digits spin and land again."""
    out = []
    digits = "0123456789"
    for i, c in enumerate(value):
        cx = x + i * (cw + 4)
        out.append(f'<rect x="{cx}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="#1f1d1a"/>')
        if c in digits:
            d = int(c)
            k = _uid("sf")
            cid = _uid("clip")
            start = (d + 5) % 10
            spins = (d - start) % 10 + 10
            seq = [(start + j) % 10 for j in range(spins + 1)]
            css = (f"@keyframes {k}{{0%,100%{{transform:translateY(-{spins * ch}px)}}"
                   f"2%{{transform:translateY(0)}}22%{{transform:translateY(-{spins * ch}px)}}}}"
                   f".{k}{{transform:translateY(-{spins * ch}px);animation:{k} {period}s steps({spins},end) "
                   f"{delay + i * 0.15:.2f}s infinite}}")
            out.append(f"<style>{css}</style><clipPath id=\"{cid}\"><rect x=\"{cx}\" y=\"{y}\" width=\"{cw}\" "
                       f"height=\"{ch}\"/></clipPath><g clip-path=\"url(#{cid})\"><g class=\"{k}\">")
            for j, dd in enumerate(seq):
                out.append(text(str(dd), "mono", size, cx + cw / 2, y + ch * 0.74 + j * ch, "#f3ead6", "middle"))
            out.append("</g></g>")
        else:
            out.append(text(c, "mono", size, cx + cw / 2, y + ch * 0.74, "#f3ead6", "middle"))
        out.append(f'<rect x="{cx}" y="{y + ch / 2 - 0.6}" width="{cw}" height="1.2" fill="#000" opacity=".55"/>')
    return "".join(out), len(value) * (cw + 4) - 4


def ticker(y, h, w, items, speed=70.0, label="LATEST"):
    """A black news ticker. The text scrolls; at rest it reads from the start."""
    sep = "   •   "
    line = sep.join(items) + sep
    tw = T.width(line, "mono", 18)
    dur = tw / speed
    k = _uid("tk")
    cid = _uid("clip")
    lw = T.width(label, "head-bold", 18) + 30
    css = f".{k}{{animation:tick {dur:.1f}s linear infinite}}"
    out = [f"<style>{css}</style>", f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="#151412"/>',
           f'<clipPath id="{cid}"><rect x="{lw}" y="{y}" width="{w - lw}" height="{h}"/></clipPath>',
           f'<g clip-path="url(#{cid})"><g class="{k}">',
           text(line + line, "mono", 18, lw + 16, y + h * 0.66, "#efe6d2"), "</g></g>",
           f'<rect x="0" y="{y}" width="{lw}" height="{h}" fill="{RED}"/>',
           text(label, "head-bold", 18, lw / 2, y + h * 0.68, "#fff", "middle")]
    return "".join(out)


def typewriter(inner_svg, x, y, w, h, period=12.0, delay=0.5):
    """Types a line out again every `period` seconds. Frame 0 and the resting state show the whole line."""
    k = _uid("tw")
    css = (f"@keyframes {k}{{0%,100%{{clip-path:inset(0 0 0 0)}}1%{{clip-path:inset(0 100% 0 0)}}"
           f"30%{{clip-path:inset(0 0 0 0)}}}}"
           f".{k}{{animation:{k} {period}s steps(48,end) {delay}s infinite}}")
    return f"<style>{css}</style><g class=\"{k}\">{inner_svg}</g>"


def breaking(x, y, label="BREAKING"):
    w = T.width(label, "head-bold", 17) + 34
    return (f'<rect x="{x}" y="{y - 19}" width="{w:.0f}" height="26" fill="{RED}"/>'
            f'<circle cx="{x + 12}" cy="{y - 6}" r="4.5" fill="#fff" style="animation:pulse 1.4s ease-in-out infinite"/>'
            + text(label, "head-bold", 17, x + 23, y, "#fff")), w
