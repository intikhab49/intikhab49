"""Road strip: a decorated truck on the Karakoram Highway; scenery scrolls past in parallax."""
from ta_core import (BLUE, CREAM, DBLUE, DGREEN, DRED, GOLD, GREEN, INK, ORANGE, PINK, PURPLE, RED, RNG, SAFFRON,
                     TEAL, WHITE, Doc, arc_brush, brush, n, polar)
from ta_fonts import F
from ta_motifs import blossom, chain, dots, leaf, rose, tape_defs

W, H = 1280, 300
GROUND = 262


def wheel(doc, cx, cy, r, dur=0.6):
    doc.keyframes("roll", "to{transform:rotate(360deg)}")
    spokes = []
    cols = [RED, SAFFRON, GREEN, BLUE, PINK, TEAL]
    for i in range(6):
        a = i * 60
        p1, p2 = polar(cx, cy, r * 0.56, a - 18), polar(cx, cy, r * 0.56, a + 18)
        spokes.append(f'<path d="M{n(cx)} {n(cy)}L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}Z" fill="{cols[i]}"/>')
    return (f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="#151515" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 0.86)}" fill="none" stroke="#2c2c2c" stroke-width="{n(r * 0.1)}" stroke-dasharray="4 5"/>'
            f'<g style="transform-origin:{n(cx)}px {n(cy)}px;animation:roll {dur}s linear infinite">'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 0.62)}" fill="#e9eef3" stroke="{INK}" stroke-width="2.5"/>{"".join(spokes)}'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 0.2)}" fill="{GOLD}" stroke="{INK}" stroke-width="2"/></g>')


def truck(doc, ox, oy, s=1.0, side_text=("AI", "ML", "RAG")):
    """Side view of a decorated Bedford, facing right. (ox, oy) = rear wheel-ground point; local ground y=0."""
    tape = tape_defs(doc, 14)
    out = []

    def P(x, y):
        return f"{n(x)} {n(y)}"
    # crown (taj) over the cab
    crown = f"M{P(330, -206)}C{P(400, -214)} {P(460, -238)} {P(512, -262)}C{P(532, -250)} {P(530, -214)} {P(514, -186)}L{P(470, -176)}L{P(330, -180)}Z"
    out.append(f'<path d="{crown}" fill="{INK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    out.append(f'<path d="{crown}" fill="url(#{tape})"/>')
    inner = f"M{P(342, -196)}C{P(404, -204)} {P(458, -224)} {P(504, -246)}C{P(514, -236)} {P(514, -212)} {P(504, -194)}L{P(466, -186)}L{P(342, -188)}Z"
    out.append(f'<path d="{inner}" fill="{RED}"/>')
    for i, x in enumerate((370, 440, 500)):
        out.append(blossom(x, -196 - (x - 342) * 0.22 + 4, 6.5, color=[SAFFRON, WHITE, TEAL, PINK, SAFFRON][i], center=RED))
    for ex in (405, 472):
        ey = -192 - (ex - 342) * 0.22
        out.append(f'<ellipse cx="{ex}" cy="{n(ey)}" rx="13" ry="8" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
                   f'<circle cx="{ex + 2}" cy="{n(ey)}" r="5" fill="{BLUE}"/><circle cx="{ex + 2}" cy="{n(ey)}" r="2.2" fill="{INK}"/>')
    # cargo body
    out.append(f'<rect x="0" y="-214" width="344" height="176" rx="6" fill="{INK}"/>')
    out.append(f'<rect x="5" y="-209" width="334" height="18" fill="url(#{tape})"/>')
    out.append(f'<rect x="5" y="-189" width="334" height="104" fill="{CREAM}"/>')
    out.append(f'<rect x="5" y="-85" width="334" height="24" fill="{GREEN}"/>')
    out.append(dots(14, -73, 332, -73, 12, 2.6, SAFFRON, WHITE))
    out.append(f'<rect x="5" y="-61" width="334" height="20" fill="{DRED}"/>')
    for i in range(14):
        out.append(f'<path d="M{n(8 + i * 24)} -41Q{n(20 + i * 24)} -28 {n(32 + i * 24)} -41Z" fill="{SAFFRON}" stroke="{INK}" stroke-width="2"/>')
    # painted panels: three arched windows on the cargo side
    pals = [(BLUE, "#7aa2ff"), (DGREEN, "#5bd38a"), (PURPLE, "#b48cff")]
    for i in range(3):
        x0 = 16 + i * 108
        arch = f"M{P(x0, -92)}L{P(x0, -158)}Q{P(x0, -182)} {P(x0 + 50, -184)}Q{P(x0 + 100, -182)} {P(x0 + 100, -158)}L{P(x0 + 100, -92)}Z"
        out.append(f'<path d="{arch}" fill="{pals[i][0]}" stroke="{INK}" stroke-width="4"/>')
        out.append(f'<path d="{arch}" fill="none" stroke="{GOLD}" stroke-width="2" transform="translate({n((x0 + 50) * 0.08)} {n(-138 * 0.08)}) scale(.92)"/>')
        out.append(rose(x0 + 50, -150, 17, ["red", "yellow", "pink"][i], rot0=i * 20, seed=30 + i))
        out.append(leaf(x0 + 50, -134, 22, 8, 120))
        out.append(leaf(x0 + 50, -134, 22, 8, 60))
        doc_font = F("tekob")
        rid, box, adv = doc.text_def(doc_font, side_text[i], x0 + 50, -100, 26, anchor="middle")
        out.append(f'<use href="#{rid}" fill="{INK}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><use href="#{rid}" fill="{WHITE}"/>')
    for x in (0, 112, 220, 330):
        out.append(f'<rect x="{x + 5}" y="-189" width="6" height="104" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/>')
    # cab
    cab = f"M{P(346, -40)}L{P(346, -176)}L{P(458, -176)}C{P(476, -176)} {P(482, -170)} {P(490, -150)}L{P(512, -104)}C{P(518, -92)} {P(520, -80)} {P(520, -66)}L{P(520, -40)}Z"
    out.append(f'<path d="{cab}" fill="{INK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    out.append(f'<path d="{cab}" fill="#f2b705"/>')
    out.append(f'<path d="M{P(350, -100)}L{P(516, -100)}L{P(520, -84)}L{P(350, -84)}Z" fill="{RED}"/>')
    out.append(dots(356, -92, 512, -92, 11, 2.2, WHITE))
    win = f"M{P(372, -166)}L{P(452, -166)}C{P(466, -166)} {P(472, -160)} {P(478, -148)}L{P(494, -116)}L{P(372, -116)}Z"
    out.append(f'<path d="{win}" fill="#9fd8ff" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<path d="{brush((392, -160), (402, -148), (412, -134), (420, -122), 9)}" fill="#fff" opacity=".8"/>')
    out.append(f'<path d="M{P(420, -166)}L{P(420, -116)}" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<rect x="360" y="-76" width="96" height="30" rx="5" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>')
    out.append(blossom(384, -61, 9, color=PINK, center=SAFFRON) + blossom(408, -61, 9, color=SAFFRON, center=RED)
               + blossom(432, -61, 9, color=WHITE, center=RED))
    out.append(f'<circle cx="514" cy="-72" r="11" fill="#fff6c0" stroke="{INK}" stroke-width="3"/>'
               f'<circle cx="514" cy="-72" r="5" fill="#ffd400"/>')
    # headlight beam
    out.append(f'<path d="M{P(522, -78)}L{P(640, -100)}L{P(640, -36)}L{P(522, -66)}Z" fill="url(#beam)"/>')
    out.append(f'<rect x="506" y="-46" width="26" height="14" rx="4" fill="url(#chromev)" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<rect x="-8" y="-44" width="22" height="12" rx="3" fill="url(#chromev)" stroke="{INK}" stroke-width="3"/>')
    # chassis + mudflap
    out.append(f'<rect x="10" y="-40" width="500" height="12" fill="#2a2a2a" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<path d="M{P(14, -40)}L{P(42, -40)}L{P(44, -2)}L{P(12, -2)}Z" fill="{INK}"/>')
    out.append(f'<circle cx="28" cy="-22" r="8" fill="#fff"/><circle cx="29" cy="-22" r="4" fill="{BLUE}"/><circle cx="29" cy="-22" r="1.8" fill="{INK}"/>')
    # wheels
    out.append(wheel(doc, 86, -26, 26))
    out.append(wheel(doc, 150, -26, 26))
    out.append(wheel(doc, 446, -26, 26))
    g = f'<g transform="translate({n(ox)} {n(oy)}) scale({s})">{"".join(out)}</g>'
    # chains between the wheels (outside the scaled group so they swing in page space)
    ch = []
    r = RNG(9)
    for i, x in enumerate((196, 222, 248, 274, 300, 326, 360, 386)):
        ch.append(chain(doc, ox + x * s, oy - 30 * s, links=3 + i % 2, link=7 * s, pendant=["leaf", "bell", "bead"][i % 3],
                        swing=r.uniform(10, 16), dur=r.uniform(0.9, 1.3), delay=-r.uniform(0, 1)))
    for i, x in enumerate((508, 522)):
        ch.append(chain(doc, ox + x * s, oy - 34 * s, links=2, link=6 * s, pendant="bell" if i else "leaf",
                        swing=14, dur=1.0 + i * 0.2, delay=-i * 0.3))
    return g + "".join(ch)


def build():
    d = Doc(W, H, "A decorated Pakistani truck driving the Karakoram Highway",
            "Animated: mountains, poplars and kilometre stones scroll past a hand-painted truck. "
            "The stones name the work: voice AI agents, RAG, LLM evals, machine learning, multi-tenant SaaS and open source.")
    d.keyframes("scroll", "to{transform:translateX(var(--p))}")
    d.keyframes("bounce", "0%,100%{transform:translateY(0)}50%{transform:translateY(-2.5px)}")
    d.keyframes("puff", "0%{transform:translate(0,0) scale(.3);opacity:.7}100%{transform:translate(-90px,-26px) scale(1.6);opacity:0}")
    d.keyframes("flap", "0%,100%{transform:scaleY(1)}50%{transform:scaleY(-.6)}")
    d.keyframes("fly", "0%{transform:translateX(0)}100%{transform:translateX(-1500px)}")
    d.define('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1f6b"/>'
             '<stop offset=".45" stop-color="#b8327a"/><stop offset=".8" stop-color="#ff7a3c"/><stop offset="1" stop-color="#ffc35a"/></linearGradient>',
             '<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff3a8" stop-opacity=".75"/><stop offset="1" stop-color="#fff3a8" stop-opacity="0"/></linearGradient>',
             '<linearGradient id="chromev" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#9aa6b4"/><stop offset="1" stop-color="#e9eef3"/></linearGradient>',
             '<radialGradient id="sun"><stop offset="0" stop-color="#fff2b0"/><stop offset=".6" stop-color="#ffd23f"/><stop offset="1" stop-color="#ff9a3c"/></radialGradient>',
             f'<clipPath id="strip"><rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="22"/></clipPath>')
    body = []
    body.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#sky)"/>')
    body.append(f'<circle cx="1010" cy="128" r="62" fill="url(#sun)"/>')
    for i in range(16):
        p1, p2 = polar(1010, 128, 76, i * 22.5 - 5), polar(1010, 128, 100, i * 22.5)
        p3 = polar(1010, 128, 76, i * 22.5 + 5)
        body.append(f'<path d="M{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}L{n(p3[0])} {n(p3[1])}Z" fill="#ffd23f" opacity=".7"/>')

    def layer(content, period, dur):
        return (f'<g style="--p:-{period}px;animation:scroll {dur}s linear infinite">{content}'
                f'<g transform="translate({period} 0)">{content}</g></g>')
    # far peaks (snow caps)
    r = RNG(4)
    P1 = 1280
    pts, x = [(0, 230)], 0
    peaks = []
    while x < P1:
        w = r.uniform(90, 170)
        h = r.uniform(90, 150)
        peaks.append((x + w / 2, 230 - h, w))
        x += w * 0.75
    far = []
    for cx, top, w in peaks:
        far.append(f'<path d="M{n(cx - w)} 232L{n(cx)} {n(top)}L{n(cx + w)} 232Z" fill="#3c2a7a" stroke="#2a1d5c" stroke-width="2"/>')
        sx = (cx - w * 0.28, top + (232 - top) * 0.28)
        sx2 = (cx + w * 0.28, top + (232 - top) * 0.28)
        far.append(f'<path d="M{n(cx)} {n(top)}L{n(sx2[0])} {n(sx2[1])}L{n(cx + w * 0.12)} {n(sx2[1] - 8)}L{n(cx)} {n(sx2[1] + 4)}'
                   f'L{n(cx - w * 0.14)} {n(sx[1] - 6)}L{n(sx[0])} {n(sx[1])}Z" fill="#f4f1ff"/>')
    body.append(layer("".join(far), P1, 90))
    # birds
    birds = []
    for i, (bx, by) in enumerate(((1300, 60), (1340, 76), (1380, 52), (1700, 90), (1735, 102))):
        birds.append(f'<g transform="translate({bx} {by})"><path d="M-9 0Q-4 -6 0 0Q4 -6 9 0" fill="none" stroke="{INK}" stroke-width="2.4" '
                     f'stroke-linecap="round" style="transform-origin:0 0;animation:flap .6s ease-in-out {-i * 0.13}s infinite"/></g>')
    body.append(f'<g style="animation:fly 26s linear infinite">{"".join(birds)}</g>')
    # mid hills with poplars
    P2 = 640
    hills = [f'<path d="M0 248C80 200 160 196 240 222C320 248 400 190 480 200C560 210 600 236 640 248L640 300L0 300Z" fill="#1f7a46"/>',
             f'<path d="M0 252C90 232 170 236 260 246C350 256 430 228 520 236C580 242 610 250 640 252L640 300L0 300Z" fill="#16613a"/>']
    for k, tx in enumerate((40, 128, 210, 330, 420, 552, 600)):
        ty = 236 - (k % 3) * 6
        hills.append(f'<path d="M{tx} {ty + 22}L{tx} {ty + 30}" stroke="#4a2c12" stroke-width="3"/>'
                     f'<path d="M{tx} {ty - 34}C{tx + 11} {ty - 16} {tx + 9} {ty + 14} {tx} {ty + 24}C{tx - 9} {ty + 14} {tx - 11} {ty - 16} {tx} {ty - 34}Z" fill="#0f5a2f" stroke="{INK}" stroke-width="2"/>'
                     f'<path d="M{tx - 2} {ty - 24}C{tx - 7} {ty - 8} {tx - 6} {ty + 6} {tx - 2} {ty + 16}" fill="none" stroke="#5bd38a" stroke-width="2.5" stroke-linecap="round"/>')
    body.append(layer("".join(hills), P2, 18))
    # road
    body.append(f'<rect x="0" y="252" width="{W}" height="48" fill="#3b3640"/>')
    body.append(f'<rect x="0" y="252" width="{W}" height="5" fill="#f2c14e"/>')
    P3 = 1920
    road = []
    for i in range(0, P3, 80):
        road.append(f'<rect x="{i}" y="276" width="44" height="5" rx="2" fill="#fff"/>')
    stones = [("VOICE AI", "3"), ("RAG", "12"), ("LLM EVALS", "27"), ("ML", "41"), ("SAAS", "58"), ("OPEN SOURCE", "73")]
    for i, (lab, km) in enumerate(stones):
        sx = 160 + i * 320
        road.append(f'<path d="M{sx - 34} 262L{sx - 34} 206Q{sx - 34} 180 {sx} 180Q{sx + 34} 180 {sx + 34} 206L{sx + 34} 262Z" fill="#fbfbf4" stroke="{INK}" stroke-width="3"/>')
        road.append(f'<path d="M{sx - 34} 214L{sx - 34} 206Q{sx - 34} 180 {sx} 180Q{sx + 34} 180 {sx + 34} 206L{sx + 34} 214Z" fill="#f2b705" stroke="{INK}" stroke-width="3"/>')
        fs = 21
        while F("tekob").width(lab, fs) > 62:
            fs -= 1
        rid, box, adv = d.text_def(F("tekob"), lab, sx, 210, fs, anchor="middle")
        road.append(f'<use href="#{rid}" fill="{INK}"/>')
        rid2, box2, adv2 = d.text_def(F("tekob"), km, sx, 246, 28, anchor="middle")
        road.append(f'<use href="#{rid2}" fill="{DRED}"/>')
        rid3, _, _ = d.text_def(F("teko"), "KM", sx, 258, 12, anchor="middle")
        road.append(f'<use href="#{rid3}" fill="{INK}"/>')
    body.append(layer("".join(road), P3, 9))
    # truck (bobbing) + exhaust
    puffs = "".join(f'<circle cx="198" cy="242" r="9" fill="#e9e3f0" style="transform-origin:198px 242px;animation:puff 1.6s ease-out {-i * 0.4}s infinite"/>' for i in range(4))
    body.append(puffs)
    body.append(f'<g style="animation:bounce .45s ease-in-out infinite">{truck(d, 210, GROUND + 2, 0.9)}</g>')
    d.add(f'<g clip-path="url(#strip)">{"".join(body)}</g>')
    d.add(f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="22" fill="none" stroke="{INK}" stroke-width="7"/>')
    return d


if __name__ == "__main__":
    import sys
    print(build().save(sys.argv[1] if len(sys.argv) > 1 else "../out/road.svg"))
