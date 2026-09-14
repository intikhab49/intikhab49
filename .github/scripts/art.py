"""Hand-built profile art ("sunset circuit" theme). Standard library only.

Run from the repo root:  python .github/scripts/art.py   ->  writes assets/*.svg
Logos: Simple Icons (CC0), cached in icons.json next to this file.
"""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))

BG, CARD, EDGE = "#0A0A14", "#12121F", "#26263D"
TEXT, MUTED = "#F6F4FF", "#A3A1BE"
CORAL, AMBER, LIME, PINK, BLUE = "#FF5C39", "#FFB224", "#A3F547", "#FF3D9A", "#5B8CFF"
VIOLET = "#B794FF"
SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def x(s):
    return escape(str(s))


def wrap(text, n):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


CSS = f"""<style>
.sans{{font-family:{SANS};}} .mono{{font-family:{MONO};letter-spacing:1.2px;}}
.fx{{transform-box:fill-box;transform-origin:center;}}
.blob{{animation:float 14s ease-in-out infinite alternate;}}
.b2{{animation-duration:18s;animation-direction:alternate-reverse;}} .b3{{animation-duration:22s;}}
@keyframes float{{from{{transform:translate(0,0) scale(1);}} to{{transform:translate(60px,-40px) scale(1.15);}}}}
.spin{{animation:spin 16s linear infinite;}} .rspin{{animation:spin 24s linear infinite reverse;}}
@keyframes spin{{to{{transform:rotate(360deg);}}}}
.eq{{animation:eq 1.1s ease-in-out infinite alternate;transform-origin:center;transform-box:fill-box;}}
@keyframes eq{{from{{transform:scaleY(.22);}} to{{transform:scaleY(1);}}}}
.pulse{{animation:pulse 2s ease-in-out infinite;}}
@keyframes pulse{{0%,100%{{opacity:1;}} 50%{{opacity:.25;}}}}
.ring{{animation:ring 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center;}}
@keyframes ring{{from{{transform:scale(.3);opacity:.9;}} to{{transform:scale(1.6);opacity:0;}}}}
.draw{{stroke-dasharray:1;animation:draw 4.5s ease-out infinite backwards;}}
@keyframes draw{{0%{{stroke-dashoffset:1;}} 60%,100%{{stroke-dashoffset:0;}}}}
.rot{{opacity:0;animation:rot 15s infinite both;}}
@keyframes rot{{0%{{opacity:0;transform:translateY(16px);}} 3%,17%{{opacity:1;transform:translateY(0);}} 20%,100%{{opacity:0;transform:translateY(-16px);}}}}
.move{{animation:move 2.6s linear infinite;}}
@keyframes move{{from{{transform:translateX(0);opacity:0;}} 15%{{opacity:1;}} 85%{{opacity:1;}} to{{transform:translateX(var(--dx,120px));opacity:0;}}}}
.drop{{animation:drop 3s ease-out infinite both;}}
@keyframes drop{{0%{{transform:translateY(-18px);opacity:0;}} 20%,80%{{transform:translateY(0);opacity:1;}} 100%{{opacity:0;}}}}
.scan{{animation:scan 2.8s ease-in-out infinite alternate;}}
@keyframes scan{{from{{transform:translateY(0);}} to{{transform:translateY(var(--dy,80px));}}}}
.shine{{animation:shine 5s linear infinite;}}
@keyframes shine{{from{{transform:translateX(-400px);}} to{{transform:translateX(1400px);}}}}
.enter{{animation:enter .9s cubic-bezier(.2,.8,.2,1) both;}}
@keyframes enter{{from{{transform:translateY(-14px);opacity:0;}} to{{transform:translateY(0);opacity:1;}}}}
.grow{{animation:grow 1.4s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:bottom;}}
@keyframes grow{{from{{transform:scaleY(0);}} to{{transform:scaleY(1);}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;}} .rot{{opacity:0;}} .r0{{opacity:1;}}}}
</style>"""


def defs(uid):
    return f"""<defs>
<linearGradient id="sun{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}"/><stop offset=".5" stop-color="{CORAL}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity=".9"/><stop offset=".5" stop-color="{PINK}" stop-opacity=".35"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".8"/></linearGradient>
<filter id="blur{uid}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="46"/></filter>
<filter id="glow{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="dots{uid}" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{EDGE}"/></pattern>
</defs>"""


def svg(w, h, title, body, uid="", blobs=True):
    bl = ""
    if blobs:
        bl = (f'<g filter="url(#blur{uid})" opacity=".55">'
              f'<circle class="blob" cx="{w*.12:.0f}" cy="{h*.2:.0f}" r="{min(w,h)*.32:.0f}" fill="{CORAL}"/>'
              f'<circle class="blob b2" cx="{w*.78:.0f}" cy="{h*.85:.0f}" r="{min(w,h)*.3:.0f}" fill="{BLUE}"/>'
              f'<circle class="blob b3" cx="{w*.55:.0f}" cy="{h*.1:.0f}" r="{min(w,h)*.22:.0f}" fill="{PINK}"/></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{x(title)}">'
            f'<title>{x(title)}</title>{CSS}{defs(uid)}'
            f'<clipPath id="clip{uid}"><rect width="{w}" height="{h}" rx="20"/></clipPath>'
            f'<g clip-path="url(#clip{uid})"><rect width="{w}" height="{h}" fill="{BG}"/>{bl}'
            f'<rect width="{w}" height="{h}" fill="url(#dots{uid})" opacity=".6"/>{body}</g>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="19" fill="none" stroke="url(#edge{uid})" stroke-width="1.5"/></svg>')


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return .2126 * r + .7152 * g + .0722 * b


def logo(slug, cx, cy, size, color=None):
    """Simple Icons logo centred at (cx, cy); falls back to a monogram."""
    if slug in ICONS:
        ic = ICONS[slug]
        c = color or (ic["hex"] if lum(ic["hex"]) > .28 else TEXT)
        s = size / 24
        return f'<path transform="translate({cx - size/2:.1f} {cy - size/2:.1f}) scale({s:.3f})" d="{ic["d"]}" fill="{c}"/>'
    label = {"vapi": "V", "lightgbm": "LG", "xgboost": "XG", "chromadb": "C", "openrouter": "OR", "mcp": "MCP", "retell": "RT",
             "notebooklm": "NB", "neon": "NE", "betterauth": "BA", "playwright": "PW", "drissionpage": "DP"}.get(slug, slug[:2].upper())
    return (f'<rect x="{cx - size/2:.1f}" y="{cy - size/2:.1f}" width="{size}" height="{size}" rx="{size*.25:.1f}" fill="url(#sun)"/>'
            f'<text x="{cx}" y="{cy + size*.18:.1f}" class="sans" font-size="{size*(.46 if len(label) < 3 else .32):.0f}" font-weight="800" fill="{BG}" text-anchor="middle">{x(label)}</text>')


def chip(px, py, label, color, slug=None):
    w = len(label) * 7.4 + 26 + (18 if slug else 0)
    icon = logo(slug, px + 17, py + 13, 13) if slug else ""
    tx = px + (30 if slug else 13)
    return (f'<rect x="{px}" y="{py}" width="{w:.0f}" height="26" rx="13" fill="{CARD}" stroke="{color}" stroke-opacity=".55"/>'
            f'{icon}<text x="{tx}" y="{py + 17.5}" class="mono" font-size="11" fill="{color}">{x(label)}</text>'), w


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 500
    roles = [("voice AI agents", "that answer real calls", CORAL), ("RAG chatbots", "that know your documents", PINK),
             ("ML models", "that survive honest backtests", LIME), ("automations", "that run while you sleep", AMBER),
             ("multi-tenant systems", "that scale safely", VIOLET)]
    rot = "".join(
        f'<text class="sans rot{" r0" if i == 0 else ""}" style="animation-delay:{i*3}s" x="64" y="262" font-size="36" font-weight="700" fill="{TEXT}">'
        f'{"I architect" if i == 4 else "I build"} <tspan fill="{c}">{x(a)}</tspan> <tspan fill="{MUTED}" font-weight="500">{x(b)}</tspan></text>'
        for i, (a, b, c) in enumerate(roles))
    chips = []
    for row, labels in enumerate([[("AI ENGINEER", CORAL), ("VOICE AI · VAPI + TWILIO", AMBER), ("RAG + LLM AGENTS", PINK),
                                   ("ML + QUANT", LIME), ("AUTOMATION", BLUE)],
                                  [("SYSTEMS ARCHITECT", VIOLET), ("MULTI-TENANT SAAS", AMBER), ("CLAUDE + MCP", CORAL),
                                   ("n8n WORKFLOWS", PINK), ("LLM COST OPTIMIZATION", LIME)]]):
        cx = 64
        for label, col in labels:
            c, w = chip(cx, 312 + row * 36, label, col)
            chips.append(c)
            cx += w + 10
    # orb: rings, orbiting dots, equalizer core
    ox, oy = 1000, 240
    bars = "".join(
        f'<rect class="eq" style="animation-delay:{(i*137)%900/1000:.2f}s" x="{ox - 66 + i*12}" y="{oy - 34}" width="7" height="68" rx="3.5" fill="url(#sun)"/>'
        for i, _ in enumerate(range(11)))
    orb = f"""
<circle cx="{ox}" cy="{oy}" r="150" fill="none" stroke="{EDGE}" stroke-width="1"/>
<g class="fx spin" style="transform-origin:{ox}px {oy}px;transform-box:view-box"><circle cx="{ox}" cy="{oy}" r="150" fill="none" stroke="url(#sun)" stroke-width="2.5" stroke-dasharray="90 380" stroke-linecap="round"/>
<circle cx="{ox + 150}" cy="{oy}" r="6" fill="{AMBER}" filter="url(#glow)"/></g>
<g class="rspin" style="transform-origin:{ox}px {oy}px;transform-box:view-box"><circle cx="{ox}" cy="{oy}" r="112" fill="none" stroke="{BLUE}" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="4 10"/>
<circle cx="{ox}" cy="{oy - 112}" r="5" fill="{LIME}" filter="url(#glow)"/><circle cx="{ox - 97}" cy="{oy + 56}" r="4" fill="{PINK}" filter="url(#glow)"/></g>
<circle cx="{ox}" cy="{oy}" r="84" fill="{CARD}" stroke="{EDGE}"/>
<circle class="ring" cx="{ox}" cy="{oy}" r="84" fill="none" stroke="{CORAL}" stroke-width="2"/>
{bars}
<text x="{ox}" y="{oy + 62}" class="mono" font-size="10" fill="{MUTED}" text-anchor="middle">LIVE · ON CALL</text>"""
    body = f"""
<rect x="64" y="52" width="252" height="30" rx="15" fill="{CARD}" stroke="{LIME}" stroke-opacity=".6"/>
<circle class="pulse" cx="84" cy="67" r="5" fill="{LIME}" filter="url(#glow)"/>
<text x="98" y="71.5" class="mono" font-size="11" fill="{LIME}">OPEN TO CONTRACT WORK</text>
<text x="60" y="186" class="sans" font-size="96" font-weight="800" letter-spacing="-3" fill="url(#sun)" filter="url(#glow)">Intikhab Azam</text>
{rot}
{''.join(chips)}
<line x1="64" y1="404" x2="780" y2="404" stroke="{EDGE}"/>
<text x="64" y="434" class="mono" font-size="12" fill="{MUTED}">PYTHON · TYPESCRIPT · PYTORCH · LANGCHAIN · VAPI · TWILIO · FASTAPI · DOCKER · KUBERNETES</text>
<text x="64" y="460" class="mono" font-size="12" fill="{MUTED}">CLAUDE · MCP · N8N · NESTJS · NEXT.JS · PRISMA · POSTGRES · CLOUDFLARE WORKERS</text>
{orb}
<rect class="shine" x="0" y="0" width="120" height="{H}" fill="#fff" opacity=".035" transform="skewX(-20)"/>"""
    return svg(W, H, "Intikhab Azam, AI engineer and systems architect: voice AI agents, RAG chatbots, machine learning and automation. Open to contract work.", body)


# ---------------------------------------------------------------- what I build
def build():
    import random
    W, cw, ch, gap, x0 = 1200, 376, 290, 12, 18
    H = 20 + 2 * ch + gap + 20
    items = [
        ("VOICE AI AGENTS", CORAL, "Vapi + Twilio receptionists and outbound callers wired into CRMs, payments and dialers."),
        ("RAG + LLM AGENTS", PINK, "Chatbots grounded in your documents, with tool calling, memory and evaluation."),
        ("ML + QUANT", LIME, "Forecasting, face recognition and backtests that can't fool themselves."),
        ("AUTOMATION", BLUE, "Lead engines, scraping, enrichment and scheduled pipelines that run unattended."),
        ("SYSTEM ARCHITECTURE", VIOLET, "Multi-tenant SaaS, BFF auth, field-level encryption, queues and CI/CD built to scale."),
        ("AI AGENT WORKFLOWS", AMBER, "Claude, MCP and n8n agents that triage, route and act across Slack, Notion and CRMs."),
    ]
    out = []
    for i, (title, col, desc) in enumerate(items):
        cx, cy = x0 + (i % 3) * (cw + gap), 20 + (i // 3) * (ch + gap)
        ill_x, ill_y = cx + (cw - 240) / 2, cy + 20
        if i == 0:
            ill = "".join(f'<rect class="eq" style="animation-delay:{(j*173)%1000/1000:.2f}s" x="{ill_x + j*20:.1f}" y="{ill_y + 20}" width="10" height="80" rx="5" fill="{col}" opacity="{.45 + (j % 3)*.25:.2f}"/>' for j in range(12))
        elif i == 1:
            docs = "".join(f'<rect x="{ill_x}" y="{ill_y + 10 + j*34}" width="46" height="26" rx="5" fill="{CARD}" stroke="{col}" stroke-opacity=".7"/>'
                           f'<line x1="{ill_x+8}" y1="{ill_y+20+j*34}" x2="{ill_x+36}" y2="{ill_y+20+j*34}" stroke="{MUTED}" stroke-width="2"/>' for j in range(3))
            dots = "".join(f'<circle class="move" style="--dx:118px;animation-delay:{j*.45:.2f}s" cx="{ill_x + 56}" cy="{ill_y + 23 + (j % 3)*34}" r="4" fill="{col}" filter="url(#glow)"/>' for j in range(6))
            bubble = (f'<rect x="{ill_x + 178}" y="{ill_y + 30}" width="58" height="46" rx="12" fill="{col}"/>'
                      f'<path d="M{ill_x+190} {ill_y+76} l-6 12 l16 -12z" fill="{col}"/>'
                      + "".join(f'<circle class="pulse" style="animation-delay:{j*.3}s" cx="{ill_x+194+j*13}" cy="{ill_y+53}" r="3.5" fill="{BG}"/>' for j in range(3)))
            ill = docs + dots + bubble
        elif i == 2:
            rng, v, candles = random.Random(7), 60, []
            for j in range(11):
                o = v
                v += rng.uniform(-14, 16)
                c = v
                hi, lo = max(o, c) + rng.uniform(2, 8), min(o, c) - rng.uniform(2, 8)
                cc = LIME if c >= o else CORAL
                px = ill_x + j * 22
                candles.append(f'<line x1="{px+5}" y1="{ill_y+120-hi:.1f}" x2="{px+5}" y2="{ill_y+120-lo:.1f}" stroke="{cc}" stroke-width="1.5"/>'
                               f'<rect x="{px}" y="{ill_y+120-max(o,c):.1f}" width="10" height="{max(abs(c-o),2):.1f}" fill="{cc}"/>')
            pts = " ".join(f"{ill_x + 5 + j*22:.1f},{ill_y + 50 - j*5 - (j % 2)*6:.1f}" for j in range(11))
            ill = "".join(candles) + f'<polyline pathLength="1" class="draw" points="{pts}" fill="none" stroke="{AMBER}" stroke-width="2" filter="url(#glow)"/>'
        elif i == 3:
            nodes = [(ill_x + 10, ill_y + 60), (ill_x + 90, ill_y + 20), (ill_x + 90, ill_y + 100), (ill_x + 170, ill_y + 60), (ill_x + 230, ill_y + 60)]
            links = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
            ill = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{EDGE}" stroke-width="2"/>' for a, b in links)
            ill += "".join(f'<circle class="move" style="--dx:{nodes[b][0]-nodes[a][0]:.0f}px;animation-delay:{k*.5}s" cx="{nodes[a][0]}" cy="{(nodes[a][1]+nodes[b][1])/2}" r="4" fill="{col}" filter="url(#glow)"/>' for k, (a, b) in enumerate(links))
            ill += "".join(f'<circle cx="{nx}" cy="{ny}" r="{13 if k in (0,4) else 10}" fill="{CARD}" stroke="{col}" stroke-width="2"/>' for k, (nx, ny) in enumerate(nodes))
        elif i == 4:
            boxes = [("CLIENT", 0, 44), ("API", 92, 44), ("QUEUE", 184, 0), ("DB", 184, 44), ("LLM", 184, 88)]
            ill = ""
            for lab, bx, by in boxes[2:]:
                ill += f'<line x1="{ill_x+148}" y1="{ill_y+64}" x2="{ill_x+bx}" y2="{ill_y+by+20}" stroke="{EDGE}" stroke-width="2"/>'
            ill += f'<line x1="{ill_x+56}" y1="{ill_y+64}" x2="{ill_x+92}" y2="{ill_y+64}" stroke="{EDGE}" stroke-width="2"/>'
            ill += "".join(f'<circle class="move" style="--dx:36px;animation-delay:{k*.6:.1f}s" cx="{ill_x+56}" cy="{ill_y+64}" r="4" fill="{col}" filter="url(#glow)"/>' for k in range(3))
            for lab, bx, by in boxes:
                ill += (f'<rect x="{ill_x+bx}" y="{ill_y+by}" width="56" height="40" rx="8" fill="{CARD}" stroke="{col if lab in ("API", "DB") else EDGE}" stroke-width="2"/>'
                        f'<text x="{ill_x+bx+28}" y="{ill_y+by+24}" class="mono" font-size="9" fill="{TEXT}" text-anchor="middle">{lab}</text>')
            ill += f'<rect class="pulse" x="{ill_x+178}" y="{ill_y+40}" width="60" height="48" rx="10" fill="none" stroke="{col}" stroke-dasharray="4 4"/>'
            ill += f'<text x="{ill_x+120}" y="{ill_y+150}" class="mono" font-size="9" fill="{col}" text-anchor="middle">TENANT-SCOPED · ENCRYPTED</text>'
        else:
            steps = [("slack", "SLACK"), ("claude", "CLAUDE"), ("n8n", "n8n"), ("notion", "NOTION")]
            ill = f'<line x1="{ill_x+24}" y1="{ill_y+60}" x2="{ill_x+216}" y2="{ill_y+60}" stroke="{EDGE}" stroke-width="2"/>'
            ill += "".join(f'<circle class="move" style="--dx:190px;animation-delay:{k*.65:.2f}s" cx="{ill_x+24}" cy="{ill_y+60}" r="4" fill="{col}" filter="url(#glow)"/>' for k in range(4))
            for k, (slug, lab) in enumerate(steps):
                nx = ill_x + 24 + k * 64
                ill += (f'<circle cx="{nx}" cy="{ill_y+60}" r="24" fill="{CARD}" stroke="{col if k == 1 else EDGE}" stroke-width="2"/>'
                        f'{logo(slug, nx, ill_y + 60, 22)}'
                        f'<text x="{nx}" y="{ill_y+106}" class="mono" font-size="9" fill="{MUTED}" text-anchor="middle">{lab}</text>')
        text = "".join(f'<text x="{cx + 22}" y="{cy + 234 + j*20}" class="sans" font-size="14" fill="{MUTED}">{x(line)}</text>' for j, line in enumerate(wrap(desc, 46)))
        out.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16" fill="{CARD}" fill-opacity=".85" stroke="{EDGE}"/>'
                   f'<rect x="{cx}" y="{cy}" width="{cw}" height="4" rx="2" fill="{col}"/>'
                   f'{ill}<text x="{cx + 22}" y="{cy + 204}" class="mono" font-size="13" font-weight="700" fill="{col}">0{i+1} · {x(title)}</text>{text}')
    return svg(W, H, "What I build: voice AI agents, RAG and LLM agents, machine learning, automation, system architecture and Claude + n8n agent workflows", "".join(out), blobs=False)


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("edgeproof", "EdgeProof", "CRYPTO BACKTESTING · ML VALIDATION", LIME,
     "Catches the overfitting that makes trading bots look profitable: triple-barrier labels, purged CV and deflated Sharpe, verified by a planted-edge control.",
     [("Python", "python"), ("PyTorch", "pytorch"), ("LightGBM", "lightgbm")]),
    ("vapi-crm", "Vapi Voice Agent CRM", "AI VOICE AGENTS · CALL OPS", CORAL,
     "Call-ops backend for AI voice agents: webhook ingestion, predictive dialer, auto-redial and payment-verified conversions.",
     [("Node.js", "nodedotjs"), ("Twilio", "twilio"), ("Stripe", "stripe")]),
    ("lead-finder", "Lead Finder Engine", "LEAD GENERATION · SCRAPING", AMBER,
     "Self-hosted lead engine: grid search past the Google Places 60-result cap, free OpenStreetMap fallback and resumable runs.",
     [("Python", "python"), ("FastAPI", "fastapi"), ("Streamlit", "streamlit")]),
    ("secureface", "SecureFace", "COMPUTER VISION · ANTI-SPOOFING", PINK,
     "Face recognition that blocks photo and video replay attacks with a head-pose challenge and rPPG pulse detection.",
     [("OpenCV", "opencv"), ("Python", "python"), ("Streamlit", "streamlit")]),
    ("wealth-advisor", "AI Wealth Advisor", "RAG · TOOL-CALLING AGENT", BLUE,
     "Financial assistant with RAG memory that scores portfolio risk (VaR, Sharpe, drawdown) and designs strategies.",
     [("LangChain", "langchain"), ("Gemini", "googlegemini"), ("Flask", "flask")]),
    ("cryptoaion", "CryptoAion", "DEEP LEARNING · PRICE FORECASTING", AMBER,
     "BiLSTM + attention price forecasts on 30m to 24h timeframes, served by FastAPI and streamed live over WebSockets.",
     [("PyTorch", "pytorch"), ("FastAPI", "fastapi"), ("Python", "python")]),
    ("npi-pipeline", "NPI Lead Pipeline", "HEALTHCARE DATA · AUTOMATION", LIME,
     "NPI Registry providers to practice websites to e-mails: resume-safe and scheduled on GitHub Actions with zero paid APIs.",
     [("Python", "python"), ("Actions", "githubactions")]),
    ("k8s-microservices", "K8s Microservices", "DEVOPS · KUBERNETES", BLUE,
     "Flask microservices on Kubernetes with an NGINX gateway, PostgreSQL, a logging service and Prometheus monitoring.",
     [("Kubernetes", "kubernetes"), ("Docker", "docker"), ("NGINX", "nginx")]),
]


def visual(kind, vx, vy, col):
    if kind == "edgeproof":
        fake = " ".join(f"{vx + i*16},{vy + 110 - i*9 - (i%2)*5}" for i in range(11))
        real = " ".join(f"{vx + i*16},{vy + 92 + ((i*7)%5) - 2}" for i in range(11))
        return (f'<polyline pathLength="1" class="draw" points="{fake}" fill="none" stroke="{CORAL}" stroke-width="2" stroke-dasharray="1"/>'
                f'<text x="{vx + 100}" y="{vy + 18}" class="mono" font-size="9" fill="{CORAL}">BACKTEST</text>'
                f'<polyline points="{real}" fill="none" stroke="{col}" stroke-width="2.5" filter="url(#glow)"/>'
                f'<text x="{vx + 100}" y="{vy + 128}" class="mono" font-size="9" fill="{col}">REALITY</text>')
    if kind == "vapi-crm":
        cx, cy = vx + 80, vy + 60
        return (f'<circle class="ring" cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<circle class="ring" style="animation-delay:1.2s" cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<circle cx="{cx}" cy="{cy}" r="28" fill="{col}"/>'
                f'<path transform="translate({cx-12} {cy-12})" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" fill="{BG}"/>')
    if kind == "lead-finder":
        grid = "".join(f'<line x1="{vx + i*30}" y1="{vy}" x2="{vx + i*30}" y2="{vy+120}" stroke="{EDGE}"/>' for i in range(6))
        grid += "".join(f'<line x1="{vx}" y1="{vy + i*30}" x2="{vx+150}" y2="{vy + i*30}" stroke="{EDGE}"/>' for i in range(5))
        pins = "".join(f'<g class="drop" style="animation-delay:{i*.45:.2f}s"><path d="M{px} {py} c-7 -9 -9 -12 -9 -16 a9 9 0 0 1 18 0 c0 4 -2 7 -9 16z" fill="{c}"/><circle cx="{px}" cy="{py-16}" r="3" fill="{BG}"/></g>'
                       for i, (px, py, c) in enumerate([(vx+30, vy+50, col), (vx+95, vy+40, CORAL), (vx+65, vy+95, PINK), (vx+130, vy+85, col), (vx+20, vy+112, LIME)]))
        return grid + pins
    if kind == "secureface":
        cx, cy = vx + 75, vy + 58
        beat = f"M{vx} {vy+120} h40 l8 -18 l8 30 l8 -22 l6 10 h80"
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="36" ry="46" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="6 5"/>'
                f'<circle cx="{cx-13}" cy="{cy-8}" r="3" fill="{col}"/><circle cx="{cx+13}" cy="{cy-8}" r="3" fill="{col}"/>'
                f'<path d="M{cx-12} {cy+20} q12 9 24 0" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<rect class="scan" style="--dy:84px" x="{cx-46}" y="{cy-46}" width="92" height="3" fill="{col}" filter="url(#glow)"/>'
                f'<path pathLength="1" class="draw" d="{beat}" fill="none" stroke="{CORAL}" stroke-width="2" stroke-dasharray="1"/>')
    if kind == "wealth-advisor":
        cx, cy, r = vx + 60, vy + 62, 40
        segs, start = [], 0
        for frac, c in [(.42, col), (.26, AMBER), (.18, PINK), (.14, LIME)]:
            segs.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="14" pathLength="100" stroke-dasharray="{frac*100-1.5:.1f} 100" stroke-dashoffset="{-start*100:.1f}" transform="rotate(-90 {cx} {cy})"/>')
            start += frac
        return (f'<g class="spin" style="transform-origin:{cx}px {cy}px;transform-box:view-box">{"".join(segs)}</g>'
                f'<rect x="{vx+100}" y="{vy+4}" width="62" height="34" rx="10" fill="{CARD}" stroke="{col}"/>'
                f'<text x="{vx+131}" y="{vy+26}" class="mono" font-size="10" fill="{col}" text-anchor="middle">VaR</text>'
                f'<rect x="{vx+100}" y="{vy+86}" width="62" height="34" rx="10" fill="{CARD}" stroke="{AMBER}"/>'
                f'<text x="{vx+131}" y="{vy+108}" class="mono" font-size="10" fill="{AMBER}" text-anchor="middle">SHARPE</text>')
    if kind == "cryptoaion":
        import random
        rng, v, out = random.Random(11), 60, []
        for j in range(8):
            o = v; v += rng.uniform(-12, 14); c = v
            cc = LIME if c >= o else CORAL
            px = vx + j * 13
            out.append(f'<rect x="{px}" y="{vy+120-max(o,c)}" width="8" height="{max(abs(c-o),2):.1f}" fill="{cc}"/>')
        last = vy + 120 - v
        fc = f"M{vx+100} {last:.1f} C{vx+120} {last-10:.1f} {vx+140} {last-30:.1f} {vx+160} {last-40:.1f}"
        return ("".join(out) + f'<path d="{fc}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="4 5" filter="url(#glow)"/>'
                f'<circle class="pulse" cx="{vx+160}" cy="{last-40:.1f}" r="5" fill="{col}" filter="url(#glow)"/>'
                f'<text x="{vx+104}" y="{vy+128}" class="mono" font-size="9" fill="{col}">BiLSTM</text>')
    if kind == "npi-pipeline":
        nodes = [vx + 10, vx + 80, vx + 150]
        out = f'<line x1="{nodes[0]}" y1="{vy+60}" x2="{nodes[2]}" y2="{vy+60}" stroke="{EDGE}" stroke-width="2"/>'
        out += "".join(f'<rect class="move" style="--dx:140px;animation-delay:{k*.65:.2f}s" x="{nodes[0]-4}" y="{vy+56}" width="8" height="8" rx="2" fill="{col}" filter="url(#glow)"/>' for k in range(4))
        for i, (n, lab) in enumerate(zip(nodes, ["NPI", "WEB", "@"])):
            out += (f'<circle cx="{n}" cy="{vy+60}" r="18" fill="{CARD}" stroke="{col}" stroke-width="2"/>'
                    f'<text x="{n}" y="{vy+64}" class="mono" font-size="10" fill="{TEXT}" text-anchor="middle">{x(lab)}</text>')
        return out
    # k8s pods
    out = []
    for i, (hx, hy) in enumerate([(0, 0), (1, 0), (2, 0), (.5, 1), (1.5, 1), (1, 2)]):
        cx, cy = vx + 40 + hx * 44, vy + 22 + hy * 38
        pts = " ".join(f"{cx + 20*__import__('math').cos(__import__('math').radians(60*k+30)):.1f},{cy + 20*__import__('math').sin(__import__('math').radians(60*k+30)):.1f}" for k in range(6))
        out.append(f'<polygon class="pulse" style="animation-delay:{i*.35:.2f}s" points="{pts}" fill="{CARD}" stroke="{col}" stroke-width="2"/>')
    return "".join(out)


def card(p):
    slug, title, tag, col, desc, tech = p
    W, H = 590, 300
    lines = "".join(f'<text x="30" y="{176 + j*21}" class="sans" font-size="15" fill="{MUTED}">{x(t)}</text>' for j, t in enumerate(wrap(desc, 64)[:3]))
    chips, cx = [], 30
    for label, s in tech:
        c, w = chip(cx, 246, label, TEXT, s)
        chips.append(c)
        cx += w + 8
    n = PROJECTS.index(p) + 1
    body = (f'<rect x="0" y="0" width="6" height="{H}" fill="{col}"/>'
            f'<text x="30" y="46" class="mono" font-size="12" fill="{col}">{n:02d} · {x(tag)}</text>'
            f'<text x="28" y="92" class="sans" font-size="34" font-weight="800" fill="{TEXT}">{x(title)}</text>'
            f'<rect x="30" y="112" width="60" height="4" rx="2" fill="url(#sun)"/>'
            f'{visual(slug, 400, 20, col)}{lines}{"".join(chips)}'
            f'<text x="560" y="272" class="mono" font-size="12" fill="{col}" text-anchor="end">VIEW REPO →</text>')
    return svg(W, H, f"{title}: {desc}", body)


# ---------------------------------------------------------------- stack
STACK = [
    ("AI + ML", CORAL, ["python", "pytorch", "scikitlearn", "numpy", "pandas", "jupyter", "langchain", "openai", "googlegemini", "huggingface", "opencv"]),
    ("AGENTS + LLMs", VIOLET, ["claude", "anthropic", "mcp", "openrouter", "elevenlabs", "deepgram", "retell", "notebooklm", "lightgbm", "xgboost"]),
    ("VOICE + BACKEND", AMBER, ["twilio", "vapi", "fastapi", "flask", "nodedotjs", "express", "stripe", "postgresql", "mysql", "sqlite", "mongodb"]),
    ("SYSTEM ARCHITECTURE", LIME, ["nestjs", "nextdotjs", "prisma", "drizzle", "neon", "betterauth", "minio", "cloudflareworkers", "pnpm"]),
    ("AUTOMATION + QA", CORAL, ["n8n", "slack", "notion", "resend", "playwright", "drissionpage", "jest"]),
    ("FRONTEND", PINK, ["typescript", "javascript", "react", "vite", "tailwindcss", "astro", "streamlit", "cplusplus"]),
    ("DEVOPS + CLOUD", BLUE, ["docker", "kubernetes", "nginx", "prometheus", "githubactions", "linux", "gnubash", "cloudflare", "vercel"]),
]


def stack():
    W, rowh = 1200, 104
    H = 40 + rowh * len(STACK)
    out = []
    for r, (label, col, slugs) in enumerate(STACK):
        y = 28 + r * rowh
        out.append(f'<text x="32" y="{y + 44}" class="mono" font-size="12" font-weight="700" fill="{col}">0{r+1}</text>'
                   f'<text x="32" y="{y + 62}" class="mono" font-size="11" fill="{TEXT}">{x(label)}</text>')
        for i, s in enumerate(slugs):
            tx = 190 + i * 90
            name = ICONS[s]["title"] if s in ICONS else {"vapi": "Vapi", "mcp": "MCP", "openrouter": "OpenRouter", "retell": "Retell AI",
                                                          "notebooklm": "NotebookLM", "lightgbm": "LightGBM", "xgboost": "XGBoost", "neon": "Neon",
                                                          "betterauth": "better-auth", "playwright": "Playwright", "drissionpage": "DrissionPage"}.get(s, s)
            name = {"Google Gemini": "Gemini", "GNU Bash": "Bash", "GitHub Actions": "Actions", "scikit-learn": "sklearn", "Hugging Face": "HF", "Cloudflare Workers": "CF Workers"}.get(name, name)
            out.append(f'<g class="enter" style="animation-delay:{r*.25 + i*.06:.2f}s">'
                       f'<rect x="{tx}" y="{y + 6}" width="80" height="84" rx="14" fill="{CARD}" stroke="{EDGE}"/>'
                       f'{logo(s, tx + 40, y + 38, 30)}'
                       f'<text x="{tx + 40}" y="{y + 78}" class="sans" font-size="11" fill="{MUTED}" text-anchor="middle">{x(name)}</text></g>')
    return svg(W, H, "Tech stack: " + ", ".join(ICONS[s]["title"] if s in ICONS else s for _, _, ss in STACK for s in ss), "".join(out), blobs=False)


# ---------------------------------------------------------------- architecture
def architecture():
    W, H = 1200, 500
    cols = [
        ("01 · CLIENTS", CORAL, ["Web portals", "Phone · voice AI", "Slack · e-mail", "Mobile + partner APIs"]),
        ("02 · EDGE", AMBER, ["Cloudflare Workers", "BFF · httpOnly auth", "Webhook ingestion"]),
        ("03 · CORE SERVICES", PINK, ["NestJS · FastAPI", "Job queue + workers", "n8n workflows"]),
        ("04 · INTELLIGENCE", VIOLET, ["LLM router", "Claude · GPT-4o", "Small models first", "RAG · vector memory"]),
        ("05 · DATA + OPS", LIME, ["Postgres · tenant RLS", "Encrypted PII fields", "Object storage", "Prometheus · CI/CD"]),
    ]
    bw, bh, x0, step = 196, 50, 36, 232
    out = [f'<text x="36" y="46" class="mono" font-size="12" font-weight="700" fill="{AMBER}">● REFERENCE ARCHITECTURE</text>'
           f'<text x="1164" y="46" class="mono" font-size="11" fill="{MUTED}" text-anchor="end">HOW I DESIGN PRODUCTION AI SYSTEMS</text>']
    centers = []
    for c, (head, col, boxes) in enumerate(cols):
        bx = x0 + c * step
        out.append(f'<text x="{bx}" y="96" class="mono" font-size="12" font-weight="700" fill="{col}">{x(head)}</text>'
                   f'<rect x="{bx}" y="108" width="{bw}" height="3" rx="1.5" fill="{col}"/>')
        n = len(boxes)
        top = 140 + (4 - n) * (bh + 22) / 2
        ys = []
        for j, lab in enumerate(boxes):
            by = top + j * (bh + 22)
            ys.append(by + bh / 2)
            out.append(f'<rect x="{bx}" y="{by:.0f}" width="{bw}" height="{bh}" rx="12" fill="{CARD}" stroke="{col}" stroke-opacity=".55"/>'
                       f'<circle cx="{bx + 20}" cy="{by + bh/2:.0f}" r="4" fill="{col}"/>'
                       f'<text x="{bx + 34}" y="{by + bh/2 + 5:.0f}" class="sans" font-size="14" font-weight="600" fill="{TEXT}">{x(lab)}</text>')
        centers.append((bx, ys, col))
    links = []
    for c in range(len(centers) - 1):
        ax, ays, col = centers[c]
        bx, bys, _ = centers[c + 1]
        for k, ya in enumerate(ays):
            yb = bys[min(k, len(bys) - 1)]
            x1, x2 = ax + bw, bx
            links.append(f'<path d="M{x1} {ya:.0f} C{x1 + 18} {ya:.0f} {x2 - 18} {yb:.0f} {x2} {yb:.0f}" fill="none" stroke="{EDGE}" stroke-width="1.5"/>')
            links.append(f'<circle class="move" style="--dx:{x2 - x1}px;animation-delay:{(c*3 + k)*.35:.2f}s" cx="{x1}" cy="{(ya + yb)/2:.0f}" r="3.5" fill="{col}" filter="url(#glow)"/>')
    band = (f'<rect x="36" y="420" width="1128" height="56" rx="14" fill="{CARD}" stroke="{EDGE}"/>'
            f'<text x="60" y="454" class="mono" font-size="12" fill="{MUTED}"><tspan fill="{VIOLET}">CROSS-CUTTING</tspan>   '
            f'MULTI-TENANCY · IDEMPOTENCY + RETRIES · KEY ROTATION · AUDIT TRAILS · COST BUDGETS · E2E-GATED DEPLOYS</text>')
    return svg(W, H, "Reference architecture for production AI systems: clients, edge, core services, LLM routing and intelligence, multi-tenant data and ops", "".join(links + out) + band, blobs=False)


# ---------------------------------------------------------------- call to action
def cta():
    W, H = 1200, 190
    body = f"""
<text x="56" y="80" class="sans" font-size="33" font-weight="800" fill="{TEXT}">Got an AI system that's <tspan fill="url(#sun)">slow, expensive</tspan> or unreliable?</text>
<text x="58" y="122" class="sans" font-size="17" fill="{MUTED}">Voice agents · RAG chatbots · LLM cost optimization · ML validation · automation</text>
<rect x="56" y="140" width="300" height="34" rx="17" fill="url(#sun)"/>
<text x="206" y="162" class="mono" font-size="12" font-weight="700" fill="{BG}" text-anchor="middle">OPEN TO CONTRACT WORK →</text>
<g transform="translate(1100 95)"><circle class="ring" r="44" fill="none" stroke="{LIME}" stroke-width="2"/><circle class="ring" style="animation-delay:1.2s" r="44" fill="none" stroke="{LIME}" stroke-width="2"/><circle r="30" fill="{LIME}" filter="url(#glow)"/>
<text y="5" class="mono" font-size="11" font-weight="700" fill="{BG}" text-anchor="middle">HIRE</text></g>
<rect class="shine" x="0" y="0" width="120" height="{H}" fill="#fff" opacity=".04" transform="skewX(-20)"/>"""
    return svg(W, H, "Open to contract work: voice agents, RAG chatbots, LLM cost optimization, ML validation and automation", body)


if __name__ == "__main__":
    os.makedirs("assets/projects", exist_ok=True)
    files = {"assets/hero.svg": hero(), "assets/build.svg": build(), "assets/stack.svg": stack(), "assets/architecture.svg": architecture(), "assets/cta.svg": cta()}
    for p in PROJECTS:
        files[f"assets/projects/{p[0]}.svg"] = card(p)
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    print(len(files), "files")
