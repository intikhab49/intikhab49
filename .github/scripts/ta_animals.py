"""Card motifs. Each draws inside a 230 x 320 box (origin top-left) and returns SVG markup."""
import math

from ta_core import (BLUE, CREAM, DBLUE, DGOLD, DGREEN, DRED, GOLD, GREEN, INK, LGREEN, MAGENTA, ORANGE, PINK, PURPLE,
                     RED, RNG, SAFFRON, TEAL, WHITE, arc_brush, bez, bez_d, brush, n, petal_d, polar)
from ta_fonts import F
from ta_motifs import blossom, bud, dots, leaf, rose

BW, BH = 230, 320


def _label(doc, font, text, x, y, size, fill=INK, anchor="middle", outline=None, ow=3):
    rid, box, adv = doc.text_def(F(font), text, x, y, size, anchor=anchor)
    s = ""
    if outline:
        s += f'<use href="#{rid}" fill="{outline}" stroke="{outline}" stroke-width="{ow}" stroke-linejoin="round"/>'
    return s + f'<use href="#{rid}" fill="{fill}"/>', box


def cloud(x, y, s=1.0, fill="#ffffff"):
    parts = [(0, 0, 18), (20, -10, 22), (44, -2, 18), (60, 6, 13), (-16, 8, 12), (22, 8, 18)]
    c = "".join(f'<circle cx="{n(x + dx * s)}" cy="{n(y + dy * s)}" r="{n(r * s)}"/>' for dx, dy, r in parts)
    return (f'<g fill="{INK}" transform="translate(0 {n(3 * s)})" opacity=".25">{c}</g>'
            f'<g fill="{fill}">{c}</g>')


# ---------------------------------------------------------------- eagle (open-jev)
def eagle(doc):
    doc.keyframes("flapL", "0%,100%{transform:rotate(0)}50%{transform:rotate(-10deg)}")
    doc.keyframes("flapR", "0%,100%{transform:rotate(0)}50%{transform:rotate(10deg)}")
    doc.keyframes("tilt", "0%,100%{transform:rotate(0)}50%{transform:rotate(-6deg)}")
    cx = 115
    out = [cloud(22, 236, 0.9), cloud(150, 30, 0.7)]

    def wing(sign):
        S = (cx + sign * 16, 142)
        T = (cx + sign * 108, 30)
        c1, c2 = (cx + sign * 52, 104), (cx + sign * 88, 44)
        parts = []
        for j in reversed(range(10)):
            t = 0.18 + j * 0.088
            p = bez(S, c1, c2, T, t)
            L = 46 + j * 8.5
            ang = 90 - sign * (18 + j * 7.5)
            tip = polar(p[0], p[1], L, ang)
            q1 = polar(p[0], p[1], L * 0.35, ang + sign * 6)
            q2 = polar(p[0], p[1], L * 0.72, ang + sign * 3)
            parts.append(f'<path d="{brush(p, q1, q2, tip, 24, peak=0.38, tip1=5)}" fill="{INK}"/>')
            parts.append(f'<path d="{brush(p, q1, q2, tip, 19, peak=0.38, tip1=3)}" fill="{["#6b3a14", "#83491b"][j % 2]}"/>')
            parts.append(f'<path d="{brush(polar(p[0], p[1], 8, ang), q1, q2, polar(p[0], p[1], L * 0.86, ang), 5, peak=0.4)}" fill="#f2b33d"/>')
            wt = polar(p[0], p[1], L * 0.97, ang)
            parts.append(f'<circle cx="{n(wt[0])}" cy="{n(wt[1])}" r="3.2" fill="#fff"/>')
        for j in range(7):
            p = bez(S, c1, c2, T, 0.06 + j * 0.13)
            parts.append(f'<circle cx="{n(p[0])}" cy="{n(p[1] + 6)}" r="{n(15 - j)}" fill="{INK}"/>'
                         f'<circle cx="{n(p[0])}" cy="{n(p[1] + 6)}" r="{n(12.5 - j)}" fill="#a3622b"/>'
                         f'<path d="{arc_brush(p[0], p[1] + 6, 9 - j * 0.8, 200, 340, 4)}" fill="#ffd27a"/>')
        lead = f"M{n(S[0])} {n(S[1])}C{n(c1[0])} {n(c1[1])} {n(c2[0])} {n(c2[1])} {n(T[0])} {n(T[1])}"
        parts.append(f'<path d="{lead}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
                     f'<path d="{lead}" fill="none" stroke="#5a3412" stroke-width="4" stroke-linecap="round"/>')
        anim = "flapL" if sign < 0 else "flapR"
        return f'<g style="transform-origin:{n(S[0])}px {n(S[1])}px;animation:{anim} 1.8s ease-in-out infinite">{"".join(parts)}</g>'
    out.append(wing(-1))
    out.append(wing(1))
    # tail fan
    for k in range(5):
        a = 72 + k * 9
        tip = polar(cx, 222, 70, a)
        out.append(f'<path d="{petal_d(cx, 222, 70, 13, a, roundness=0.6)}" fill="{INK}" stroke="{INK}" stroke-width="5"/>'
                   f'<path d="{petal_d(cx, 222, 70, 13, a, roundness=0.6)}" fill="{CREAM}"/>'
                   f'<circle cx="{n(tip[0])}" cy="{n(tip[1])}" r="7" fill="#5a3412"/>')
    # body
    body = petal_d(cx, 236, 138, 44, -90, roundness=0.5)
    out.append(f'<path d="{body}" fill="{INK}" stroke="{INK}" stroke-width="8"/><path d="{body}" fill="#5a3412"/>')
    for row in range(6):
        for col in range(3 - (row == 5)):
            sx = cx - 18 + col * 18 + (row % 2) * 9 - (row == 5) * -9
            sy = 134 + row * 16
            out.append(f'<path d="M{n(sx - 8)} {n(sy)}Q{n(sx)} {n(sy + 11)} {n(sx + 8)} {n(sy)}" fill="none" stroke="#f2b33d" stroke-width="3" stroke-linecap="round"/>')
    # legs + ribbon
    for s in (-1, 1):
        out.append(f'<path d="M{cx + s * 14} 226L{cx + s * 22} 278" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                   f'<path d="M{cx + s * 14} 226L{cx + s * 22} 278" stroke="{SAFFRON}" stroke-width="5.5" stroke-linecap="round"/>')
    rb = "M14 278L216 278L206 292L216 306L14 306L24 292Z"
    out.append(f'<path d="{rb}" fill="{RED}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    t, _ = _label(doc, "tekob", "NOUL · CHOICE · SCORE", cx, 301, 21, fill=WHITE)
    out.append(t)
    for s in (-1, 1):
        for k in range(3):
            tx = cx + s * 22 + (k - 1) * 6
            out.append(f'<path d="M{tx} 274Q{tx + 2} 284 {tx - 2} 288" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    # head
    head = (f'<path d="{petal_d(cx, 128, 40, 26, -90, roundness=0.4)}" fill="{INK}" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="{cx + 4}" cy="90" r="23" fill="{INK}"/><circle cx="{cx + 4}" cy="90" r="20" fill="{CREAM}"/>'
            f'<path d="{brush((cx - 14, 96), (cx - 6, 104), (cx + 6, 108), (cx + 18, 104), 6)}" fill="#c99a5b"/>'
            f'<path d="M{cx + 18} 80Q{cx + 44} 76 {cx + 47} 98Q{cx + 37} 92 {cx + 22} 97Z" fill="{SAFFRON}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<circle cx="{cx + 11}" cy="84" r="5.5" fill="#ffd400" stroke="{INK}" stroke-width="2"/><circle cx="{cx + 12}" cy="84" r="2.6" fill="{INK}"/>'
            f'<path d="M{cx + 1} 77Q{cx + 12} 71 {cx + 22} 78" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    out.append(f'<g style="transform-origin:{cx}px 110px;animation:tilt 3.6s ease-in-out infinite">{head}</g>')
    return "".join(out)


# ---------------------------------------------------------------- parrot (pushback)
def parrot(doc):
    doc.keyframes("pop", "0%,6%{transform:scale(0)}12%{transform:scale(1.08)}15%,82%{transform:scale(1)}90%,100%{transform:scale(0)}")
    doc.keyframes("chat", "0%,100%{transform:rotate(0)}50%{transform:rotate(16deg)}")
    out = []
    # tail behind the branch
    out.append(f'<path d="{brush((132, 232), (146, 262), (160, 292), (176, 326), 26, peak=0.25, tip1=6)}" fill="{INK}"/>'
               f'<path d="{brush((132, 232), (146, 262), (160, 292), (176, 326), 20, peak=0.25, tip1=4)}" fill="#0e8c86"/>'
               f'<path d="{brush((138, 236), (150, 264), (160, 290), (172, 318), 6)}" fill="#7be0d0"/>')
    # branch with a rose
    out.append(f'<path d="{brush((-10, 270), (60, 256), (150, 262), (240, 246), 18, peak=0.5, tip0=12, tip1=10)}" fill="{INK}"/>'
               f'<path d="{brush((-10, 268), (60, 254), (150, 260), (240, 244), 12, peak=0.5, tip0=8, tip1=7)}" fill="#7a4a24"/>')
    out.append(leaf(34, 262, 40, 13, 130) + leaf(52, 258, 36, 12, 60) + leaf(196, 248, 34, 11, 115))
    out.append(rose(206, 238, 24, "pink", rot0=12, seed=44))
    # body
    out.append('<g transform="rotate(-14 128 196)">'
               f'<ellipse cx="128" cy="196" rx="44" ry="68" fill="{INK}"/><ellipse cx="128" cy="196" rx="40" ry="64" fill="#22a447"/>'
               f'<ellipse cx="114" cy="206" rx="22" ry="46" fill="#8ee05a"/></g>')
    wing = "M142 150C176 160 182 220 160 262C150 272 136 262 134 240C130 210 128 172 142 150Z"
    out.append(f'<path d="{wing}" fill="{INK}" transform="translate(2 2)"/><path d="{wing}" fill="#0f7a3d"/>')
    for k in range(4):
        y0 = 176 + k * 20
        out.append(f'<path d="{brush((144, y0), (160, y0 + 8), (164, y0 + 22), (158, y0 + 36), 9, peak=0.4)}" fill="{["#2fc4b2", "#34d27a"][k % 2]}"/>')
    # feet
    for fx in (114, 138):
        out.append(f'<path d="M{fx} 250L{fx - 6} 262M{fx} 250L{fx + 6} 262" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                   f'<path d="M{fx} 250L{fx - 6} 262M{fx} 250L{fx + 6} 262" stroke="#9aa4ad" stroke-width="3" stroke-linecap="round"/>')
    # head
    out.append(f'<circle cx="134" cy="118" r="34" fill="{INK}"/><circle cx="134" cy="118" r="31" fill="#2bb24c"/>'
               f'<path d="{arc_brush(134, 118, 25, 200, 300, 9)}" fill="#7be08f"/>'
               f'<path d="{arc_brush(134, 120, 29, 30, 150, 7)}" fill="{INK}"/>'
               f'<path d="{arc_brush(134, 121, 33, 40, 140, 5)}" fill="{PINK}"/>')
    out.append(f'<circle cx="122" cy="110" r="9" fill="#ffb37a" stroke="{INK}" stroke-width="2"/><circle cx="121" cy="110" r="4.6" fill="{INK}"/><circle cx="119.5" cy="108.5" r="1.6" fill="#fff"/>')
    lower = f'<path d="M106 126Q98 136 106 142Q114 140 116 130Z" fill="#8f0f1a" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
    out.append(f'<g style="transform-origin:112px 128px;animation:chat .5s ease-in-out infinite">{lower}</g>')
    out.append(f'<path d="M112 104Q84 102 86 132Q90 124 100 126Q104 134 114 130Z" fill="{RED}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
               f'<path d="M104 108Q94 110 92 120" stroke="#ff9aa3" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    # speech bubble
    bub = "M14 18L216 18Q224 18 224 26L224 74Q224 82 216 82L104 82L90 102L88 82L14 82Q6 82 6 74L6 26Q6 18 14 18Z"
    t1, _ = _label(doc, "popb", "you're absolutely", 115, 46, 19, fill=INK)
    t2, _ = _label(doc, "shri", "right!", 115, 72, 24, fill=RED)
    out.append(f'<g style="transform-origin:90px 100px;animation:pop 5s ease-out infinite">'
               f'<path d="{bub}" fill="{INK}" transform="translate(3 4)" opacity=".5"/>'
               f'<path d="{bub}" fill="#fff" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>{t1}{t2}</g>')
    return "".join(out)


# ---------------------------------------------------------------- nazar eye (diff-gate)
def nazar(doc):
    doc.keyframes("look", "0%,30%{transform:translateX(0)}40%,55%{transform:translateX(-17px)}65%,80%{transform:translateX(15px)}90%,100%{transform:translateX(0)}")
    doc.keyframes("lid", "0%,44%,52%,100%{transform:scaleY(0)}48%{transform:scaleY(1)}")
    doc.keyframes("stamp", "0%,55%{transform:scale(2.2);opacity:0}62%{transform:scale(.92);opacity:1}66%,94%{transform:scale(1);opacity:1}100%{opacity:0;transform:scale(1)}")
    out = []
    for i in range(18):
        p1, p2 = polar(115, 140, 240, i * 20), polar(115, 140, 240, i * 20 + 10)
        out.append(f'<path d="M115 140L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}Z" fill="#2a2470" opacity=".7"/>')
    # brow
    out.append(f'<path d="{brush((14, 74), (70, 22), (160, 22), (220, 70), 22, peak=0.45)}" fill="{INK}"/>'
               f'<path d="{brush((40, 54), (90, 30), (140, 30), (190, 50), 5, peak=0.5)}" fill="{GOLD}" opacity=".9"/>')
    eye = "M8 142Q115 52 222 142Q115 230 8 142Z"
    doc.define(f'<clipPath id="eyeclip"><path d="{eye}"/></clipPath>')
    # lashes along the upper lid
    for k in range(9):
        t = 0.1 + k * 0.1
        bx = (1 - t) ** 2 * 8 + 2 * (1 - t) * t * 115 + t * t * 222
        by = (1 - t) ** 2 * 142 + 2 * (1 - t) * t * 52 + t * t * 142
        ang = -90 + (t - 0.5) * 110
        tip = polar(bx, by, 26, ang)
        c = polar(bx, by, 14, ang - 14)
        out.append(f'<path d="{brush((bx, by + 4), c, c, tip, 9, peak=0.3)}" fill="{INK}"/>')
    out.append(f'<path d="{eye}" fill="#fff" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
    iris = (f'<circle cx="115" cy="142" r="50" fill="{DBLUE}"/><circle cx="115" cy="142" r="43" fill="#2f7bff"/>'
            f'<circle cx="115" cy="142" r="31" fill="#fff"/><circle cx="115" cy="142" r="24" fill="#4fc3ff"/>'
            f'<circle cx="115" cy="142" r="14" fill="{INK}"/><circle cx="103" cy="128" r="7" fill="#fff"/><circle cx="125" cy="152" r="3" fill="#fff"/>')
    out.append(f'<g clip-path="url(#eyeclip)"><g style="animation:look 6s ease-in-out infinite">{iris}</g>'
               f'<rect x="0" y="50" width="230" height="96" fill="{MAGENTA}" style="transform-origin:115px 52px;animation:lid 6s ease-in-out infinite"/></g>')
    out.append(f'<path d="{eye}" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
    out.append(f'<path d="M30 154Q115 214 200 154" fill="none" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"/>')
    # code plate + stamp
    out.append(f'<rect x="10" y="244" width="210" height="62" rx="10" fill="#121222" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="10" y="244" width="210" height="16" rx="8" fill="#2b2b44"/>'
               f'<circle cx="22" cy="252" r="3.4" fill="{RED}"/><circle cx="33" cy="252" r="3.4" fill="{SAFFRON}"/><circle cx="44" cy="252" r="3.4" fill="{GREEN}"/>')
    t, _ = _label(doc, "mono", "+ import ghost_pkg", 22, 288, 17, fill="#9ef2b0", anchor="start")
    out.append(t)
    st, sb = _label(doc, "tekob", "BLOCK", 168, 292, 34, fill=RED)
    out.append(f'<g style="transform-origin:168px 282px;animation:stamp 6s ease-out infinite">'
               f'<g transform="rotate(-12 168 282)"><rect x="124" y="262" width="88" height="38" rx="5" fill="none" stroke="{RED}" stroke-width="4"/>{st}</g></g>')
    return "".join(out)


# ---------------------------------------------------------------- kite (rag-cost-curve)
def kite(doc):
    """The string IS the measured curve: x = $ per correct answer, y = exact match (200 MuSiQue queries)."""
    doc.keyframes("kfly", "0%,100%{transform:rotate(-5deg)}50%{transform:rotate(6deg)}")
    doc.keyframes("tailwave", "0%,100%{transform:rotate(-12deg)}50%{transform:rotate(14deg)}")
    data = [("naive", 0.0155, 0.275), ("reranked", 0.0156, 0.290), ("iterative", 0.0273, 0.505), ("agentic", 0.0389, 0.600)]

    def X(c):
        return 40 + (c - 0.015) / 0.025 * 156

    def Y(e):
        return 252 - (e - 0.25) / 0.4 * 168
    pts = [(X(c), Y(e)) for _, c, e in data]
    out = [cloud(16, 70, 0.75), cloud(120, 196, 0.6, "#eaf6ff")]
    # axes, painted
    out.append(f'<path d="M22 264L222 264" stroke="#ffffff" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" opacity=".85"/>'
               f'<path d="M22 264L22 70" stroke="#ffffff" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" opacity=".85"/>')
    t, _ = _label(doc, "tekob", "COST PER CORRECT ANSWER", 222, 286, 17, fill=WHITE, anchor="end", outline=DBLUE, ow=4)
    out.append(t)
    t, _ = _label(doc, "tekob", "ACCURACY", 0, 0, 17, fill=WHITE, anchor="start", outline=DBLUE, ow=4)
    out.append(f'<g transform="translate(16 200) rotate(-90)">{t}</g>')
    # string through the data (Catmull-Rom)
    chain_pts = [(30, 300)] + pts
    d = f"M{n(chain_pts[0][0])} {n(chain_pts[0][1])}"
    for i in range(len(chain_pts) - 1):
        p0 = chain_pts[i - 1] if i > 0 else chain_pts[i]
        p1, p2 = chain_pts[i], chain_pts[i + 1]
        p3 = chain_pts[i + 2] if i + 2 < len(chain_pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{n(c1[0])} {n(c1[1])} {n(c2[0])} {n(c2[1])} {n(p2[0])} {n(p2[1])}"
    out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="#fff3c4" stroke-width="2.4" stroke-linecap="round"/>')
    # spool
    out.append(f'<g transform="rotate(-20 26 306) translate(0 -6)"><rect x="6" y="296" width="40" height="22" rx="4" fill="#a8641e" stroke="{INK}" stroke-width="3"/>'
               f'<rect x="12" y="298" width="28" height="18" fill="#fff3c4"/><path d="M12 302H40M12 306H40M12 310H40" stroke="#d9a066" stroke-width="1.5"/>'
               f'<rect x="-6" y="303" width="14" height="8" rx="3" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
               f'<rect x="44" y="303" width="14" height="8" rx="3" fill="{RED}" stroke="{INK}" stroke-width="2"/></g>')
    # beads + labels
    cols = [SAFFRON, ORANGE, PINK, RED]
    for (lab, c, e), (px, py), col in zip(data, pts, cols):
        out.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="7.5" fill="{col}" stroke="{INK}" stroke-width="3"/>')
    lab_pos = [("naive ≈ reranked", pts[0][0] + 13, pts[0][1] - 4, "start"),
               ("iterative", pts[2][0] + 13, pts[2][1] + 14, "start"),
               ("agentic", pts[3][0] - 13, pts[3][1] + 8, "end")]
    for text, lx, ly, anc in lab_pos:
        t, _ = _label(doc, "tekob", text, lx, ly, 19, fill=WHITE, anchor=anc, outline=INK, ow=4)
        out.append(t)
    # kite at the agentic bead
    ax, ay = pts[3]
    kx, ky = ax - 4, ay - 46
    kw, kt, kb = 28, 34, 38
    k = (f"M{n(kx)} {n(ky - kt)}L{n(kx + kw)} {n(ky)}L{n(kx)} {n(ky + kb)}L{n(kx - kw)} {n(ky)}Z")
    tri = [(f"M{n(kx)} {n(ky - kt)}L{n(kx + kw)} {n(ky)}L{n(kx)} {n(ky)}Z", RED),
           (f"M{n(kx)} {n(ky - kt)}L{n(kx - kw)} {n(ky)}L{n(kx)} {n(ky)}Z", SAFFRON),
           (f"M{n(kx)} {n(ky + kb)}L{n(kx + kw)} {n(ky)}L{n(kx)} {n(ky)}Z", GREEN),
           (f"M{n(kx)} {n(ky + kb)}L{n(kx - kw)} {n(ky)}L{n(kx)} {n(ky)}Z", BLUE)]
    kite_g = [f'<path d="{k}" fill="{INK}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>']
    kite_g += [f'<path d="{dd}" fill="{c}"/>' for dd, c in tri]
    kite_g.append(f'<circle cx="{n(kx)}" cy="{n(ky)}" r="8" fill="#fff" stroke="{INK}" stroke-width="3"/><circle cx="{n(kx)}" cy="{n(ky)}" r="3.4" fill="{PINK}"/>')
    kite_g.append(f'<path d="M{n(kx)} {n(ky - kt)}L{n(kx)} {n(ky + kb)}M{n(kx - kw)} {n(ky)}Q{n(kx)} {n(ky - 12)} {n(kx + kw)} {n(ky)}" stroke="{INK}" stroke-width="2.5" fill="none"/>')
    tail = []
    for i in range(3):
        bx, by = kx + 8 + i * 6, ky + kb + 12 + i * 13
        tail.append(f'<path d="M{n(bx - 8)} {n(by - 5)}L{n(bx + 8)} {n(by + 5)}L{n(bx + 8)} {n(by - 5)}L{n(bx - 8)} {n(by + 5)}Z" fill="{[PINK, SAFFRON, TEAL, RED][i]}" stroke="{INK}" stroke-width="2"/>')
    tail_line = f'<path d="M{n(kx)} {n(ky + kb)}Q{n(kx + 10)} {n(ky + kb + 24)} {n(kx + 22)} {n(ky + kb + 44)}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
    kite_g.append(f'<g style="transform-origin:{n(kx)}px {n(ky + kb)}px;animation:tailwave 2.2s ease-in-out infinite">{tail_line}{"".join(tail)}</g>')
    bridle = f'<path d="M{n(ax)} {n(ay)}L{n(kx)} {n(ky + 6)}" stroke="{INK}" stroke-width="2"/>'
    out.append(f'<g style="transform-origin:{n(ax)}px {n(ay)}px;animation:kfly 3.4s ease-in-out infinite">{bridle}{"".join(kite_g)}</g>')
    return "".join(out)


# ---------------------------------------------------------------- camel (minio-from-source)
def camel(doc):
    doc.keyframes("legA", "0%,100%{transform:rotate(14deg)}50%{transform:rotate(-14deg)}")
    doc.keyframes("legB", "0%,100%{transform:rotate(-14deg)}50%{transform:rotate(14deg)}")
    doc.keyframes("walk", "0%,50%,100%{transform:translateY(0)}25%,75%{transform:translateY(-3px)}")
    doc.keyframes("tass", "0%,100%{transform:rotate(-12deg)}50%{transform:rotate(12deg)}")
    out = []
    # dunes + sun
    out.append(f'<circle cx="176" cy="74" r="34" fill="#ffe08a"/>'
               f'<path d="M-10 268C40 244 90 244 140 262C180 276 210 262 240 252L240 330L-10 330Z" fill="#e08a2e"/>'
               f'<path d="M-10 290C50 274 110 280 170 292C200 298 220 294 240 290L240 330L-10 330Z" fill="#c76a1c"/>')
    tan, shade = "#e2a866", "#b9783c"

    def leg(x, y, anim, dx=0):
        g = (f'<path d="{brush((x, y), (x + 4 + dx, y + 30), (x + dx, y + 48), (x + dx, y + 80), 22, peak=0.15, tip1=9)}" fill="{INK}"/>'
             f'<path d="{brush((x, y), (x + 4 + dx, y + 30), (x + dx, y + 48), (x + dx, y + 80), 16, peak=0.15, tip1=6)}" fill="{shade}"/>'
             f'<ellipse cx="{n(x + dx)}" cy="{n(y + 80)}" rx="10" ry="5" fill="{INK}"/>'
             f'<circle cx="{n(x + 2 + dx)}" cy="{n(y + 42)}" r="5" fill="{shade}" stroke="{INK}" stroke-width="2"/>')
        return f'<g style="transform-origin:{n(x)}px {n(y)}px;animation:{anim} 1.2s ease-in-out infinite">{g}</g>'
    body_g = []
    body_g.append(leg(66, 214, "legB") + leg(158, 214, "legA"))
    body = ("M36 204C30 172 54 154 70 146C82 116 116 108 132 134C146 150 168 158 180 176C190 194 184 222 162 230"
            "L72 234C52 234 40 224 36 204Z")
    body_g.append(f'<path d="{body}" fill="{INK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/><path d="{body}" fill="{tan}"/>')
    body_g.append(f'<path d="{brush((60, 222), (100, 232), (140, 232), (170, 222), 12)}" fill="{shade}"/>')
    # neck + head
    body_g.append(f'<path d="{brush((164, 184), (196, 176), (198, 140), (206, 104), 44, peak=0.1, tip1=20)}" fill="{INK}"/>'
                  f'<path d="{brush((164, 184), (196, 176), (198, 140), (206, 104), 36, peak=0.1, tip1=15)}" fill="{tan}"/>')
    body_g.append(f'<g transform="rotate(24 214 102)"><ellipse cx="216" cy="100" rx="26" ry="14" fill="{INK}"/><ellipse cx="216" cy="100" rx="23" ry="11.5" fill="{tan}"/></g>'
                  f'<circle cx="208" cy="94" r="3.2" fill="{INK}"/><path d="M203 90Q208 86 214 89" stroke="{INK}" stroke-width="2" fill="none"/>'
                  f'<path d="M196 86L192 76L201 83Z" fill="{shade}" stroke="{INK}" stroke-width="2"/>'
                  f'<path d="M228 114Q234 116 236 111" stroke="{INK}" stroke-width="2.2" fill="none"/>')
    # decorated harness
    body_g.append(f'<path d="M188 140Q200 150 210 138" stroke="{RED}" stroke-width="7" fill="none"/>'
                  + "".join(f'<circle cx="{190 + i * 5}" cy="{145 + (i % 2) * 2}" r="2" fill="{GOLD}"/>' for i in range(4))
                  + f'<circle cx="200" cy="80" r="6" fill="{PINK}" stroke="{INK}" stroke-width="2"/><circle cx="212" cy="80" r="5" fill="{SAFFRON}" stroke="{INK}" stroke-width="2"/>')
    # saddle cloth with tassels
    cloth = "M70 148C86 124 120 120 136 142L144 196L64 196Z"
    body_g.append(f'<path d="{cloth}" fill="{RED}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    body_g.append(dots(74, 188, 140, 188, 9, 2.6, GOLD, WHITE))
    for i in range(7):
        tx = 68 + i * 12
        body_g.append(f'<g style="transform-origin:{tx}px 196px;animation:tass 1.2s ease-in-out {-i * 0.1}s infinite">'
                      f'<path d="M{tx} 196L{tx} 206" stroke="{INK}" stroke-width="2"/><path d="{petal_d(tx, 204, 12, 4.5, 90)}" fill="{[PINK, SAFFRON, TEAL, GREEN][i % 4]}" stroke="{INK}" stroke-width="1.8"/></g>')
    # crates
    for (x0, y0, label, rot, col) in ((66, 100, "AMD64", -3, BLUE), (72, 52, "ARM64", 4, GREEN)):
        crate = []
        crate.append(f'<rect x="{x0}" y="{y0}" width="72" height="48" rx="4" fill="#c8913a" stroke="{INK}" stroke-width="4"/>')
        crate.append(f'<path d="M{x0 + 4} {y0 + 4}L{x0 + 68} {y0 + 44}M{x0 + 68} {y0 + 4}L{x0 + 4} {y0 + 44}" stroke="#8a5a22" stroke-width="3"/>')
        crate.append(f'<rect x="{x0 + 8}" y="{y0 + 11}" width="56" height="26" rx="4" fill="{col}" stroke="{INK}" stroke-width="2.5"/>')
        t, _ = _label(doc, "tekob", label, x0 + 36, y0 + 33, 24, fill=WHITE)
        crate.append(t)
        body_g.append(f'<g transform="rotate({rot} {x0 + 36} {y0 + 24})">{"".join(crate)}</g>')
    body_g.append(f'<path d="M80 104L94 150M128 104L118 150" stroke="#5a3412" stroke-width="4"/>')
    # tail
    body_g.append(f'<path d="M38 194Q24 210 28 232" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                  f'<path d="{petal_d(28, 228, 16, 6, 100)}" fill="{PINK}" stroke="{INK}" stroke-width="2"/>')
    allg = leg(80, 214, "legA", -2) + leg(170, 214, "legB", -2) + f'<g style="animation:walk 1.2s ease-in-out infinite">{"".join(body_g)}</g>'
    out.append(f'<g transform="translate(-10 10) scale(.94)">{allg}</g>')
    return "".join(out)


# ---------------------------------------------------------------- bulbul on a rose (voice agents)
def bulbul(doc):
    doc.keyframes("wave", "0%{transform:scale(.4);opacity:0}20%{opacity:1}100%{transform:scale(1.25);opacity:0}")
    doc.keyframes("sing", "0%,100%{transform:rotate(0)}50%{transform:rotate(14deg)}")
    doc.keyframes("note", "0%{transform:translate(0,0);opacity:0}15%{opacity:1}100%{transform:translate(18px,-60px);opacity:0}")
    out = []
    # rose bush
    out.append(f'<path d="{brush((150, 330), (150, 280), (110, 240), (60, 214), 12, peak=0.5, tip0=8, tip1=6)}" fill="{INK}"/>'
               f'<path d="{brush((150, 330), (150, 280), (110, 240), (60, 214), 7, peak=0.5, tip0=5, tip1=4)}" fill="#3f8a3a"/>')
    out.append(leaf(150, 286, 44, 14, 200) + leaf(140, 262, 40, 13, -40) + leaf(96, 236, 34, 11, 230) + leaf(188, 300, 36, 12, -20))
    out.append(rose(170, 262, 38, "red", rot0=8, seed=71))
    out.append(bud(64, 214, 26, 200, color=PINK, light="#ffb3d1"))
    out.append(rose(40, 300, 22, "yellow", rot0=0, seed=72))
    # sound waves out of the beak
    for i in range(3):
        out.append(f'<path d="M168 150A52 52 0 0 1 168 206" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" '
                   f'style="transform-origin:148px 178px;animation:wave 2.1s ease-out {i * 0.7}s infinite"/>')
    notes = []
    for i, (nx, ny, c) in enumerate(((176, 150, SAFFRON), (196, 176, WHITE), (186, 122, PINK))):
        notes.append(f'<g style="animation:note 3s ease-out {i}s infinite"><ellipse cx="{nx}" cy="{ny}" rx="7" ry="5.5" transform="rotate(-20 {nx} {ny})" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                     f'<path d="M{nx + 6} {ny - 2}L{nx + 6} {ny - 26}L{nx + 16} {ny - 20}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></g>')
    out.append("".join(notes))
    bird = []
    # tail
    bird.append(f'<path d="{brush((84, 186), (66, 214), (54, 236), (44, 262), 30, peak=0.3, tip1=10)}" fill="{INK}"/>'
               f'<path d="{brush((84, 186), (66, 214), (54, 236), (44, 262), 23, peak=0.3, tip1=7)}" fill="#6b5446"/>'
               f'<path d="{petal_d(80, 198, 22, 9, 120)}" fill="{RED}" stroke="{INK}" stroke-width="2"/>')
    # body
    bird.append('<g transform="rotate(-28 108 170)">'
               f'<ellipse cx="108" cy="170" rx="46" ry="32" fill="{INK}"/><ellipse cx="108" cy="170" rx="42" ry="28" fill="#7a6252"/>'
               f'<ellipse cx="118" cy="184" rx="28" ry="15" fill="#f4ead8"/></g>')
    for k in range(4):
        bird.append(f'<path d="{brush((74 + k * 9, 158 - k * 6), (88 + k * 9, 170 - k * 6), (100 + k * 9, 174 - k * 6), (112 + k * 9, 170 - k * 6), 7)}" fill="#a28470"/>')
    # feet on the branch
    bird.append(f'<path d="M104 196L98 214M116 194L114 212" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    # head with crest, singing
    head = (f'<circle cx="140" cy="128" r="24" fill="{INK}"/><circle cx="140" cy="128" r="21" fill="#1c1716"/>'
            f'<path d="M128 108L114 70L144 104Z" fill="#1c1716" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<circle cx="138" cy="136" r="9" fill="#fff"/><path d="M128 124Q132 118 138 122" stroke="{RED}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<circle cx="146" cy="122" r="4" fill="#fff"/><circle cx="147" cy="122" r="2.2" fill="{INK}"/>'
            f'<path d="M158 120L176 124L158 130Z" fill="#2a2a2a" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    lower = f'<path d="M158 132L174 140L157 138Z" fill="#2a2a2a" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    bird.append(head + f'<g style="transform-origin:158px 132px;animation:sing .7s ease-in-out infinite">{lower}</g>')
    out.append(f'<g transform="translate(-6 46)">{"".join(bird)}</g>')
    for fx, fy, c in ((28, 40, SAFFRON), (64, 20, PINK), (206, 214, TEAL)):
        out.append(blossom(fx, fy, 11, color=c, center=RED if c != PINK else SAFFRON))
    out.append(leaf(6, 74, 34, 11, -20) + leaf(36, 66, 30, 10, -60))
    return "".join(out)


# ---------------------------------------------------------------- balance scale (edgeproof)
def scales(doc):
    doc.keyframes("beam", "0%,100%{transform:rotate(9deg)}50%{transform:rotate(15deg)}")
    doc.keyframes("pan", "0%,100%{transform:rotate(-9deg)}50%{transform:rotate(-15deg)}")
    out = []
    for i in range(12):
        p1, p2 = polar(115, 150, 260, i * 30), polar(115, 150, 260, i * 30 + 15)
        out.append(f'<path d="M115 150L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}Z" fill="#7d3fd0" opacity=".45"/>')
    # pillar + base
    out.append(f'<path d="M106 92L124 92L128 270L102 270Z" fill="url(#brassv)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M64 300L166 300L150 270L80 270Z" fill="url(#brassv)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               f'<rect x="56" y="298" width="118" height="14" rx="5" fill="#8a5a12" stroke="{INK}" stroke-width="4"/>'
               f'<circle cx="115" cy="62" r="12" fill="url(#brassv)" stroke="{INK}" stroke-width="4"/>'
               f'<path d="M115 50L115 36" stroke="{INK}" stroke-width="4"/><circle cx="115" cy="34" r="5" fill="{RED}" stroke="{INK}" stroke-width="2"/>')
    piv = (115, 92)

    def pan(x, label, coins, col):
        g = [f'<path d="M{x} 0L{x - 30} 92M{x} 0L{x + 30} 92M{x} 0L{x} 92" stroke="{INK}" stroke-width="2.4"/>']
        for k in range(coins):
            cy = 88 - k * 7
            g.append(f'<ellipse cx="{x + (k % 2) * 4 - 2}" cy="{cy}" rx="15" ry="5" fill="{GOLD}" stroke="{INK}" stroke-width="2.2"/>')
        g.append(f'<path d="M{x - 40} 92Q{x} 124 {x + 40} 92Z" fill="url(#brassv)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
        t, _ = _label(doc, "tekob", label, x, 152, 26, fill=WHITE, outline=INK, ow=5)
        g.append(f'<rect x="{x - 36}" y="128" width="72" height="30" rx="6" fill="{col}" stroke="{INK}" stroke-width="3"/>{t}')
        return (f'<g transform="translate(0 {piv[1]})"><g style="transform-origin:{x}px 0px;animation:pan 3s ease-in-out infinite">'
                f'{"".join(g)}</g></g>')
    beam = (f'<rect x="38" y="{piv[1] - 6}" width="154" height="12" rx="6" fill="url(#brassv)" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{piv[0]}" cy="{piv[1]}" r="9" fill="{RED}" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<g style="transform-origin:{piv[0]}px {piv[1]}px;animation:beam 3s ease-in-out infinite">{beam}'
               f'{pan(50, "EDGE", 2, GREEN)}{pan(180, "FEES", 6, RED)}</g>')
    doc.define('<linearGradient id="brassv" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a12"/>'
               '<stop offset=".4" stop-color="#ffd76a"/><stop offset=".65" stop-color="#d79a1e"/><stop offset="1" stop-color="#7a4a0a"/></linearGradient>')
    return "".join(out)


# ---------------------------------------------------------------- fish in a grid net (lead finder)
def fishnet(doc):
    doc.keyframes("swim", "0%,100%{transform:translateX(-8px)}50%{transform:translateX(8px)}")
    doc.keyframes("fin", "0%,100%{transform:rotate(-14deg)}50%{transform:rotate(14deg)}")
    doc.keyframes("rise", "0%{transform:translateY(0);opacity:0}20%{opacity:.9}100%{transform:translateY(-120px);opacity:0}")
    doc.keyframes("bob2", "0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}")
    out = []
    for i in range(5):
        out.append(f'<path d="M{20 + i * 50} 0L{60 + i * 50} 0L{20 + i * 40} 330L{0 + i * 40} 330Z" fill="#fff" opacity=".05"/>')
    # net mesh (the grid search)
    mesh = []
    for i in range(-8, 14):
        mesh.append(f'<path d="M{i * 30} 70L{i * 30 + 260} 330" stroke="#f6e7c1" stroke-width="2.2" opacity=".55"/>')
        mesh.append(f'<path d="M{i * 30} 70L{i * 30 - 260} 330" stroke="#f6e7c1" stroke-width="2.2" opacity=".55"/>')
    out.append(f'<g clip-path="url(#netclip)">{"".join(mesh)}</g>')
    doc.define('<clipPath id="netclip"><path d="M0 70Q115 110 230 70L230 330L0 330Z"/></clipPath>')
    out.append(f'<path d="M0 70Q115 110 230 70" fill="none" stroke="#c8913a" stroke-width="7"/>'
               f'<path d="M0 70Q115 110 230 70" fill="none" stroke="#f2c14e" stroke-width="3" stroke-dasharray="6 8"/>')
    # map-pin floats on the rope: the leads
    for i, x in enumerate((40, 115, 190)):
        y = 70 + (1 - ((x - 115) / 115) ** 2) * 20 - 4
        out.append(f'<g style="animation:bob2 2s ease-in-out {-i * 0.6}s infinite">'
                   f'<path d="M{x} {n(y)}C{x - 14} {n(y - 16)} {x - 16} {n(y - 38)} {x} {n(y - 40)}C{x + 16} {n(y - 38)} {x + 14} {n(y - 16)} {x} {n(y)}Z" '
                   f'fill="{[RED, SAFFRON, PINK][i]}" stroke="{INK}" stroke-width="3"/><circle cx="{x}" cy="{n(y - 26)}" r="6" fill="#fff" stroke="{INK}" stroke-width="2"/></g>')

    def fish(x, y, s, body, fin, flip=1, delay=0):
        g = []
        tail = f'<path d="M{-46} 0L{-74} -22Q{-64} 0 {-74} 22Z" fill="{fin}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        g.append(f'<g style="transform-origin:-44px 0px;animation:fin .8s ease-in-out {delay}s infinite">{tail}</g>')
        g.append(f'<path d="M-50 0C-30 -30 30 -34 56 -4C60 0 60 4 56 6C30 34 -30 30 -50 0Z" fill="{body}" stroke="{INK}" stroke-width="4"/>')
        for r_ in range(2):
            for c_ in range(4):
                sx, sy = -26 + c_ * 14, -10 + r_ * 16
                g.append(f'<path d="M{sx} {sy - 6}Q{sx + 9} {sy} {sx} {sy + 6}" fill="none" stroke="#fff" stroke-width="2.4" opacity=".8"/>')
        g.append(f'<path d="M-4 -24Q8 -44 22 -24Z" fill="{fin}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M30 -12Q34 4 30 16" fill="none" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="40" cy="-6" r="7" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="41" cy="-6" r="3.4" fill="{INK}"/>')
        return (f'<g style="animation:swim 3.4s ease-in-out {delay}s infinite"><g transform="translate({x} {y}) scale({s * flip} {s})">'
                f'{"".join(g)}</g></g>')
    out.append(fish(118, 170, 1.0, ORANGE, BLUE, 1, 0))
    out.append(fish(104, 252, 0.85, TEAL, PINK, -1, -1.2))
    out.append(fish(170, 300, 0.55, SAFFRON, RED, 1, -0.6))
    for i, (bx, by) in enumerate(((180, 200), (196, 240), (60, 220), (40, 290))):
        out.append(f'<circle cx="{bx}" cy="{by}" r="{4 + i % 2 * 2}" fill="none" stroke="#e8fbff" stroke-width="2" style="animation:rise 3s ease-in {-i * 0.8}s infinite"/>')
    return "".join(out)
