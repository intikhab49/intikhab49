"""Hero: the painted tailboard of a Pakistani truck, with bumper and swinging chains."""
from ta_core import (BLUE, CREAM, DGOLD, DGREEN, DRED, GOLD, GREEN, INK, NIGHT, ORANGE, PINK, PURPLE, RED, RNG,
                     SAFFRON, TEAL, WHITE, Doc, arc_brush, brush, n, petal_d, polar)
from ta_fonts import F
from ta_motifs import (TWINKLE, blossom, bud, chain, dots, glint, lamp, leaf, peacock, rose, sparkle, tape_defs,
                       vine)

RAISE = 64          # extra height for the crown; the rest of the board shifts down by this
W, H = 1280, 850 + RAISE
URDU = "nast"
UH = 136
X0, X1, YS, YB = 24, 1256, 96, 640
CX = W / 2


def board(k):
    """Tailboard outline inset by k, with a broad dome crest rising at the centre."""
    x0, x1, ys, yb = X0 + k, X1 - k, YS + k, YB - k
    r = max(6, 26 - k * 0.6)
    cl, cr = 300 + k * 0.9, 980 - k * 0.9
    top = 2 - RAISE + k
    sx, sy = 388 + k * 0.55, top + 42 - k * 0.05

    def L(px, py):
        return f"{n(px)} {n(py)}"

    def R(px, py):
        return f"{n(2 * CX - px)} {n(py)}"
    return (f"M{n(x0 + r)} {n(ys)}L{L(cl, ys)}"
            f"C{L(cl + 46, ys)} {L(sx - 14, sy + 52)} {L(sx, sy)}"
            f"C{L(sx + 30, top + 8)} {L(CX - 120, top)} {L(CX, top)}"
            f"C{R(CX - 120, top)} {R(sx + 30, top + 8)} {R(sx, sy)}"
            f"C{R(sx - 14, sy + 52)} {R(cl + 46, ys)} {R(cl, ys)}"
            f"L{n(x1 - r)} {n(ys)}Q{n(x1)} {n(ys)} {n(x1)} {n(ys + r)}L{n(x1)} {n(yb - r)}Q{n(x1)} {n(yb)} {n(x1 - r)} {n(yb)}"
            f"L{n(x0 + r)} {n(yb)}Q{n(x0)} {n(yb)} {n(x0)} {n(yb - r)}L{n(x0)} {n(ys + r)}Q{n(x0)} {n(ys)} {n(x0 + r)} {n(ys)}Z")


def vase(cx, top, s=1.0):
    """Brass guldasta vase with enamel bands; top = rim y."""
    def X(v):
        return n(cx + v * s)

    def Y(v):
        return n(top + v * s)
    body = (f"M{X(-26)} {Y(0)}L{X(26)} {Y(0)}L{X(20)} {Y(10)}C{X(56)} {Y(24)} {X(62)} {Y(62)} {X(30)} {Y(84)}"
            f"L{X(22)} {Y(92)}L{X(34)} {Y(100)}L{X(-34)} {Y(100)}L{X(-22)} {Y(92)}L{X(-30)} {Y(84)}"
            f"C{X(-62)} {Y(62)} {X(-56)} {Y(24)} {X(-20)} {Y(10)}Z")
    out = [f'<path d="{body}" fill="{INK}" stroke="{INK}" stroke-width="{n(8 * s)}" stroke-linejoin="round"/>',
           f'<path d="{body}" fill="url(#brass)"/>',
           f'<path d="M{X(-47)} {Y(40)}Q{X(0)} {Y(56)} {X(47)} {Y(40)}L{X(44)} {Y(54)}Q{X(0)} {Y(70)} {X(-44)} {Y(54)}Z" fill="{RED}" stroke="{INK}" stroke-width="{n(2.5 * s)}"/>',
           f'<path d="M{X(-36)} {Y(72)}Q{X(0)} {Y(84)} {X(36)} {Y(72)}" fill="none" stroke="{GREEN}" stroke-width="{n(6 * s)}"/>',
           f'<path d="M{X(-30)} {Y(4)}L{X(30)} {Y(4)}" stroke="{GOLD}" stroke-width="{n(5 * s)}" stroke-linecap="round"/>',
           f'<path d="{brush((cx - 30 * s, top + 22 * s), (cx - 44 * s, top + 34 * s), (cx - 44 * s, top + 60 * s), (cx - 26 * s, top + 80 * s), 7 * s)}" fill="#fff6c8" opacity=".9"/>']
    for i in range(5):
        out.append(f'<circle cx="{X(-30 + i * 15)}" cy="{Y(48 + (i % 2) * 2)}" r="{n(2.4 * s)}" fill="#fff"/>')
    return "".join(out)


def ribbon(doc, cx, cy, w, h, text):
    """Folded red ribbon banner with painted caps."""
    x0, x1 = cx - w / 2, cx + w / 2
    tail = h * 0.9
    out = []
    for side in (-1, 1):
        ex = x0 if side < 0 else x1
        tx = ex + side * tail * 1.4
        d = (f"M{n(ex)} {n(cy - h * 0.25)}L{n(tx)} {n(cy - h * 0.25)}L{n(tx - side * tail * 0.45)} {n(cy + h * 0.25)}"
             f"L{n(tx)} {n(cy + h * 0.75)}L{n(ex)} {n(cy + h * 0.75)}Z")
        out.append(f'<path d="{d}" fill="{DRED}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        fold = f"M{n(ex)} {n(cy + h * 0.5)}L{n(ex - side * tail * 0.55)} {n(cy + h * 0.75)}L{n(ex)} {n(cy + h * 0.75)}Z"
        out.append(f'<path d="{fold}" fill="#5c0710" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    band = f"M{n(x0)} {n(cy - h / 2)}Q{n(cx)} {n(cy - h / 2 - 10)} {n(x1)} {n(cy - h / 2)}L{n(x1)} {n(cy + h / 2)}Q{n(cx)} {n(cy + h / 2 - 10)} {n(x0)} {n(cy + h / 2)}Z"
    out.append(f'<path d="{band}" fill="{RED}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    out.append(f'<path d="M{n(x0 + 10)} {n(cy - h / 2 + 7)}Q{n(cx)} {n(cy - h / 2 - 3)} {n(x1 - 10)} {n(cy - h / 2 + 7)}" fill="none" stroke="#ff8a8f" stroke-width="3" opacity=".8"/>')
    out.append(dots(x0 + 14, cy + h / 2 - 8, x1 - 14, cy + h / 2 - 8, 16, 2.2, GOLD))
    doc.add("".join(out))
    doc.painted(F("tekob"), text, cx, cy + h * 0.22, h * 0.78, WHITE, ow=3.2, shadow=(2, 3), ls=0.04)


def build():
    d = Doc(W, H, "Intikhab Azam: AI/ML engineer, researcher and systems architect",
            "Painted in the style of Pakistani truck art: a decorated truck tailboard with reflective tape, two peacocks, "
            "a vase of roses, the name Intikhab Azam in Urdu and English, and swinging bumper chains.")
    d.keyframes("twinkle", TWINKLE)
    d.keyframes("spin", "to{transform:rotate(360deg)}")
    d.define('<linearGradient id="brass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a12"/>'
             '<stop offset=".35" stop-color="#ffd76a"/><stop offset=".6" stop-color="#d79a1e"/><stop offset="1" stop-color="#7a4a0a"/></linearGradient>',
             '<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/>'
             '<stop offset=".45" stop-color="#b9c3cf"/><stop offset=".55" stop-color="#7d8896"/><stop offset="1" stop-color="#e9eef3"/></linearGradient>',
             f'<radialGradient id="field" cx=".5" cy=".42" r=".65"><stop offset="0" stop-color="#1d1834"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient>',
             f'<linearGradient id="crest" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff3b3b"/><stop offset="1" stop-color="{DRED}"/></linearGradient>',
             f'<linearGradient id="plate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6dc"/><stop offset="1" stop-color="#f1d9a0"/></linearGradient>')
    tape = tape_defs(d, 30)

    # ---- board, reflective frame, field
    d.add(f'<path d="{board(0)}" fill="{INK}" transform="translate(0 8)" opacity=".35"/>')
    d.add(f'<path d="{board(0)}" fill="{INK}"/>')
    d.add(f'<path d="{board(5)}" fill="url(#{tape})"/>')
    d.define(f'<clipPath id="frame"><path d="{board(5)}"/></clipPath>')
    d.add(glint(d, "frame", X0, YS - 90, X1 - X0, YB - YS + 90, dur=6.5, band=120, angle=18, opacity=.7))
    d.add(f'<path d="{board(33)}" fill="{INK}"/>')
    d.add(f'<path d="{board(37)}" fill="{GOLD}"/>')
    d.add(f'<path d="{board(41)}" fill="url(#field)"/>')
    d.define(f'<clipPath id="inner"><path d="{board(41)}"/></clipPath>')

    # ---- crest: red arch with a turning sunburst behind the Urdu name
    floor = YS + 41
    rays = []
    for i in range(24):
        a0 = i * 15
        p1, p2 = polar(CX, 120, 420, a0), polar(CX, 120, 420, a0 + 7.5)
        rays.append(f'<path d="M{CX} 120L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}Z" fill="#ff7a45"/>')
    d.define(f'<clipPath id="crestclip"><path d="{board(41)}"/></clipPath><clipPath id="crestband"><rect x="0" y="{-RAISE - 10}" width="{W}" height="{floor + RAISE + 10}"/></clipPath>')
    d.add(f'<g clip-path="url(#crestclip)"><g clip-path="url(#crestband)"><rect x="260" y="{-RAISE - 10}" width="760" height="{floor + RAISE + 10}" fill="url(#crest)"/>'
          f'<g opacity=".5"><g style="transform-origin:{CX}px 120px;animation:spin 60s linear infinite">{"".join(rays)}</g></g></g></g>')
    d.add(f'<path d="M330 {floor}L950 {floor}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
          f'<path d="M334 {floor}L946 {floor}" stroke="{GOLD}" stroke-width="3"/>')
    d.add(dots(372, floor - 7, 908, floor - 7, 14, 2, "#ffe7a3"))
    U = F(URDU)
    us = 90
    while True:
        _, _, ub = U.layout("انتخاب اعظم", us)
        if ub[3] - ub[1] <= UH and ub[2] - ub[0] <= 400:
            break
        us -= 1
    uy = floor - 12 - ub[3]
    d.painted(U, "انتخاب اعظم", CX, uy, us, GOLD, ow=5.5, shadow=(3, 4), halo="#7a1010", hw=1.5, anchor="ink-middle")
    print("urdu size", us, "ink", [round(v) for v in (ub[2] - ub[0], ub[3] - ub[1])], "top", round(uy + ub[1]))
    for side in (-1, 1):
        d.add(leaf(CX + side * 222, floor - 52, 40, 13, -90 + side * 55) + leaf(CX + side * 222, floor - 52, 36, 12, 90 - side * 20))
        d.add(rose(CX + side * 222, floor - 52, 27, "pink" if side < 0 else "yellow", rot0=side * 15, seed=90 + side))
        d.add(blossom(CX + side * 262, floor - 18, 13, color=SAFFRON, center=RED))

    # halo of rays behind the bouquet, fading out
    d.define('<radialGradient id="halo"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".6"/>'
             '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
             f'<mask id="halomask"><circle cx="{CX}" cy="250" r="190" fill="url(#halo)"/></mask>')
    hr = []
    for i in range(32):
        p1, p2 = polar(CX, 250, 200, i * 11.25), polar(CX, 250, 200, i * 11.25 + 5.6)
        hr.append(f'<path d="M{CX} 250L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}Z" fill="#3b2f73"/>')
    d.add(f'<g mask="url(#halomask)"><g style="transform-origin:{CX}px 250px;animation:spin 90s linear infinite reverse">{"".join(hr)}</g></g>')

    # ---- peacocks facing the vase
    d.add(f'<g transform="translate(318 388) scale(.84)">{peacock(d, 3)}</g>')
    d.add(f'<g transform="translate(962 388) scale(-.84 .84)">{peacock(d, 5)}</g>')

    # ---- guldasta: vase of roses in the centre
    g = []
    for side in (-1, 1):
        g.append(vine((CX, 300), (CX + side * 40, 260), (CX + side * 70, 200), (CX + side * 108, 176), w=5))
        g.append(vine((CX, 300), (CX + side * 60, 296), (CX + side * 110, 270), (CX + side * 150, 268), w=4))
        g.append(bud(CX + side * 108, 176, 34, -90 + side * 40))
        g.append(bud(CX + side * 150, 268, 26, side * 10 if side > 0 else 170, color=PINK, light="#ffb3d1"))
        for k, (ang, L) in enumerate(((-150 if side < 0 else -30, 70), (-115 if side < 0 else -65, 64), (160 if side < 0 else 20, 58))):
            g.append(leaf(CX + side * 30, 262 - k * 6, L, 20, ang))
    g.append(rose(CX - 62, 252, 34, "yellow", rot0=10, seed=4))
    g.append(rose(CX + 62, 252, 34, "pink", rot0=-12, seed=5))
    g.append(rose(CX, 214, 46, "red", rot0=4, seed=6))
    g.append(rose(CX - 26, 280, 22, "white", rot0=30, seed=7))
    g.append(rose(CX + 28, 282, 22, "blue", rot0=8, seed=8))
    g.append(blossom(CX - 96, 214, 14, color=TEAL, center=SAFFRON))
    g.append(blossom(CX + 96, 214, 14, color=PURPLE, center=SAFFRON))
    g.append(vase(CX, 290, 0.95))
    d.add(f'<g clip-path="url(#inner)">{"".join(g)}</g>')

    # ---- sparkles in the field
    r = RNG(11)
    for i in range(14):
        sx = r.choice([r.uniform(90, 250), r.uniform(400, 520), r.uniform(760, 880), r.uniform(1030, 1190)])
        d.add(sparkle(sx, r.uniform(170, 360), r.uniform(6, 11), color=r.choice([WHITE, GOLD, "#bfe9ff"]),
                      dur=r.uniform(2.0, 3.4), delay=-r.uniform(0, 3)))

    # ---- name plate
    px0, px1, py0, py1 = 70, 1210, 398, 526
    d.add(f'<rect x="{px0}" y="{py0}" width="{px1 - px0}" height="{py1 - py0}" rx="18" fill="{INK}" transform="translate(0 6)" opacity=".5"/>')
    d.add(f'<rect x="{px0}" y="{py0}" width="{px1 - px0}" height="{py1 - py0}" rx="18" fill="url(#plate)" stroke="{INK}" stroke-width="6"/>')
    d.add(f'<rect x="{px0 + 10}" y="{py0 + 10}" width="{px1 - px0 - 20}" height="{py1 - py0 - 20}" rx="11" fill="none" stroke="{RED}" stroke-width="3"/>')
    d.add(dots(px0 + 26, py0 + 20, px1 - 26, py0 + 20, 18, 2.6, GREEN, RED))
    d.add(dots(px0 + 26, py1 - 20, px1 - 26, py1 - 20, 18, 2.6, RED, GREEN))
    for side in (-1, 1):
        ex = px0 + 44 if side < 0 else px1 - 44
        d.add(rose(ex, (py0 + py1) / 2, 26, "red", rot0=side * 20, seed=21 + side))
        d.add(leaf(ex, (py0 + py1) / 2 - 28, 30, 10, -90 - side * 30))
        d.add(leaf(ex, (py0 + py1) / 2 + 28, 30, 10, 90 + side * 30))
    name = "INTIKHAB AZAM"
    size = 104
    while F("ultra").width(name, size, 0.02) > 960:
        size -= 1
    rid, box = d.painted(F("ultra"), name, CX, 494, size, None, ow=6.5, shadow=(5, 6), shadow_fill="#5c0710", ls=0.02,
                         fills=[RED, "#f29100", GREEN, PINK, BLUE, ORANGE, TEAL, PURPLE, RED, GREEN, "#f29100", BLUE])
    # gloss sweep across the letters
    d.define(f'<mask id="namemask"><use href="#{rid}" fill="#fff"/></mask>')
    d.define('<linearGradient id="gloss" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    d.add(f'<g mask="url(#namemask)"><g transform="rotate(14 {n(box[0])} {n(box[1])})"><rect x="{n(box[0] - 140)}" y="{n(box[1] - 40)}" width="90" height="{n(box[3] - box[1] + 80)}" '
          f'fill="url(#gloss)" style="--d:{n(box[2] - box[0] + 300)}px;'
          f'animation:sweep 7s ease-in-out 1.2s infinite"/></g></g>')
    # highlight band on the top half of each letter
    d.define(f'<mask id="tophalf"><use href="#{rid}" fill="#fff"/><rect x="0" y="{n(box[1] + (box[3] - box[1]) * 0.42)}" width="{W}" height="200" fill="#000"/></mask>')
    d.add(f'<rect x="{n(box[0])}" y="{n(box[1])}" width="{n(box[2] - box[0])}" height="{n(box[3] - box[1])}" fill="#fff" opacity=".22" mask="url(#tophalf)"/>')

    # ---- ribbon with the titles
    ribbon(d, CX, 566, 820, 52, "AI/ML ENGINEER  ·  RESEARCHER  ·  SYSTEMS ARCHITECT")

    # ---- bumper, lamps, number plate
    by0, by1 = 656, 706
    d.add(f'<rect x="8" y="{by0}" width="{W - 16}" height="{by1 - by0}" rx="14" fill="{INK}"/>')
    d.add(f'<rect x="13" y="{by0 + 5}" width="{W - 26}" height="{by1 - by0 - 10}" rx="10" fill="url(#chrome)"/>')
    d.define('<pattern id="hazard" width="34" height="40" patternUnits="userSpaceOnUse" patternTransform="skewX(-35)">'
             f'<rect width="34" height="40" fill="#fff"/><rect width="17" height="40" fill="{RED}"/></pattern>')
    for xa, xb in ((120, 300), (W - 300, W - 120)):
        d.add(f'<rect x="{xa}" y="{by0 + 9}" width="{xb - xa}" height="{by1 - by0 - 18}" rx="4" fill="url(#hazard)" stroke="{INK}" stroke-width="3"/>')
    d.add(lamp(d, 70, (by0 + by1) / 2, 17, color="#ff3020", dur=1.3))
    d.add(lamp(d, W - 70, (by0 + by1) / 2, 17, color="#ff3020", dur=1.3, delay=0.65))
    d.painted(F("shri"), "dekh magar", 432, by1 - 15, 28, RED, ow=2.6, shadow=(1, 2))
    d.painted(F("shri"), "pyar se", W - 432, by1 - 15, 28, RED, ow=2.6, shadow=(1, 2))
    d.add(f'<rect x="{CX - 92}" y="{by0 + 6}" width="184" height="{by1 - by0 - 12}" rx="6" fill="#ffd400" stroke="{INK}" stroke-width="4"/>')
    d.text(F("tekob"), "INTIKHAB49", CX, by1 - 13, 36, fill=INK, anchor="middle", ls=0.05)

    # ---- chains hanging off the bumper
    r = RNG(5)
    xs = [40 + i * 50 for i in range(25)]
    kinds = ["leaf", "bell", "leaf", "bead", "leaf"]
    tones = [("#e9eef3", "#8d99a8"), ("#ffe08a", "#b8860b"), ("#ff8a96", "#a10012"), ("#9fe8a8", "#0a7a33")]
    for i, x in enumerate(xs):
        if abs(x - CX) < 100:
            continue
        d.add(chain(d, x, by1 - 2, links=5 + (i * 7) % 4, link=11, pendant=kinds[i % 5], tone=tones[i % 4],
                    swing=r.uniform(6, 11), dur=r.uniform(1.8, 2.6), delay=-r.uniform(0, 2.5)))
    d.body = [f'<g transform="translate(0 {RAISE})">{"".join(d.body)}</g>']
    return d


if __name__ == "__main__":
    import sys
    print(build().save(sys.argv[1] if len(sys.argv) > 1 else "../out/hero.svg"))
