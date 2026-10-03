"""System architecture as a painted route board: requests ride little trucks through five stops."""
from ta_core import (BLUE, CREAM, DGREEN, DRED, GOLD, GREEN, INK, NIGHT, ORANGE, PINK, PURPLE, RED, SAFFRON, TEAL,
                     WHITE, Doc, n)
from ta_fonts import F
from ta_motifs import blossom, dots, leaf, rose, tape_defs

W, H = 1280, 640
ROAD = 352

STOPS = [
    ("CALLERS + CLIENTS", ["Phone: Vapi + Twilio", "Web and mobile apps", "Slack and e-mail bots"], ORANGE),
    ("EDGE", ["Cloudflare Workers", "BFF auth, httpOnly cookies", "Rate limits, webhooks"], PINK),
    ("SERVICES", ["NestJS + FastAPI", "Queues, retries, idempotency", "n8n workflows"], GREEN),
    ("AI LAYER", ["LLM router, small first", "Claude for the hard calls", "RAG + evals in CI"], BLUE),
    ("DATA", ["Postgres, row-level security", "Field-level encryption", "Object storage, Prometheus"], PURPLE),
]


def mini_truck(col):
    """Side-view mini truck, facing right; rear wheel ground point at (0, 0)."""
    return (f'<rect x="-8" y="-46" width="54" height="34" rx="3" fill="{col}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-8" y="-46" width="54" height="7" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="6" cy="-26" r="3" fill="#fff"/><circle cx="18" cy="-26" r="3" fill="#fff"/><circle cx="30" cy="-26" r="3" fill="#fff"/>'
            f'<path d="M48 -12V-40H64Q70 -40 73 -32L78 -22V-12Z" fill="#f2b705" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M53 -36H63Q66 -36 68 -31L71 -26H53Z" fill="#9fd8ff" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M40 -60Q62 -64 80 -58L76 -46H44Z" fill="{RED}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="-10" y="-14" width="90" height="6" fill="#2a2a2a"/>'
            f'<circle cx="8" cy="-7" r="8" fill="#151515" stroke="{INK}" stroke-width="2"/><circle cx="8" cy="-7" r="3.4" fill="{GOLD}"/>'
            f'<circle cx="62" cy="-7" r="8" fill="#151515" stroke="{INK}" stroke-width="2"/><circle cx="62" cy="-7" r="3.4" fill="{GOLD}"/>'
            f'<path d="M80 -20L120 -28L120 -12Z" fill="#fff3a8" opacity=".45"/>')


def build():
    d = Doc(W, H, "System architecture: callers and clients, edge, services, AI layer, data",
            "A request's route through a production AI system: phone, web and Slack clients; Cloudflare Workers edge with BFF auth; "
            "NestJS and FastAPI services with job queues, retries and n8n; an LLM router that sends small models first and Claude "
            "for hard calls, with RAG and evals in CI; multi-tenant Postgres with row-level security, field-level encryption, object "
            "storage and Prometheus.")
    d.keyframes("drive", "from{transform:translateX(-140px)}to{transform:translateX(1420px)}")
    d.keyframes("pulse", "0%,100%{transform:scale(1)}50%{transform:scale(1.12)}")
    tape = tape_defs(d, 16)
    d.add(f'<rect x="4" y="8" width="{W - 8}" height="{H - 10}" rx="26" fill="{INK}" opacity=".3"/>'
          f'<rect x="4" y="4" width="{W - 8}" height="{H - 10}" rx="26" fill="{INK}"/>'
          f'<rect x="10" y="10" width="{W - 20}" height="{H - 22}" rx="21" fill="url(#{tape})"/>'
          f'<rect x="27" y="27" width="{W - 54}" height="{H - 56}" rx="12" fill="{INK}"/>'
          f'<rect x="30" y="30" width="{W - 60}" height="{H - 62}" rx="10" fill="#fbf0d2"/>')
    # paper texture: faint painted stripes
    for i in range(18):
        d.add(f'<path d="M30 {48 + i * 32}H{W - 30}" stroke="#e9d9ad" stroke-width="1" opacity=".7"/>')
    # corner flowers
    for (cx, cy, t) in ((70, 70, "red"), (W - 70, 70, "pink"), (70, H - 74, "yellow"), (W - 70, H - 74, "blue")):
        d.add(leaf(cx, cy, 34, 11, 45 if cx < W / 2 else 135) + leaf(cx, cy, 34, 11, -45 if cx < W / 2 else -135))
        d.add(rose(cx, cy, 22, t, seed=cx + cy))
    # road
    d.add(f'<rect x="30" y="{ROAD - 26}" width="{W - 60}" height="52" fill="#3b3640"/>'
          f'<rect x="30" y="{ROAD - 26}" width="{W - 60}" height="5" fill="#f2c14e"/>'
          f'<rect x="30" y="{ROAD + 21}" width="{W - 60}" height="5" fill="#f2c14e"/>')
    for x in range(40, W - 40, 56):
        d.add(f'<rect x="{x}" y="{ROAD - 2}" width="30" height="4" rx="2" fill="#fff" opacity=".9"/>')
    xs = [192, 416, 640, 864, 1088]
    bw, bh = 296, 150
    fs = 18.0
    while max(F("pop").width(ln, fs) for _, lines, _ in STOPS for ln in lines) > bw - 26:
        fs -= 0.25
    for i, ((title, lines, col), x) in enumerate(zip(STOPS, xs)):
        above = i % 2 == 0
        by = ROAD - 60 - bh if above else ROAD + 60
        post_y0, post_y1 = (by + bh, ROAD - 26) if above else (ROAD + 26, by)
        d.add(f'<rect x="{x - 5}" y="{post_y0}" width="10" height="{post_y1 - post_y0}" fill="#8a5a22" stroke="{INK}" stroke-width="2.5"/>')
        d.add(f'<rect x="{x - bw / 2 + 4}" y="{by + 6}" width="{bw}" height="{bh}" rx="12" fill="{INK}" opacity=".3"/>'
              f'<rect x="{x - bw / 2}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#fff8e6" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="{x - bw / 2}" y="{by}" width="{bw}" height="40" rx="12" fill="{col}" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="{x - bw / 2 + 2}" y="{by + 26}" width="{bw - 4}" height="14" fill="{col}"/>')
        ts = 26
        while F("tekob").width(title, ts, 0.03) > bw - 70:
            ts -= 1
        d.painted(F("tekob"), title, x + 14, by + 30, ts, WHITE, ow=2.6, shadow=(1.5, 2), ls=0.03)
        d.add(f'<circle cx="{x - bw / 2 + 24}" cy="{by + 20}" r="14" fill="#fff" stroke="{INK}" stroke-width="3"/>')
        d.text(F("tekob"), str(i + 1), x - bw / 2 + 24, by + 29, 24, fill=col, anchor="middle")
        for k, ln in enumerate(lines):
            d.text(F("pop"), ln, x - bw / 2 + 16, by + 72 + k * 27, fs, fill="#2a1a12")
        d.add(dots(x - bw / 2 + 14, by + bh - 12, x + bw / 2 - 14, by + bh - 12, 11, 2, col, GOLD))
        # station badge on the road
        d.add(f'<g style="transform-origin:{x}px {ROAD}px;animation:pulse 2.4s ease-in-out {-i * 0.4}s infinite">'
              f'<circle cx="{x}" cy="{ROAD}" r="20" fill="{col}" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="{x}" cy="{ROAD}" r="9" fill="#fff" stroke="{INK}" stroke-width="2.5"/></g>')
    # requests riding through
    d.define(f'<clipPath id="lane"><rect x="30" y="{ROAD - 80}" width="{W - 60}" height="140"/></clipPath>')
    trucks = "".join(f'<g style="animation:drive 16s linear {-i * 4}s infinite"><g transform="translate(0 {ROAD + 22})">{mini_truck(col)}</g></g>'
                     for i, col in enumerate((RED, BLUE, GREEN, PURPLE)))
    d.add(f'<g clip-path="url(#lane)">{trucks}</g>')
    # header ribbon
    title = "THE ROUTE OF A REQUEST"
    tw = F("tekob").width(title, 30, 0.05) + 70
    d.add(f'<path d="M{n(W / 2 - tw / 2)} 44H{n(W / 2 + tw / 2)}L{n(W / 2 + tw / 2 - 14)} 64L{n(W / 2 + tw / 2)} 84H{n(W / 2 - tw / 2)}L{n(W / 2 - tw / 2 + 14)} 64Z" '
          f'fill="{RED}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    d.painted(F("tekob"), title, W / 2, 75, 30, WHITE, ow=2.8, shadow=(1.5, 2), ls=0.05)
    return d


if __name__ == "__main__":
    import sys
    print(build().save(sys.argv[1] if len(sys.argv) > 1 else "../out/architecture.svg"))
