"""Call to action: a pair of painted mudflaps ('horn do' / 'rasta lo') around a signboard."""
import json
import os

from ta_core import (BLUE, CREAM, DGREEN, DRED, GOLD, GREEN, INK, NIGHT, ORANGE, PINK, PURPLE, RED, SAFFRON, TEAL,
                     WHITE, Doc, arc_brush, brush, n)
from ta_fonts import F
from ta_motifs import TWINKLE, blossom, chain, dots, lamp, leaf, rose, sparkle, tape_defs

W, H = 1280, 470
HERE = os.path.dirname(os.path.abspath(__file__))
X_LOGO = "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"


def eye(cx, cy, s=1.0):
    e = f"M{n(cx - 58 * s)} {n(cy)}Q{n(cx)} {n(cy - 50 * s)} {n(cx + 58 * s)} {n(cy)}Q{n(cx)} {n(cy + 46 * s)} {n(cx - 58 * s)} {n(cy)}Z"
    out = [f'<path d="{brush((cx - 60 * s, cy - 40 * s), (cx - 20 * s, cy - 66 * s), (cx + 20 * s, cy - 66 * s), (cx + 60 * s, cy - 40 * s), 12 * s)}" fill="{GOLD}"/>',
           f'<path d="{e}" fill="#fff" stroke="{GOLD}" stroke-width="{n(5 * s)}"/>',
           f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(22 * s)}" fill="{BLUE}"/><circle cx="{n(cx)}" cy="{n(cy)}" r="{n(14 * s)}" fill="#4fc3ff"/>'
           f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(8 * s)}" fill="{INK}"/><circle cx="{n(cx - 6 * s)}" cy="{n(cy - 7 * s)}" r="{n(4 * s)}" fill="#fff"/>']
    for k in range(7):
        t = 0.15 + k * 0.117
        bx = (1 - t) ** 2 * (cx - 58 * s) + 2 * (1 - t) * t * cx + t * t * (cx + 58 * s)
        by = (1 - t) ** 2 * cy + 2 * (1 - t) * t * (cy - 50 * s) + t * t * cy
        out.append(f'<path d="M{n(bx)} {n(by)}L{n(bx + (t - 0.5) * 18 * s)} {n(by - 14 * s)}" stroke="{GOLD}" stroke-width="{n(4 * s)}" stroke-linecap="round"/>')
    return "".join(out)


def mudflap(doc, x, y, w, h, word, col, delay=0.0):
    doc.keyframes("flap", "0%,100%{transform:rotate(-2.2deg)}50%{transform:rotate(2.2deg)}")
    g = []
    body = f"M{x} {y}H{x + w}V{y + h - 30}Q{x + w} {y + h} {x + w - 30} {y + h}H{x + 30}Q{x} {y + h} {x} {y + h - 30}Z"
    g.append(f'<path d="{body}" fill="#141414" stroke="{INK}" stroke-width="5"/>')
    g.append(f'<path d="M{x + 12} {y + 14}H{x + w - 12}V{y + h - 36}Q{x + w - 12} {y + h - 12} {x + w - 36} {y + h - 12}H{x + 36}Q{x + 12} {y + h - 12} {x + 12} {y + h - 36}Z" '
             f'fill="none" stroke="#c9d1db" stroke-width="3" stroke-dasharray="1 13" stroke-linecap="round"/>')
    g.append(eye(x + w / 2, y + 96, 1.15))
    for i, wd in enumerate(word):
        size = 46
        while F("ultra").width(wd, size) > w - 44:
            size -= 1
        rid, box, adv = doc.text_def(F("ultra"), wd, x + w / 2, y + 210 + i * 58, size, anchor="middle")
        g.append(f'<use href="#{rid}" fill="{col}" stroke="{col}" stroke-width="10" stroke-linejoin="round" transform="translate(2 3)"/>'
                 f'<use href="#{rid}" fill="{INK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/><use href="#{rid}" fill="#fff"/>')
    g.append(blossom(x + 34, y + h - 40, 12, color=PINK, center=SAFFRON) + blossom(x + w - 34, y + h - 40, 12, color=SAFFRON, center=RED))
    g.append(dots(x + 56, y + h - 40, x + w - 56, y + h - 40, 15, 3, col, WHITE))
    bracket = (f'<rect x="{x + w / 2 - 40}" y="{y - 22}" width="80" height="26" rx="6" fill="url(#chromev)" stroke="{INK}" stroke-width="3"/>'
               f'<circle cx="{x + w / 2 - 24}" cy="{y - 9}" r="4" fill="{INK}"/><circle cx="{x + w / 2 + 24}" cy="{y - 9}" r="4" fill="{INK}"/>')
    return (bracket + f'<g style="transform-origin:{x + w / 2}px {y}px;animation:flap 3.2s ease-in-out {delay}s infinite">{"".join(g)}</g>')


def build():
    d = Doc(W, H, "Open to contract work: voice AI agents, RAG, LLM evals, multi-tenant SaaS and automation",
            "Two painted truck mudflaps read 'horn do' and 'rasta lo' (honk, and I'll make way) around a signboard: "
            "open to contract work, message @AzamIntikhab on X or find intikhab49 on GitHub.")
    d.keyframes("twinkle", TWINKLE)
    d.define('<linearGradient id="chromev" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#9aa6b4"/><stop offset="1" stop-color="#e9eef3"/></linearGradient>')
    d.add(mudflap(d, 40, 40, 250, 400, ["HORN", "DO"], RED))
    d.add(mudflap(d, W - 290, 40, 250, 400, ["RASTA", "LO"], GREEN, delay=-1.6))
    # signboard
    tape = tape_defs(d, 16)
    bx0, bx1, by0, by1 = 322, W - 322, 34, 446
    d.add(f'<rect x="{bx0}" y="{by0 + 6}" width="{bx1 - bx0}" height="{by1 - by0}" rx="22" fill="{INK}" opacity=".3"/>'
          f'<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" rx="22" fill="{INK}"/>'
          f'<rect x="{bx0 + 6}" y="{by0 + 6}" width="{bx1 - bx0 - 12}" height="{by1 - by0 - 12}" rx="18" fill="url(#{tape})"/>'
          f'<rect x="{bx0 + 22}" y="{by0 + 22}" width="{bx1 - bx0 - 44}" height="{by1 - by0 - 44}" rx="10" fill="{INK}"/>'
          f'<rect x="{bx0 + 25}" y="{by0 + 25}" width="{bx1 - bx0 - 50}" height="{by1 - by0 - 50}" rx="8" fill="#fff6dc"/>')
    cx = W / 2
    d.add(dots(bx0 + 46, by0 + 44, bx1 - 46, by0 + 44, 16, 2.6, RED, GREEN))
    d.painted(F("shri"), "open to", cx, 120, 40, DRED, ow=3.4, shadow=(2, 3))
    size = 64
    while F("ultra").width("CONTRACT WORK", size, 0.01) > bx1 - bx0 - 90:
        size -= 1
    d.painted(F("ultra"), "CONTRACT WORK", cx, 196, size, None, ow=5, shadow=(4, 5), shadow_fill="#5c0710", ls=0.01,
              fills=[RED, "#f29100", GREEN, PINK, BLUE, ORANGE, TEAL, PURPLE, RED, GREEN, "#f29100", BLUE])
    sub = "VOICE AI AGENTS  ·  RAG  ·  LLM EVALS  ·  MULTI-TENANT SAAS  ·  AUTOMATION"
    ss = 24
    while F("tekob").width(sub, ss, 0.03) > bx1 - bx0 - 90:
        ss -= 0.5
    d.text(F("tekob"), sub, cx, 238, ss, fill=INK, anchor="middle", ls=0.03)
    d.add(dots(bx0 + 46, 256, bx1 - 46, 256, 16, 2.4, GOLD, RED))
    # contact plates
    plates = [("X", "@AzamIntikhab", INK), ("GH", "github.com/intikhab49", "#24292f")]
    py = 276
    for i, (kind, label, col) in enumerate(plates):
        tw = F("popb").width(label, 26) + 80
        px = cx - tw / 2
        yy = py + i * 60
        d.add(f'<rect x="{n(px)}" y="{yy}" width="{n(tw)}" height="50" rx="12" fill="{col}" stroke="{INK}" stroke-width="3"/>')
        if kind == "X":
            d.add(f'<path d="{X_LOGO}" transform="translate({n(px + 16)} {yy + 13}) scale(1)" fill="#fff"/>')
        else:
            gh = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))["github"]["d"]
            d.add(f'<path d="{gh}" transform="translate({n(px + 16)} {yy + 13})" fill="#fff"/>')
        d.text(F("popb"), label, px + 56, yy + 35, 26, fill="#fff")
    d.text(F("pop"), "horn do, rasta lo: honk, and I'll make way", cx, 408, 17, fill="#6b4b2a", anchor="middle")
    for (sx, sy) in ((bx0 + 70, 120), (bx1 - 70, 120), (bx0 + 66, 330), (bx1 - 66, 330)):
        d.add(rose(sx, sy, 26, "red" if sx < cx else "pink", seed=int(sx + sy)))
        d.add(leaf(sx, sy + 24, 30, 10, 100) + leaf(sx, sy + 24, 30, 10, 80))
    return d


if __name__ == "__main__":
    import sys
    print(build().save(sys.argv[1] if len(sys.argv) > 1 else "../out/cta.svg"))
