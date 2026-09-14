"""Render the static profile art (hero, stack sheet, footer) into assets/, one file per theme.

Run from the repo root:  python .github/scripts/static_art.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import THEMES, corners, frame, grid, x  # noqa: E402

OUT = "assets"


def voice_path(x0, y0, w, amp):
    """Speech-like bursts: a carrier under gaussian envelopes."""
    bursts = [(0.12, 0.05, 0.9), (0.30, 0.07, 1.0), (0.47, 0.03, 0.55), (0.63, 0.08, 0.95), (0.84, 0.05, 0.7)]
    rng = random.Random(49)
    pts = []
    for i in range(0, int(w) + 1, 2):
        u = i / w
        env = sum(a * math.exp(-((u - c) ** 2) / (2 * s * s)) for c, s, a in bursts)
        y = env * amp * math.sin(i * 0.55 + math.sin(i * 0.05) * 3) + rng.uniform(-1.2, 1.2)
        pts.append(f"{x0 + i:.1f} {y0 - y:.1f}")
    return "M" + " L".join(pts)


def price_path(x0, y0, w, amp):
    rng = random.Random(2026)
    v, raw = 0.0, []
    for _ in range(0, int(w) + 1, 4):
        v += rng.gauss(0.03, 1.0)
        raw.append(v)
    lo, hi = min(raw), max(raw)
    pts = [f"{x0 + k * 4:.1f} {y0 + amp - (r - lo) / (hi - lo) * 2 * amp:.1f}" for k, r in enumerate(raw)]
    return "M" + " L".join(pts)


def hero(t):
    W, H = 1200, 420
    sx, sy, sw, sh = 780, 92, 364, 250
    tags = ["VOICE AI AGENTS", "RAG + LLM APPS", "ML + QUANT RESEARCH", "AUTOMATION"]
    tag_spans = '<tspan class="sig">  /  </tspan>'.join(x(s) for s in tags)
    body = f"""
{grid(t, 'hg')}<rect width="{W}" height="{H}" rx="14" fill="url(#hg)"/>
{corners(t, W, H)}
<text x="56" y="48" class="mono" font-size="12">INTIKHAB AZAM / FIELD NOTES</text>
<text x="1144" y="48" class="mono" font-size="12" text-anchor="end"><tspan class="sig blink">●</tspan> AVAILABLE FOR CONTRACT WORK</text>
<line x1="56" y1="64" x2="1144" y2="64" stroke="{t['rule']}"/>
<text x="54" y="172" class="serif" font-size="80" letter-spacing="-1.5">Intikhab Azam</text>
<text x="58" y="224" class="serif" font-size="28" font-style="italic" fill="{t['muted']}" style="fill:{t['muted']}">AI systems that answer phones,</text>
<text x="58" y="260" class="serif" font-size="28" font-style="italic" style="fill:{t['muted']}">read markets and run the back office.</text>
<text x="58" y="318" class="mono" font-size="13" style="fill:{t['text']}">{tag_spans}</text>
<g>
  <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="10" fill="{t['panel']}" stroke="{t['rule']}"/>
  {grid(t, 'sg', 18, 0.7)}<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="10" fill="url(#sg)"/>
  <line x1="{sx}" y1="{sy + sh/2}" x2="{sx + sw}" y2="{sy + sh/2}" stroke="{t['rule']}"/>
  <text x="{sx + 14}" y="{sy + 22}" class="mono" font-size="10" style="fill:{t['signal']}">CH1 · VOICE</text>
  <text x="{sx + 14}" y="{sy + sh/2 + 20}" class="mono" font-size="10" style="fill:{t['sage']}">CH2 · PRICE</text>
  <text x="{sx + sw - 14}" y="{sy + sh - 12}" class="mono" font-size="10" text-anchor="end">SIGNAL ÷ NOISE</text>
  <path d="{voice_path(sx + 12, sy + 70, sw - 24, 42)}" pathLength="1" class="draw" fill="none" stroke="{t['signal']}" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="{price_path(sx + 12, sy + 186, sw - 24, 36)}" pathLength="1" class="draw draw2" fill="none" stroke="{t['sage']}" stroke-width="1.6" stroke-linejoin="round"/>
  <line x1="{sx}" y1="{sy + 6}" x2="{sx}" y2="{sy + sh - 6}" class="scan" stroke="{t['text']}" stroke-width="1" opacity="0.35"/>
</g>
<line x1="56" y1="364" x2="1144" y2="364" stroke="{t['rule']}"/>
<text x="56" y="392" class="mono" font-size="11">PYTHON · TYPESCRIPT · PYTORCH · LANGCHAIN · VAPI · TWILIO · FASTAPI · KUBERNETES</text>
<text x="1144" y="392" class="mono" font-size="11" text-anchor="end">Nº 49</text>
"""
    return frame(t, W, H, "Intikhab Azam: AI engineer for voice AI agents, RAG, machine learning and automation", body)


STACK = [
    ("01", "AI + ML", ["Python", "PyTorch", "LightGBM · XGBoost", "scikit-learn", "LangChain", "ChromaDB", "OpenAI · Gemini"]),
    ("02", "VOICE + BACKEND", ["Vapi", "Twilio", "FastAPI · Flask", "Node.js · Express", "PostgreSQL · MySQL", "SQLite · MongoDB", "Stripe"]),
    ("03", "FRONTEND", ["React", "TypeScript", "Vite", "Tailwind CSS", "Astro", "Streamlit"]),
    ("04", "DEVOPS + CLOUD", ["Docker", "Kubernetes", "NGINX · Prometheus", "GitHub Actions", "Cloudflare · Vercel", "Linux · Bash"]),
]


def stack(t):
    W, H = 1200, 330
    cols = []
    for i, (n, head, items) in enumerate(STACK):
        cx = 56 + i * 276
        rows = "".join(f'<text x="{cx}" y="{112 + j * 30}" class="serif" font-size="18">{x(it)}</text>' for j, it in enumerate(items))
        cols.append(f'<text x="{cx}" y="64" class="mono" font-size="12"><tspan class="sig">{n}</tspan>  {x(head)}</text>'
                    f'<line x1="{cx}" y1="80" x2="{cx + 236}" y2="80" stroke="{t["rule"]}"/>{rows}')
    body = f"{grid(t, 'kg')}<rect width='{W}' height='{H}' rx='14' fill='url(#kg)'/>{corners(t, W, H)}{''.join(cols)}"
    return frame(t, W, H, "Tech stack: AI and ML, voice and backend, frontend, DevOps and cloud", body)


def footer(t):
    W, H = 1200, 90
    body = f"""<line x1="56" y1="45" x2="470" y2="45" stroke="{t['rule']}"/>
<text x="600" y="50" class="mono" font-size="12" text-anchor="middle"><tspan class="sig blink">●</tspan>  END OF TRANSMISSION</text>
<line x1="730" y1="45" x2="1144" y2="45" stroke="{t['rule']}"/>"""
    return frame(t, W, H, "End of profile", body)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("hero", hero), ("stack", stack), ("footer", footer)]:
        for mode, t in THEMES.items():
            with open(f"{OUT}/{name}-{mode}.svg", "w", encoding="utf-8") as f:
                f.write(fn(t))
    print("wrote", sorted(os.listdir(OUT)))
