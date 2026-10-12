"""Inside pages: the services directory, the classifieds and the advertisement."""
import random

import press as P
import type as T

GREY = "#5b564d"

SERVICES = [
    ("AI voice agents", "Vapi · Twilio · CRMs · payments · SMS",
     "Receptionists and outbound callers that answer real phone calls."),
    ("RAG and LLM agents", "tool calling · memory · search",
     "Knowledge-base chatbots, judged by cost per correct answer."),
    ("LLM evals and research", "calibration · benchmarks · backtests",
     "Measurements that report the losing numbers too."),
    ("Multi-tenant SaaS architecture", "Postgres RLS · BFF auth · encryption",
     "Field-level encryption, event-driven jobs, cross-tenant tests."),
    ("Agentic coding", "Claude Code · Codex · DeepSeek",
     "Agents working in parallel behind spec files, a claims board and test gates."),
    ("Automation and data pipelines", "n8n · Cloudflare Workers",
     "Lead generation, scraping and enrichment."),
    ("Developer tools and CI checks", "PyPI · npm · GitHub Actions · MCP",
     "For Microsoft gov clouds, Make.com, Postgres images and AI-written code."),
]

STACK = [
    ("AI & LLMs", "Claude, Claude Code, MCP, OpenAI, Codex, Gemini, DeepSeek, OpenRouter, LangChain, Hugging Face, "
     "NotebookLM."),
    ("Voice", "Vapi, Twilio, ElevenLabs, Deepgram, Retell AI. Phone agents that book, qualify and take payments."),
    ("Machine learning", "PyTorch, scikit-learn, LightGBM, XGBoost, ONNX, NumPy, pandas, OpenCV, Jupyter, Colab."),
    ("Backend", "Python, FastAPI, Flask, Node.js, NestJS, Express, Prisma, Drizzle, PostgreSQL, Neon, MySQL, SQLite, "
     "MongoDB, Stripe, Resend."),
    ("Frontend", "TypeScript, JavaScript, React, Next.js, Vite, Tailwind CSS, Astro, Streamlit, better-auth."),
    ("Infra & automation", "Docker, Kubernetes, NGINX, Prometheus, GitHub Actions, GHCR, Cloudflare Workers, Vercel, "
     "MinIO, Linux, Bash, n8n, Playwright, Jest."),
]


def marker_ring(cx, cy, rx, ry, period=12.0, delay=0.0, seed=1):
    """A red marker ring drawn by hand around something. At rest it is drawn."""
    rng = random.Random(seed)
    pts = []
    n = 46
    for i in range(n + 6):                                  # overshoot past the start, like a real pen
        a = -2.4 + i / n * 6.283
        wob = 1 + rng.uniform(-0.035, 0.035)
        pts.append((cx + rx * wob * __import__("math").cos(a), cy + ry * wob * __import__("math").sin(a)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    length = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5 for i in range(len(pts) - 1))
    k = P._uid("ring")
    css = (f"@keyframes {k}{{0%,100%{{stroke-dashoffset:0}}2%{{stroke-dashoffset:{length:.0f}}}"
           f"18%{{stroke-dashoffset:0}}}}.{k}{{stroke-dasharray:{length:.0f};animation:{k} {period}s ease-in-out "
           f"{delay}s infinite}}")
    return (f'<style>{css}</style><path class="{k}" d="{d}" fill="none" stroke="{P.RED}" stroke-width="3.2" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity=".85" filter="url(#rough)"/>')


def services(paper_uri):
    W, H = 1280, 636
    p = P.open_page(W, H, "Services directory: what I build", "A newspaper services directory listing what Intikhab "
                    "Azam builds: " + "; ".join(f"{a} ({b})" for a, b, _ in SERVICES) + ".", paper_uri)
    M = 52
    p.append('<g filter="url(#ink)">')
    p.append(P.rule(M, W - M, 40, 3) + P.rule(M, W - M, 46, 1))
    p.append(P.text("Services Directory", "mast", 52, W / 2, 98, P.INK, "middle"))
    p.append(P.text("WHAT I BUILD · CONTRACT AND FREELANCE", "body-bold", 14, W / 2, 124, P.INK, "middle"))
    p.append(P.rule(M, W - M, 138, 1) + P.rule(M, W - M, 142, 3))
    y = 190
    rows = []
    for name, tools, line in SERVICES:
        nw = T.width(name, "head-bold", 25)
        tw = T.width(tools, "body", 19)
        p.append(P.text(name, "head-bold", 25, M, y))
        p.append(P.text(tools, "body", 19, W - M, y, P.INK, "end"))
        dots_x0, dots_x1 = M + nw + 14, W - M - tw - 14
        dots = int((dots_x1 - dots_x0) / 9)
        p.append("".join(f'<circle cx="{dots_x0 + i * 9:.1f}" cy="{y - 4}" r="1.3" fill="{P.INK}" opacity=".7"/>'
                         for i in range(max(0, dots))))
        p.append(P.text(line, "body", 16.5, M, y + 24, GREY))
        rows.append((M - 3, y - 22, nw + 6, 30))
        y += 64
    p.append("</g>")
    for i, r in enumerate(rows):
        p.append(P.highlighter(*r, period=16, delay=0.6 + i * 1.6))
    return p


def classifieds(paper_uri):
    W, H = 1280, 520
    p = P.open_page(W, H, "Classifieds: the tools of the trade", "A newspaper classifieds page listing the tech stack. "
                    + " ".join(f"{a}: {b}" for a, b in STACK), paper_uri)
    M = 44
    p.append('<g filter="url(#ink)">')
    p.append(P.rule(M, W - M, 40, 3) + P.rule(M, W - M, 46, 1))
    p.append(P.text("Classifieds", "mast", 52, M, 98))
    p.append(P.text("TOOLS OF THE TRADE · ALL IN DAILY USE", "body-bold", 14, W - M, 92, P.INK, "end"))
    p.append(P.rule(M, W - M, 112, 1))
    cols, gap = 3, 26
    cw = (W - 2 * M - (cols - 1) * gap) / cols
    boxes = []
    wrapped = [P.wrap(items, "body", 17.5, cw - 28) for _, items in STACK]
    row_h = [64 + max(len(w) for w in wrapped[r * cols:(r + 1) * cols]) * 24 for r in range(2)]
    for i, (head, items) in enumerate(STACK):
        c, r = i % cols, i // cols
        x = M + c * (cw + gap)
        y = 140 + sum(row_h[:r]) + r * 34
        lines = wrapped[i]
        h = row_h[r]
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{h}" fill="none" stroke="{P.INK}" stroke-width="1.2"/>')
        p.append(P.text(head.upper(), "head-bold", 21, x + 14, y + 34))
        p.append(P.rule(x + 14, x + cw - 14, y + 46, 0.8))
        for j, line in enumerate(lines):
            p.append(P.text(line, "body", 17.5, x + 14, y + 72 + j * 24))
        boxes.append((x + cw / 2, y + h / 2, cw / 2 + 16, h / 2 + 14))
    p.append("</g>")
    for i in (0, 4):
        cx, cy, rx, ry = boxes[i]
        p.append(marker_ring(cx, cy, rx, ry, period=13, delay=1.5 + i * 1.7, seed=i + 3))
    return p


def advert(paper_uri):
    W, H = 1280, 460
    p = P.open_page(W, H, "Advertisement: available for contract work", "A newspaper display advertisement: Intikhab "
                    "Azam is available for contract work in voice AI agents, RAG and LLM evals, multi-tenant SaaS, "
                    "automation and developer tools. Message @AzamIntikhab on X.", paper_uri)
    M = 60
    p.append('<g filter="url(#ink)">')
    p.append(P.text("ADVERTISEMENT", "body-bold", 13, W / 2, 34, "#5b564d", "middle"))
    p.append(f'<rect x="{M}" y="48" width="{W - 2 * M}" height="{H - 84}" fill="none" stroke="{P.INK}" stroke-width="5"/>'
             f'<rect x="{M + 12}" y="60" width="{W - 2 * M - 24}" height="{H - 108}" fill="none" stroke="{P.INK}" '
             f'stroke-width="1.4"/>')
    p.append(P.text("Available for", "mast", 54, W / 2, 132, P.INK, "middle"))
    p.append(P.text("CONTRACT WORK", "head", 74, W / 2, 214, P.INK, "middle"))
    p.append(P.text("Voice AI agents · RAG and LLM evals · multi-tenant SaaS · automation · developer tools",
                    "body", 21, W / 2, 262, P.INK, "middle"))
    p.append(P.rule(W / 2 - 300, W / 2 + 300, 288, 1))
    handle = "Message @AzamIntikhab on X"
    p.append(P.text(handle, "mono", 30, W / 2, 338, P.RED, "middle"))
    p.append(P.text("Portfolio and case studies: intikhab49.github.io", "body-bold", 18, W / 2, 374, P.INK, "middle"))
    p.append(P.text("Based in Pakistan · working with US teams · remote", "body", 16, W / 2, 400, "#5b564d", "middle"))
    p.append("</g>")
    hw = T.width("@AzamIntikhab", "mono", 30)
    x0 = W / 2 - T.width(handle, "mono", 30) / 2 + T.width("Message ", "mono", 30)
    p.append(P.highlighter(x0 - 4, 312, hw + 8, 34, period=9, delay=1.2))
    p.append(P.stamp(W - 225, 108, ["NOW BOOKING"], rot=-9, period=10, delay=2.5, size=22))
    return p
