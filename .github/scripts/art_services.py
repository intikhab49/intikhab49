"""'What I build': six painted plates, each with a small animated emblem."""
from ta_core import (BLUE, CREAM, DBLUE, DGREEN, DRED, GOLD, GREEN, INK, NIGHT, ORANGE, PINK, PURPLE, RED, SAFFRON,
                     TEAL, WHITE, Doc, arc_brush, brush, n, petal_d, polar)
from ta_fonts import F
from ta_motifs import TWINKLE, blossom, dots, leaf, rose, sparkle, tape_defs

W, H = 1280, 600

TILES = [
    ("VOICE AI AGENTS", "Vapi + Twilio receptionists and outbound callers, wired into CRMs, payments and SMS.", ORANGE, "mic"),
    ("RAG + LLM AGENTS", "Knowledge-base chatbots with tool calling and memory, judged by cost per correct answer.", SAFFRON, "lantern"),
    ("EVALS + RESEARCH", "Calibration, benchmarks and backtests that publish the losing numbers too.", TEAL, "gauge"),
    ("MULTI-TENANT SAAS", "Row-level security, BFF auth, field-level encryption and event-driven jobs.", GREEN, "haveli"),
    ("AGENTIC CODING", "Claude Code, Codex and DeepSeek in parallel, held to spec files and test gates.", PINK, "terminal"),
    ("AUTOMATION + DATA", "n8n and Cloudflare Workers glue, lead pipelines, scraping and enrichment.", PURPLE, "gears"),
]


def emblem(doc, kind, cx, cy, col):
    o = []
    if kind == "mic":
        doc.keyframes("ring", "0%{transform:scale(.5);opacity:0}25%{opacity:1}100%{transform:scale(1.3);opacity:0}")
        for i in range(2):
            for side in (-1, 1):
                a0, a1 = (-40, 40) if side > 0 else (140, 220)
                o.append(f'<path d="{arc_brush(cx, cy - 8, 40, a0, a1, 7)}" fill="{GOLD}" style="transform-origin:{cx}px {cy - 8}px;animation:ring 2s ease-out {i}s infinite"/>')
        o.append(f'<rect x="{cx - 17}" y="{cy - 46}" width="34" height="56" rx="17" fill="{INK}"/>'
                 f'<rect x="{cx - 14}" y="{cy - 43}" width="28" height="50" rx="14" fill="#d9dee6"/>')
        for k in range(5):
            o.append(f'<path d="M{cx - 11} {cy - 34 + k * 8}H{cx + 11}" stroke="#7d8896" stroke-width="2.5"/>')
        o.append(f'<path d="M{cx - 26} {cy - 4}Q{cx - 26} {cy + 24} {cx} {cy + 24}Q{cx + 26} {cy + 24} {cx + 26} {cy - 4}" fill="none" stroke="{INK}" stroke-width="7"/>'
                 f'<path d="M{cx - 26} {cy - 4}Q{cx - 26} {cy + 24} {cx} {cy + 24}Q{cx + 26} {cy + 24} {cx + 26} {cy - 4}" fill="none" stroke="{GOLD}" stroke-width="3.5"/>'
                 f'<path d="M{cx} {cy + 24}V{cy + 40}M{cx - 18} {cy + 42}H{cx + 18}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="M{cx} {cy + 24}V{cy + 40}M{cx - 18} {cy + 42}H{cx + 18}" stroke="{GOLD}" stroke-width="3.5" stroke-linecap="round"/>'
                 f'<path d="{brush((cx - 8, cy - 38), (cx - 10, cy - 24), (cx - 10, cy - 10), (cx - 8, cy + 2), 5)}" fill="#fff"/>')
    elif kind == "lantern":
        doc.keyframes("flick", "0%,100%{transform:scale(1,1)}30%{transform:scale(.9,1.08)}60%{transform:scale(1.06,.94)}")
        doc.keyframes("glow", "0%,100%{opacity:.55}50%{opacity:.9}")
        gid = doc.uid("lg")
        doc.define(f'<radialGradient id="{gid}"><stop offset="0" stop-color="#ffe9a0"/><stop offset="1" stop-color="#ffb400" stop-opacity="0"/></radialGradient>')
        o.append(f'<circle cx="{cx}" cy="{cy + 4}" r="54" fill="url(#{gid})" style="animation:glow 1.6s ease-in-out infinite"/>')
        o.append(f'<path d="M{cx - 14} {cy - 48}Q{cx} {cy - 64} {cx + 14} {cy - 48}" fill="none" stroke="{INK}" stroke-width="5"/>'
                 f'<rect x="{cx - 24}" y="{cy - 48}" width="48" height="10" rx="3" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M{cx - 18} {cy - 38}C{cx - 30} {cy - 20} {cx - 30} {cy + 16} {cx - 16} {cy + 28}L{cx + 16} {cy + 28}C{cx + 30} {cy + 16} {cx + 30} {cy - 20} {cx + 18} {cy - 38}Z" '
                 f'fill="#fff4c8" fill-opacity=".55" stroke="{INK}" stroke-width="4"/>'
                 f'<g style="transform-origin:{cx}px {cy + 14}px;animation:flick .9s ease-in-out infinite">'
                 f'<path d="M{cx} {cy - 16}C{cx + 10} {cy - 2} {cx + 9} {cy + 14} {cx} {cy + 14}C{cx - 9} {cy + 14} {cx - 10} {cy - 2} {cx} {cy - 16}Z" fill="{ORANGE}"/>'
                 f'<path d="M{cx} {cy - 4}C{cx + 5} {cy + 4} {cx + 4} {cy + 12} {cx} {cy + 12}C{cx - 4} {cy + 12} {cx - 5} {cy + 4} {cx} {cy - 4}Z" fill="#fff6c0"/></g>'
                 f'<rect x="{cx - 28}" y="{cy + 26}" width="56" height="14" rx="4" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M{cx - 22} {cy - 30}L{cx - 22} {cy + 24}M{cx + 22} {cy - 30}L{cx + 22} {cy + 24}" stroke="{INK}" stroke-width="3"/>')
    elif kind == "gauge":
        doc.keyframes("needle", "0%,100%{transform:rotate(-70deg)}45%,60%{transform:rotate(48deg)}75%{transform:rotate(30deg)}")
        o.append(f'<circle cx="{cx}" cy="{cy}" r="48" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="43" fill="#fff6dc"/>')
        segs = [(GREEN, 150, 210), (SAFFRON, 210, 270), (ORANGE, 270, 330), (RED, 330, 390)]
        for c, a0, a1 in segs:
            o.append(f'<path d="{arc_brush(cx, cy, 34, a0 + 2, a1 - 2, 9, peak=0.5)}" fill="{c}"/>')
        for k in range(9):
            a = 150 + k * 30
            p1, p2 = polar(cx, cy, 24, a), polar(cx, cy, 30, a)
            o.append(f'<path d="M{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}" stroke="{INK}" stroke-width="2.5"/>')
        o.append(f'<g style="transform-origin:{cx}px {cy}px;animation:needle 4s ease-in-out infinite">'
                 f'<path d="M{cx - 4} {cy}L{cx} {cy - 38}L{cx + 4} {cy}Z" fill="{RED}" stroke="{INK}" stroke-width="2"/></g>'
                 f'<circle cx="{cx}" cy="{cy}" r="7" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="3" fill="{GOLD}"/>')
    elif kind == "haveli":
        doc.keyframes("lights", "0%,100%{fill:#3a2a12}50%{fill:#ffd23f}")
        o.append(f'<path d="M{cx - 44} {cy + 44}V{cy - 22}H{cx + 44}V{cy + 44}Z" fill="#e8b46a" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M{cx - 50} {cy - 22}H{cx + 50}L{cx + 44} {cy - 32}H{cx - 44}Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M{cx - 18} {cy - 32}Q{cx - 18} {cy - 58} {cx} {cy - 62}Q{cx + 18} {cy - 58} {cx + 18} {cy - 32}Z" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M{cx} {cy - 62}V{cy - 72}" stroke="{INK}" stroke-width="3"/><circle cx="{cx}" cy="{cy - 74}" r="3" fill="{GOLD}"/>')
        k = 0
        for row in range(2):
            for col in range(3):
                wx, wy = cx - 30 + col * 30, cy - 12 + row * 26
                o.append(f'<path d="M{wx - 8} {wy + 16}V{wy + 2}Q{wx - 8} {wy - 6} {wx} {wy - 7}Q{wx + 8} {wy - 6} {wx + 8} {wy + 2}V{wy + 16}Z" '
                         f'stroke="{INK}" stroke-width="2.5" style="fill:#3a2a12;animation:lights 3s steps(1) {-k * 0.5}s infinite"/>')
                k += 1
    elif kind == "terminal":
        doc.keyframes("cur", "0%,49%{opacity:1}50%,100%{opacity:0}")
        o.append(f'<rect x="{cx - 50}" y="{cy - 40}" width="100" height="80" rx="9" fill="{INK}"/>'
                 f'<rect x="{cx - 46}" y="{cy - 36}" width="92" height="72" rx="6" fill="#1b1830"/>'
                 f'<rect x="{cx - 46}" y="{cy - 36}" width="92" height="14" rx="6" fill="#3a3560"/>'
                 f'<circle cx="{cx - 37}" cy="{cy - 29}" r="3" fill="{RED}"/><circle cx="{cx - 28}" cy="{cy - 29}" r="3" fill="{SAFFRON}"/><circle cx="{cx - 19}" cy="{cy - 29}" r="3" fill="{GREEN}"/>')
        for i, c in enumerate((ORANGE, TEAL, PINK)):
            y = cy - 10 + i * 17
            o.append(f'<path d="M{cx - 38} {y - 5}L{cx - 32} {y}L{cx - 38} {y + 5}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<rect x="{cx - 26}" y="{y - 2}" width="{30 + i * 8}" height="4" rx="2" fill="#8a85b0"/>'
                     f'<rect x="{cx + 8 + i * 8}" y="{y - 6}" width="8" height="12" fill="{c}" style="animation:cur 1s steps(1) {-i * 0.33}s infinite"/>')
    elif kind == "gears":
        doc.keyframes("spin", "to{transform:rotate(360deg)}")

        def gear(gx, gy, r, teeth, fill, rev=False, dur=8):
            parts = []
            for t in range(teeth):
                a = t * 360 / teeth
                parts.append(f'<path d="{petal_d(gx, gy, r + 12, 9, a, base=r - 6, roundness=0.5)}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>')
            parts.append(f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
                         f'<circle cx="{gx}" cy="{gy}" r="{r * 0.45}" fill="#fff6dc" stroke="{INK}" stroke-width="3"/>'
                         f'<circle cx="{gx}" cy="{gy}" r="{r * 0.18}" fill="{RED}"/>')
            d = "reverse" if rev else "normal"
            return f'<g style="transform-origin:{gx}px {gy}px;animation:spin {dur}s linear infinite {d}">{"".join(parts)}</g>'
        o.append(gear(cx - 10, cy + 6, 26, 8, SAFFRON))
        o.append(gear(cx + 34, cy - 30, 15, 6, PINK, True, 5))
    return "".join(o)


def build():
    d = Doc(W, H, "What I build: voice AI agents, RAG and LLM agents, evals and research, multi-tenant SaaS, agentic coding, automation",
            "Six hand-painted plates in Pakistani truck-art style with small animated emblems.")
    d.keyframes("twinkle", TWINKLE)
    tape = tape_defs(d, 18)
    d.add(f'<rect x="4" y="8" width="{W - 8}" height="{H - 10}" rx="26" fill="{INK}" opacity=".3"/>'
          f'<rect x="4" y="4" width="{W - 8}" height="{H - 10}" rx="26" fill="{INK}"/>'
          f'<rect x="10" y="10" width="{W - 20}" height="{H - 22}" rx="21" fill="url(#{tape})"/>'
          f'<rect x="29" y="29" width="{W - 58}" height="{H - 60}" rx="12" fill="{INK}"/>'
          f'<rect x="32" y="32" width="{W - 64}" height="{H - 66}" rx="10" fill="{NIGHT}"/>')
    tw, th, gx, gy = 392, 252, 16, 18
    x0 = (W - (3 * tw + 2 * gx)) / 2
    y0 = 46
    for i, (title, desc, col, kind) in enumerate(TILES):
        x = x0 + (i % 3) * (tw + gx)
        y = y0 + (i // 3) * (th + gy)
        d.add(f'<rect x="{n(x)}" y="{y}" width="{tw}" height="{th}" rx="16" fill="#1b1634" stroke="{col}" stroke-width="3"/>')
        d.add(dots(x + 18, y + 12, x + tw - 18, y + 12, 14, 2.2, col, GOLD))
        d.add(dots(x + 18, y + th - 12, x + tw - 18, y + th - 12, 14, 2.2, GOLD, col))
        mx, my = x + 82, y + 118
        d.add(f'<circle cx="{n(mx)}" cy="{my}" r="66" fill="{INK}"/><circle cx="{n(mx)}" cy="{my}" r="62" fill="{col}"/>'
              f'<circle cx="{n(mx)}" cy="{my}" r="54" fill="#2a2150"/>')
        for k in range(16):
            px, py = polar(mx, my, 58, k * 22.5)
            d.add(f'<circle cx="{n(px)}" cy="{n(py)}" r="2.2" fill="#fff" opacity=".85"/>')
        d.add(emblem(d, kind, mx, my, col))
        tx = x + 164
        size = 34
        while F("tekob").width(title, size, 0.02) > tw - 180:
            size -= 1
        d.painted(F("tekob"), title, tx, y + 76, size, col, ow=3.2, shadow=(2, 3), anchor="start", ls=0.02)
        fs = 18
        words, lines, cur = desc.split(), [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if F("pop").width(t, fs) <= tw - 182:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        lines.append(cur)
        for k, ln in enumerate(lines[:5]):
            d.text(F("pop"), ln, tx, y + 110 + k * 26, fs, fill="#f3ead6")
    return d


if __name__ == "__main__":
    import sys
    print(build().save(sys.argv[1] if len(sys.argv) > 1 else "../out/services.svg"))
