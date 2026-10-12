"""SVG pieces shared by every image: the painted layer, twinkling stars, meteors and outlined text.

Animations are CSS keyframes, which run inside <img> on GitHub. Everything stops for
prefers-reduced-motion.
"""
import base64
import io
import random
from html import escape

import type as T

STYLE = """
@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}
@keyframes breathe{0%,100%{opacity:.0}50%{opacity:.55}}
@keyframes shimmer{0%,100%{opacity:0}50%{opacity:.38}}
@keyframes glint{0%,100%{stroke-opacity:.4}50%{stroke-opacity:.75}}
@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes draw{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:0}}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.tw{animation:tw ease-in-out infinite}
.breathe{animation:breathe 9s ease-in-out infinite}
.shimmer{animation:shimmer ease-in-out infinite}
.glint{animation:glint ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.tw{opacity:.8}}
"""


def jpeg(img, quality=86):
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True, subsampling=0)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def open_svg(w, h, title, desc, extra_style=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>',
            f"<style>{STYLE}{extra_style}</style>",
            '<defs><radialGradient id="sg"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff6e8" '
            'stop-opacity=".9"/><stop offset="1" stop-color="#cfd9ff" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".85" stop-color="#e8eeff" stop-opacity=".85"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            '<filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
            '<filter id="blur2" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="1.6"/></filter>'
            "</defs>"]


def painting(uri, w, h):
    return f'<image href="{uri}" width="{w}" height="{h}" preserveAspectRatio="none"/>'


def twinkles(points, scale, seed, size=1.0):
    """A glow on top of painted stars, pulsing at different speeds."""
    rng = random.Random(seed)
    out = ['<g>']
    for x, y, r in points:
        rr = max(2.2, r * scale * 3.2) * size
        dur = rng.uniform(2.4, 6.5)
        out.append(f'<circle class="tw" cx="{x * scale:.1f}" cy="{y * scale:.1f}" r="{rr:.1f}" fill="url(#sg)" '
                   f'style="animation-duration:{dur:.1f}s;animation-delay:-{rng.uniform(0, dur):.1f}s"/>')
    out.append("</g>")
    return "".join(out)


def meteors(specs):
    """specs: (x, y, angle_deg, length, period_s, delay_s). Each streak crosses once per period."""
    out = []
    for i, (x, y, ang, length, period, delay) in enumerate(specs):
        travel = length * 2.2
        out.append(f"<style>@keyframes m{i}{{0%{{transform:translateX(0);opacity:0}}"
                   f"1%{{opacity:1}}7%{{transform:translateX({travel:.0f}px);opacity:0}}"
                   f"100%{{transform:translateX({travel:.0f}px);opacity:0}}}}</style>")
        out.append(f'<g transform="translate({x} {y}) rotate({ang})"><line x1="{-length}" y1="0" x2="0" y2="0" '
                   f'stroke="url(#mg)" stroke-width="2.2" stroke-linecap="round" opacity="0" '
                   f'style="animation:m{i} {period}s linear infinite;animation-delay:{delay}s"/></g>')
    return "".join(out)


_GLYPHS = {}
_FONT_IDS = {}
_TEXT_N = [0]


def text(s, font, size, x, y, fill, anchor="start", glow=None, tracking=0.0, opacity=1.0):
    """Outlined text. Each glyph is defined once per image and reused; the glow reuses the whole line."""
    gl, upem, adv = T.runs(s, font, tracking)
    scale = size / upem
    x0 = x - (adv * scale / 2 if anchor == "middle" else adv * scale if anchor == "end" else 0)
    fid = _FONT_IDS.setdefault(font, f"f{len(_FONT_IDS)}")
    uses = []
    for gid, gx, gy in gl:
        key = f"{fid}g{gid}"
        if key not in _GLYPHS:
            _GLYPHS[key] = T.glyph_d(font, gid)
        if _GLYPHS[key]:
            uses.append(f'<use href="#{key}" x="{gx:.0f}"' + (f' y="{gy:.0f}"' if gy else "") + "/>")
    _TEXT_N[0] += 1
    tid = f"t{_TEXT_N[0]}"
    body = f'<g id="{tid}" transform="translate({x0:.1f} {y:.1f}) scale({scale:.5f})">{"".join(uses)}</g>'
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    halo = f'<use href="#{tid}" fill="{glow}" filter="url(#soft)" opacity=".75"/>' if glow else ""
    return f'{halo}<g fill="{fill}"{op}>{body}</g>'


def close(parts):
    defs = "".join(f'<path id="{k}" d="{d}"/>' for k, d in _GLYPHS.items())
    _GLYPHS.clear()
    _FONT_IDS.clear()
    _TEXT_N[0] = 0
    return "".join(parts) + (f"<defs>{defs}</defs>" if defs else "") + "</svg>\n"
