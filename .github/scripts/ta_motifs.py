"""Truck-art motifs: florals, reflective tape, borders, hardware (chains, lights) and the peacock."""
import math

from ta_core import (bez, bez_d, BLUE, CREAM, DBLUE, DGOLD, DGREEN, DRED, GOLD, GREEN, INK, LGREEN, MAGENTA, ORANGE, PINK, PURPLE,
                     RED, RNG, SAFFRON, SILVER, TEAL, WHITE, arc_brush, brush, n, petal_d, polar, poly_d, rot)

ROSE_TONES = {
    "red": ("#7a0614", "#d1162b", "#ff5a6e", "#ffc2c9"),
    "pink": ("#8a0f4d", "#e0287a", "#ff7ab3", "#ffd6e8"),
    "yellow": ("#a35a00", "#f4a100", "#ffd23f", "#fff3b0"),
    "orange": ("#8f2a00", "#f05a00", "#ff9a3c", "#ffe0b8"),
    "blue": ("#0d1f6b", "#1f4fd8", "#5f8bff", "#cfe0ff"),
    "white": ("#8a7f86", "#e9e2ea", "#ffffff", "#ffffff"),
    "purple": ("#35105f", "#6a2bb8", "#a46bf0", "#e7d6ff"),
    "teal": ("#06505a", "#0f9fb0", "#4fd6e6", "#d3f8fc"),
}


def rose(cx, cy, R, tone="red", rot0=0.0, seed=1, outline=True):
    """Top-down truck-art rose: scalloped petal rings + C-stroke spiral + highlight commas."""
    dk, md, lt, hi = ROSE_TONES[tone]
    r = RNG(seed)
    out = []
    if outline:
        out.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(R * 1.05)}" fill="{INK}"/>')
    # outer petal ring
    k = 6
    for i in range(k):
        a = rot0 + i * 360 / k
        px, py = polar(cx, cy, R * 0.58, a)
        out.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="{n(R * 0.45)}" fill="{dk}"/>')
    for i in range(k):
        a = rot0 + i * 360 / k
        px, py = polar(cx, cy, R * 0.56, a)
        out.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="{n(R * 0.4)}" fill="{md}"/>')
        out.append(f'<path d="{arc_brush(px, py, R * 0.3, a - 75 + r.uniform(-8, 8), a + 70, R * 0.16)}" fill="{lt}"/>')
        out.append(f'<path d="{arc_brush(px, py, R * 0.33, a - 35, a + 25, R * 0.06)}" fill="{hi}"/>')
    # inner ring
    k2 = 5
    for i in range(k2):
        a = rot0 + 36 + i * 360 / k2
        px, py = polar(cx, cy, R * 0.3, a)
        out.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="{n(R * 0.3)}" fill="{dk}"/>')
        out.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="{n(R * 0.26)}" fill="{md}"/>')
        out.append(f'<path d="{arc_brush(px, py, R * 0.19, a - 70, a + 60, R * 0.1)}" fill="{lt}"/>')
    # spiral heart
    out.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(R * 0.27)}" fill="{dk}"/>')
    out.append(f'<path d="{arc_brush(cx, cy, R * 0.19, rot0 + 200, rot0 + 470, R * 0.12)}" fill="{md}"/>')
    out.append(f'<path d="{arc_brush(cx, cy, R * 0.2, rot0 + 230, rot0 + 330, R * 0.05)}" fill="{hi}"/>')
    out.append(f'<path d="{arc_brush(cx, cy, R * 0.09, rot0 + 30, rot0 + 300, R * 0.08)}" fill="{lt}"/>')
    out.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(R * 0.035)}" fill="{dk}"/>')
    return "".join(out)


def leaf(x0, y0, length, width, angle, tone=("#0a5c2e", GREEN, LGREEN), vein=True, hi=True):
    dk, md, lt = tone
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    tip = (x0 + ux * length, y0 + uy * length)
    out = [f'<path d="{petal_d(x0, y0, length, width, angle, roundness=0.45)}" fill="{INK}" '
           f'stroke="{INK}" stroke-width="{n(max(1.5, width * 0.18))}" stroke-linejoin="round"/>',
           f'<path d="{petal_d(x0, y0, length, width, angle, roundness=0.45)}" fill="{md}"/>']
    # dark half
    half = (f"M{n(x0)} {n(y0)}C{n(x0 + px * width * 0.9)} {n(y0 + py * width * 0.9)} "
            f"{n(x0 + ux * length * 0.45 + px * width)} {n(y0 + uy * length * 0.45 + py * width)} {n(tip[0])} {n(tip[1])}Z")
    out.append(f'<path d="{half}" fill="{dk}"/>')
    if vein:
        m0 = (x0 + ux * length * 0.08, y0 + uy * length * 0.08)
        out.append(f'<path d="{brush(m0, (m0[0] + ux * length * 0.3, m0[1] + uy * length * 0.3), (tip[0] - ux * length * 0.3, tip[1] - uy * length * 0.3), tip, max(1.2, width * 0.14), peak=0.3)}" fill="{lt}"/>')
    if hi:
        s0 = (x0 + ux * length * 0.25 - px * width * 0.55, y0 + uy * length * 0.25 - py * width * 0.55)
        s3 = (x0 + ux * length * 0.8 - px * width * 0.25, y0 + uy * length * 0.8 - py * width * 0.25)
        c = (x0 + ux * length * 0.55 - px * width * 0.75, y0 + uy * length * 0.55 - py * width * 0.75)
        out.append(f'<path d="{brush(s0, c, c, s3, max(1.4, width * 0.22), peak=0.35)}" fill="{WHITE}" opacity=".85"/>')
    return "".join(out)


def blossom(cx, cy, R, petals=5, color=PINK, center=SAFFRON, rot0=-90, dk=None):
    """Five-petal 'phool' with highlight dots."""
    dk = dk or INK
    out = []
    for i in range(petals):
        a = rot0 + i * 360 / petals
        out.append(f'<path d="{petal_d(cx, cy, R, R * 0.55, a, roundness=0.62)}" fill="{INK}" stroke="{INK}" stroke-width="{n(R * 0.16)}"/>')
    for i in range(petals):
        a = rot0 + i * 360 / petals
        out.append(f'<path d="{petal_d(cx, cy, R * 0.98, R * 0.52, a, roundness=0.62)}" fill="{color}"/>')
        hx, hy = polar(cx, cy, R * 0.62, a)
        out.append(f'<circle cx="{n(hx)}" cy="{n(hy)}" r="{n(R * 0.1)}" fill="{WHITE}" opacity=".9"/>')
    out.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(R * 0.26)}" fill="{center}" stroke="{INK}" stroke-width="{n(R * 0.07)}"/>')
    out.append(f'<circle cx="{n(cx - R * 0.07)}" cy="{n(cy - R * 0.07)}" r="{n(R * 0.08)}" fill="{WHITE}"/>')
    return "".join(out)


def bud(x, y, size, angle, color=RED, light="#ff8a96"):
    out = [f'<path d="{petal_d(x, y, size, size * 0.42, angle, roundness=0.4)}" fill="{color}" stroke="{INK}" stroke-width="{n(size * 0.08)}"/>']
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    out.append(f'<path d="{brush((x + ux * size * 0.2, y + uy * size * 0.2), (x + ux * size * 0.45 - uy * size * 0.15, y + uy * size * 0.45 + ux * size * 0.15), (x + ux * size * 0.7, y + uy * size * 0.7), (x + ux * size * 0.88, y + uy * size * 0.88), size * 0.14)}" fill="{light}"/>')
    for s in (-1, 1):
        out.append(f'<path d="{petal_d(x, y, size * 0.45, size * 0.14, angle + s * 28, roundness=0.4)}" fill="{GREEN}" stroke="{INK}" stroke-width="{n(size * 0.05)}"/>')
    return "".join(out)


def vine(p0, p1, p2, p3, w=5, color=DGREEN):
    return (f'<path d="M{n(p0[0])} {n(p0[1])}C{n(p1[0])} {n(p1[1])} {n(p2[0])} {n(p2[1])} {n(p3[0])} {n(p3[1])}" '
            f'fill="none" stroke="{INK}" stroke-width="{n(w + 3)}" stroke-linecap="round"/>'
            f'<path d="M{n(p0[0])} {n(p0[1])}C{n(p1[0])} {n(p1[1])} {n(p2[0])} {n(p2[1])} {n(p3[0])} {n(p3[1])}" '
            f'fill="none" stroke="{color}" stroke-width="{n(w)}" stroke-linecap="round"/>')


def dots(x0, y0, x1, y1, step, r, color=WHITE, alt=None):
    L = math.hypot(x1 - x0, y1 - y0)
    k = max(1, int(L // step))
    out = []
    for i in range(k + 1):
        t = i / k
        c = alt if (alt and i % 2) else color
        out.append(f'<circle cx="{n(x0 + (x1 - x0) * t)}" cy="{n(y0 + (y1 - y0) * t)}" r="{n(r)}" fill="{c}"/>')
    return "".join(out)


# ---------------------------------------------------------------- reflective tape (chamak patti)
TAPE = [("#f4f7fb", "#9aa7b8"), ("#ff2d3c", "#a10012"), ("#ffd400", "#c78a00"), ("#20c45a", "#0a7a33"),
        ("#2f7bff", "#0b3fb0"), ("#ff4fa3", "#b0105e"), ("#ff8a00", "#b84f00")]


def tape_defs(doc, h, colors=None, pid=None, kind="diamond"):
    """Pattern tile of reflective tape cut into diamonds + triangles. Returns pattern id; tile width = 2h."""
    colors = colors or TAPE
    pid = pid or doc.uid("tp")
    w = h * 2
    k = len(colors)
    grads = []
    for i, (lt, dk) in enumerate(colors):
        gid = f"{pid}g{i}"
        grads.append(gid)
        doc.define(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{lt}"/>'
                   f'<stop offset=".45" stop-color="{lt}"/><stop offset=".55" stop-color="{dk}"/><stop offset="1" stop-color="{lt}"/></linearGradient>')
    tile_w = w * k
    parts = [f'<rect width="{n(tile_w)}" height="{n(h)}" fill="{INK}"/>']
    g = h * 0.07
    for i in range(k):
        x = i * w
        c1 = f"url(#{grads[i]})"
        c2 = f"url(#{grads[(i + 3) % k]})"
        if kind == "diamond":
            parts.append(f'<path d="M{n(x + w / 2)} {n(g)}L{n(x + w - g * 1.6)} {n(h / 2)}L{n(x + w / 2)} {n(h - g)}L{n(x + g * 1.6)} {n(h / 2)}Z" fill="{c1}"/>')
            parts.append(f'<path d="M{n(x + g)} {n(g)}L{n(x + w / 2 - g * 1.7)} {n(g)}L{n(x + g)} {n(h / 2 - g * 0.9)}Z" fill="{c2}"/>')
            parts.append(f'<path d="M{n(x + w - g)} {n(g)}L{n(x + w / 2 + g * 1.7)} {n(g)}L{n(x + w - g)} {n(h / 2 - g * 0.9)}Z" fill="{c2}"/>')
            parts.append(f'<path d="M{n(x + g)} {n(h - g)}L{n(x + w / 2 - g * 1.7)} {n(h - g)}L{n(x + g)} {n(h / 2 + g * 0.9)}Z" fill="{c2}"/>')
            parts.append(f'<path d="M{n(x + w - g)} {n(h - g)}L{n(x + w / 2 + g * 1.7)} {n(h - g)}L{n(x + w - g)} {n(h / 2 + g * 0.9)}Z" fill="{c2}"/>')
            parts.append(f'<path d="M{n(x + w / 2)} {n(g * 3)}L{n(x + w / 2 + h * 0.18)} {n(h / 2)}" stroke="#fff" stroke-width="{n(h * 0.05)}" opacity=".8"/>')
        else:  # chevrons
            parts.append(f'<path d="M{n(x + g)} {n(g)}L{n(x + w / 2)} {n(h / 2)}L{n(x + g)} {n(h - g)}L{n(x + w / 2 - g)} {n(h - g)}'
                         f'L{n(x + w - g * 2)} {n(h / 2)}L{n(x + w / 2 - g)} {n(g)}Z" fill="{c1}"/>')
    doc.define(f'<pattern id="{pid}" width="{n(tile_w)}" height="{n(h)}" patternUnits="userSpaceOnUse">{"".join(parts)}</pattern>')
    return pid


def glint(doc, clip_id, x, y, w, h, dur=5.0, delay=0.0, band=None, angle=20, opacity=0.75):
    """A bright diagonal band that sweeps across the clipped shape (reflective shimmer)."""
    band = band or h * 0.9
    gid = doc.uid("gl")
    doc.define(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
               f'<stop offset=".5" stop-color="#fff" stop-opacity="{opacity}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    doc.keyframes("sweep", "0%{transform:translateX(0)}60%,100%{transform:translateX(var(--d))}")
    span = w + band * 3
    return (f'<g clip-path="url(#{clip_id})"><g transform="rotate({angle} {n(x)} {n(y + h / 2)})">'
            f'<rect x="{n(x - band * 1.5)}" y="{n(y - h)}" width="{n(band)}" height="{n(h * 3)}" fill="url(#{gid})" '
            f'style="--d:{n(span)}px;animation:sweep {dur}s ease-in-out {delay}s infinite"/></g></g>')


# ---------------------------------------------------------------- hardware
def chain(doc, x, y, links=7, link=11, pendant="leaf", color=SILVER, swing=8, dur=2.2, delay=0.0, tone=None, scale=1.0):
    """A dangling chain with a pendant; swings from (x, y)."""
    doc.keyframes("swing", "0%,100%{transform:rotate(var(--a))}50%{transform:rotate(calc(var(--a) * -1))}")
    L = link * scale
    out = []
    yy = y
    for i in range(links):
        if i % 2 == 0:
            out.append(f'<ellipse cx="{n(x)}" cy="{n(yy + L * 0.5)}" rx="{n(L * 0.32)}" ry="{n(L * 0.62)}" fill="none" stroke="{INK}" stroke-width="{n(L * 0.34)}"/>'
                       f'<ellipse cx="{n(x)}" cy="{n(yy + L * 0.5)}" rx="{n(L * 0.32)}" ry="{n(L * 0.62)}" fill="none" stroke="{color}" stroke-width="{n(L * 0.18)}"/>')
        else:
            out.append(f'<rect x="{n(x - L * 0.1)}" y="{n(yy - L * 0.1)}" width="{n(L * 0.2)}" height="{n(L * 1.2)}" rx="{n(L * 0.1)}" fill="{color}" stroke="{INK}" stroke-width="{n(L * 0.08)}"/>')
        yy += L * 0.95
    py = yy + L * 0.1
    tone = tone or (SILVER, "#8d99a8")
    if pendant == "leaf":
        s = L * 1.9
        d = (f"M{n(x)} {n(py)}C{n(x + s * 0.55)} {n(py + s * 0.35)} {n(x + s * 0.5)} {n(py + s * 0.95)} {n(x)} {n(py + s * 1.45)}"
             f"C{n(x - s * 0.5)} {n(py + s * 0.95)} {n(x - s * 0.55)} {n(py + s * 0.35)} {n(x)} {n(py)}Z")
        out.append(f'<path d="{d}" fill="{tone[0]}" stroke="{INK}" stroke-width="{n(L * 0.18)}"/>')
        out.append(f'<path d="M{n(x)} {n(py + s * 0.2)}L{n(x)} {n(py + s * 1.25)}" stroke="{tone[1]}" stroke-width="{n(L * 0.14)}"/>')
        out.append(f'<path d="{brush((x - s * 0.28, py + s * 0.45), (x - s * 0.33, py + s * 0.7), (x - s * 0.25, py + s * 0.95), (x - s * 0.1, py + s * 1.15), s * 0.12)}" fill="#fff" opacity=".85"/>')
    elif pendant == "bell":
        s = L * 1.5
        d = (f"M{n(x - s * 0.15)} {n(py)}L{n(x + s * 0.15)} {n(py)}C{n(x + s * 0.45)} {n(py + s * 0.2)} {n(x + s * 0.45)} {n(py + s * 0.8)} {n(x + s * 0.75)} {n(py + s * 1.1)}"
             f"L{n(x - s * 0.75)} {n(py + s * 1.1)}C{n(x - s * 0.45)} {n(py + s * 0.8)} {n(x - s * 0.45)} {n(py + s * 0.2)} {n(x - s * 0.15)} {n(py)}Z")
        out.append(f'<path d="{d}" fill="{GOLD}" stroke="{INK}" stroke-width="{n(L * 0.18)}"/>')
        out.append(f'<circle cx="{n(x)}" cy="{n(py + s * 1.22)}" r="{n(s * 0.18)}" fill="{DGOLD}" stroke="{INK}" stroke-width="{n(L * 0.12)}"/>')
        out.append(f'<path d="{brush((x - s * 0.28, py + s * 0.3), (x - s * 0.32, py + s * 0.55), (x - s * 0.36, py + s * 0.75), (x - s * 0.5, py + s * 0.98), s * 0.12)}" fill="#fff" opacity=".8"/>')
    elif pendant == "bead":
        out.append(f'<circle cx="{n(x)}" cy="{n(py + L * 0.6)}" r="{n(L * 0.7)}" fill="{tone[0]}" stroke="{INK}" stroke-width="{n(L * 0.16)}"/>'
                   f'<circle cx="{n(x - L * 0.22)}" cy="{n(py + L * 0.4)}" r="{n(L * 0.2)}" fill="#fff" opacity=".85"/>')
    return (f'<g style="--a:{swing}deg;transform-origin:{n(x)}px {n(y)}px;'
            f'animation:swing {dur}s ease-in-out {delay}s infinite">{"".join(out)}</g>')


def lamp(doc, cx, cy, r, color="#ff2a1a", core="#ffd0a0", dur=1.4, delay=0.0, blink=True):
    doc.keyframes("blink", "0%,45%{opacity:1}55%,100%{opacity:.18}")
    gid = doc.uid("lg")
    doc.define(f'<radialGradient id="{gid}"><stop offset="0" stop-color="{core}"/><stop offset=".45" stop-color="{color}"/>'
               f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
    anim = f' style="animation:blink {dur}s steps(1) {delay}s infinite"' if blink else ""
    return (f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 1.18)}" fill="#cfd6df" stroke="{INK}" stroke-width="{n(r * 0.12)}"/>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="#3a0a06"/>'
            f'<g{anim}><circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 1.9)}" fill="url(#{gid})" opacity=".55"/>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 0.92)}" fill="{color}"/>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 0.45)}" fill="{core}"/></g>'
            f'<path d="{arc_brush(cx, cy, r * 0.7, 200, 260, r * 0.22)}" fill="#fff" opacity=".85"/>')


def sparkle(cx, cy, r, color=WHITE, dur=2.4, delay=0.0):
    d = (f"M{n(cx)} {n(cy - r)}Q{n(cx + r * 0.12)} {n(cy - r * 0.12)} {n(cx + r)} {n(cy)}Q{n(cx + r * 0.12)} {n(cy + r * 0.12)} "
         f"{n(cx)} {n(cy + r)}Q{n(cx - r * 0.12)} {n(cy + r * 0.12)} {n(cx - r)} {n(cy)}Q{n(cx - r * 0.12)} {n(cy - r * 0.12)} {n(cx)} {n(cy - r)}Z")
    return (f'<path d="{d}" fill="{color}" style="transform-origin:{n(cx)}px {n(cy)}px;'
            f'animation:twinkle {dur}s ease-in-out {delay}s infinite"/>')


TWINKLE = "0%,100%{transform:scale(.15);opacity:0}50%{transform:scale(1) rotate(45deg);opacity:1}"


# ---------------------------------------------------------------- the peacock (faces right, feet at 0,0)
def peacock(doc, seed=3):
    r = RNG(seed)
    doc.keyframes("bob", "0%,100%{transform:rotate(0)}50%{transform:rotate(-5deg)}")
    doc.keyframes("sway", "0%,100%{transform:rotate(0)}50%{transform:rotate(2.2deg)}")
    doc.keyframes("eyes", "0%,100%{opacity:.25}50%{opacity:1}")
    out = []
    # tail: a long train that bows up, then falls to the ground behind the bird
    base = (-40, -104)
    tips = [(-250, -168), (-272, -128), (-282, -88), (-276, -50), (-258, -18), (-228, 4), (-190, 16), (-148, 20), (-104, 18)]
    tail, eyes = [], []
    greens = ["#0f7a3d", "#14924a", "#1aa653"]
    for i, tip in enumerate(tips):
        dx = base[0] - tip[0]
        c1 = (base[0] - dx * 0.35, base[1] - 34 + i * 2)
        c2 = (tip[0] + dx * 0.3, tip[1] - 26)
        tail.append(f'<path d="{brush(base, c1, c2, tip, 30, peak=0.7, tip1=8)}" fill="{INK}"/>')
        tail.append(f'<path d="{brush(base, c1, c2, tip, 24, peak=0.7, tip1=5)}" fill="{greens[i % 3]}"/>')
        tail.append(f'<path d="{brush(base, c1, c2, tip, 5, peak=0.5)}" fill="#9fe8a8" opacity=".7"/>')
        for t, sc in ((0.6, 0.55), (0.8, 0.75), (0.97, 1.0)):
            ex, ey = bez(base, c1, c2, tip, t)
            tx, ty = bez_d(base, c1, c2, tip, t)
            ang = math.degrees(math.atan2(ty, tx))
            tail.append(f'<g transform="translate({n(ex)} {n(ey)}) rotate({n(ang)}) scale({sc})">'
                        f'<ellipse rx="21" ry="14.5" fill="{INK}"/><ellipse rx="19" ry="13" fill="#a5d63a"/>'
                        f'<ellipse rx="14.5" ry="10" fill="#c08a1e"/><ellipse cx="1.5" rx="10.5" ry="7.5" fill="{TEAL}"/>'
                        f'<ellipse cx="3" rx="6" ry="5" fill="{DBLUE}"/></g>')
            eyes.append(f'<circle cx="{n(ex + 2 * sc)}" cy="{n(ey - 2 * sc)}" r="{n(3.4 * sc)}" fill="#fff"/>')
    out.append(f'<g style="transform-origin:{base[0]}px {base[1]}px;animation:sway 5s ease-in-out infinite">'
               f'{"".join(tail)}<g style="animation:eyes 2.6s ease-in-out infinite">{"".join(eyes)}</g></g>')
    # legs
    for lx in (-14, 8):
        out.append(f'<path d="M{lx} -66L{lx - 2} -6" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                   f'<path d="M{lx} -66L{lx - 2} -6" stroke="#d9a066" stroke-width="3.5" stroke-linecap="round"/>')
        for dx in (-12, 0, 11):
            out.append(f'<path d="M{lx - 2} -5L{lx - 2 + dx} 0" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                       f'<path d="M{lx - 2} -5L{lx - 2 + dx} 0" stroke="#d9a066" stroke-width="2.4" stroke-linecap="round"/>')
    # body
    out.append('<g transform="rotate(-24 -6 -112)">'
               f'<ellipse cx="-6" cy="-112" rx="52" ry="64" fill="{INK}"/>'
               f'<ellipse cx="-6" cy="-112" rx="47" ry="59" fill="{BLUE}"/>'
               f'<ellipse cx="4" cy="-118" rx="30" ry="44" fill="#2f6bff"/>')
    for row in range(5):
        for col in range(4):
            sx = -34 + col * 18 + (row % 2) * 9
            sy = -150 + row * 18
            out.append(f'<path d="M{sx - 7} {sy}Q{sx} {sy + 9} {sx + 7} {sy}" fill="none" stroke="{TEAL}" stroke-width="2.6" stroke-linecap="round" opacity=".9"/>')
    out.append('</g>')
    # folded wing: teal coverts with cream scallops, chestnut primaries
    wing = "M-60 -152C-22 -172 18 -142 8 -98C2 -72 -30 -60 -68 -72C-84 -100 -80 -134 -60 -152Z"
    out.append(f'<path d="{wing}" fill="{INK}" transform="translate(-2 3)"/><path d="{wing}" fill="#0e6f7c"/>')
    for row in range(4):
        for col in range(4 - row // 2):
            sx = -58 + col * 17 + (row % 2) * 8
            sy = -146 + row * 15
            out.append(f'<path d="M{sx - 8} {sy}Q{sx} {sy + 12} {sx + 8} {sy}" fill="none" stroke="#f6e7c1" stroke-width="3" stroke-linecap="round"/>')
    for k in range(4):
        y0 = -92 + k * 7
        out.append(f'<path d="{brush((-72 + k * 4, y0), (-50, y0 + 8), (-20, y0 + 10), (6 - k * 3, y0 - 2), 9, peak=0.4)}" fill="{["#b4471a", "#d9661f"][k % 2]}"/>')
    # neck + head (bobbing)
    head = []
    neck0, neck3 = (16, -158), (40, -246)
    head.append(f'<path d="{brush(neck0, (34, -190), (22, -222), neck3, 44, peak=0.2, tip1=24)}" fill="{INK}"/>')
    head.append(f'<path d="{brush(neck0, (34, -190), (22, -222), neck3, 36, peak=0.2, tip1=19)}" fill="{BLUE}"/>')
    head.append(f'<path d="{brush((24, -170), (40, -196), (30, -222), (44, -240), 12, peak=0.4)}" fill="{TEAL}" opacity=".9"/>')
    head.append(f'<circle cx="42" cy="-250" r="17" fill="{INK}"/><circle cx="42" cy="-250" r="14.5" fill="{BLUE}"/>')
    head.append('<path d="M52 -256L72 -250L52 -243Z" fill="#e8dcc0" stroke="#120d0a" stroke-width="2.5" stroke-linejoin="round"/>')
    head.append('<path d="M33 -258Q44 -264 54 -256" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
                '<path d="M34 -243Q44 -238 54 -245" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>')
    head.append('<circle cx="46" cy="-251" r="4.6" fill="#120d0a"/><circle cx="47.5" cy="-252.5" r="1.6" fill="#fff"/>')
    for k in range(5):
        a = -122 + k * 14
        tip = polar(40, -264, 34 + (k % 2) * 6, a)
        head.append(f'<path d="M40 -264L{n(tip[0])} {n(tip[1])}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
        head.append(f'<path d="{petal_d(tip[0], tip[1], 13, 5.5, a, base=-3)}" fill="{TEAL}" stroke="{INK}" stroke-width="2"/>')
        head.append(f'<circle cx="{n(tip[0])}" cy="{n(tip[1])}" r="2.2" fill="{GOLD}"/>')
    out.append(f'<g style="transform-origin:20px -165px;animation:bob 3.2s ease-in-out infinite">{"".join(head)}</g>')
    return "".join(out)
