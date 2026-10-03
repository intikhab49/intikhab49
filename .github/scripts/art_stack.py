"""Tech stack as painted number plates, grouped by category."""
import json
import os

from ta_core import (BLUE, DGREEN, DRED, GOLD, GREEN, INK, NIGHT, ORANGE, PINK, PURPLE, RED, SAFFRON, TEAL, WHITE, Doc,
                     n)
from ta_fonts import F
from ta_motifs import blossom, dots, rose, tape_defs

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))

STACK = [
    ("AI + AGENTS", PINK, [("Claude", "claude"), ("Claude Code", "claude"), ("MCP", "modelcontextprotocol"), ("Anthropic", "anthropic"),
                           ("OpenAI", "openai"), ("Codex", "openai"), ("Gemini", "googlegemini"), ("DeepSeek", "deepseek"),
                           ("OpenRouter", "openrouter"), ("LangChain", "langchain"), ("Hugging Face", "huggingface"), ("n8n", "n8n"),
                           ("NotebookLM", None)]),
    ("VOICE AI", ORANGE, [("Vapi", None), ("Twilio", "twilio"), ("ElevenLabs", "elevenlabs"), ("Deepgram", "deepgram"), ("Retell AI", None)]),
    ("ML + DATA", BLUE, [("Python", "python"), ("PyTorch", "pytorch"), ("scikit-learn", "scikitlearn"), ("LightGBM", None), ("XGBoost", None),
                         ("ONNX", "onnx"), ("NumPy", "numpy"), ("pandas", "pandas"), ("Jupyter", "jupyter"), ("OpenCV", "opencv"),
                         ("Google Colab", "googlecolab")]),
    ("BACKEND", GREEN, [("Node.js", "nodedotjs"), ("NestJS", "nestjs"), ("FastAPI", "fastapi"), ("Flask", "flask"), ("Express", "express"),
                        ("Prisma", "prisma"), ("Drizzle", "drizzle"), ("PostgreSQL", "postgresql"), ("Neon", "neon"), ("MySQL", "mysql"),
                        ("SQLite", "sqlite"), ("MongoDB", "mongodb"), ("Stripe", "stripe"), ("Resend", "resend")]),
    ("WEB", TEAL, [("TypeScript", "typescript"), ("JavaScript", "javascript"), ("React", "react"), ("Next.js", "nextdotjs"), ("Vite", "vite"),
                   ("Tailwind CSS", "tailwindcss"), ("Astro", "astro"), ("Streamlit", "streamlit"), ("better-auth", "betterauth"), ("C++", "cplusplus")]),
    ("INFRA + DEVOPS", PURPLE, [("Docker", "docker"), ("Kubernetes", "kubernetes"), ("NGINX", "nginx"), ("Prometheus", "prometheus"),
                                ("GitHub Actions", "githubactions"), ("GHCR", "github"), ("Cloudflare", "cloudflare"),
                                ("CF Workers", "cloudflareworkers"), ("Vercel", "vercel"), ("MinIO", "minio"), ("Linux", "linux"),
                                ("Bash", "gnubash"), ("pnpm", "pnpm")]),
    ("TESTING + TOOLS", RED, [("Playwright", "playwright"), ("Jest", "jest"), ("DrissionPage", None), ("Slack", "slack"), ("Notion", "notion")]),
]

PER_ROW = 7
LABEL_W = 176
PW, PH, GAP, VGAP = 142, 44, 6, 9
X0 = (1280 - (176 + 8 + 7 * (142 + 6) - 6)) // 2 - 7


def lum(hexc):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def names():
    return [t for _, _, items in STACK for t, _ in items]


def build():
    rows = sum((len(items) + PER_ROW - 1) // PER_ROW for _, _, items in STACK)
    H = 40 + rows * (PH + VGAP) + (len(STACK) - 1) * 10 + 34
    W = 1280
    d = Doc(W, H, "Tech stack", "Tech stack: " + ", ".join(names()))
    tape = tape_defs(d, 14)
    d.add(f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="24" fill="{INK}"/>'
          f'<rect x="9" y="9" width="{W - 18}" height="{H - 18}" rx="20" fill="url(#{tape})"/>'
          f'<rect x="23" y="23" width="{W - 46}" height="{H - 46}" rx="12" fill="{INK}"/>'
          f'<rect x="26" y="26" width="{W - 52}" height="{H - 52}" rx="10" fill="{NIGHT}"/>')
    y = 40
    sym = {}
    for cat, col, items in STACK:
        nrows = (len(items) + PER_ROW - 1) // PER_ROW
        bh = nrows * PH + (nrows - 1) * VGAP
        # category label
        lx = X0 + 14
        d.add(f'<rect x="{lx}" y="{y}" width="{LABEL_W - 14}" height="{bh}" rx="10" fill="{col}" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="{lx + 5}" y="{y + 5}" width="{LABEL_W - 24}" height="{bh - 10}" rx="7" fill="none" stroke="#fff" stroke-width="1.5" opacity=".7"/>')
        size = 23
        while F("tekob").width(cat, size, 0.03) > LABEL_W - 40:
            size -= 1
        d.painted(F("tekob"), cat, lx + (LABEL_W - 14) / 2, y + bh / 2 + size * 0.33, size, WHITE, ow=2.6, shadow=(1.5, 2), ls=0.03)
        for i, (title, slug) in enumerate(items):
            r, c = divmod(i, PER_ROW)
            px = X0 + LABEL_W + 8 + c * (PW + GAP)
            py = y + r * (PH + VGAP)
            d.add(f'<rect x="{px}" y="{py}" width="{PW}" height="{PH}" rx="8" fill="#fff6dc" stroke="{INK}" stroke-width="2.5"/>'
                  f'<rect x="{px + 3}" y="{py + 3}" width="7" height="{PH - 6}" rx="3" fill="{col}"/>')
            ix, iy = px + 16, py + (PH - 24) / 2
            if slug and slug in ICONS:
                ic = ICONS[slug]
                fill = ic["hex"] if ic["hex"].startswith("#") else "#" + ic["hex"]
                if lum(fill) > 0.75:
                    fill = INK
                if slug not in sym:
                    sym[slug] = f"ic{len(sym)}"
                    d.define(f'<path id="{sym[slug]}" d="{ic["d"]}"/>')
                d.add(f'<use href="#{sym[slug]}" transform="translate({n(ix)} {n(iy)})" fill="{fill}"/>')
            else:
                mono = "".join(w[0] for w in title.split()[:2]).upper()
                d.add(f'<circle cx="{n(ix + 12)}" cy="{n(iy + 12)}" r="12.5" fill="{col}" stroke="{INK}" stroke-width="2"/>')
                d.text(F("tekob"), mono, ix + 12, iy + 19, 17, fill=WHITE, anchor="middle")
            fs = 20
            while F("tekob").width(title, fs, 0.02) > PW - 52:
                fs -= 0.5
            d.text(F("tekob"), title, px + 46, py + PH / 2 + fs * 0.33, fs, fill=INK, ls=0.02)
        y += bh + VGAP + 10
    return d


if __name__ == "__main__":
    import sys
    print(build().save(sys.argv[1] if len(sys.argv) > 1 else "../out/stack.svg"))
