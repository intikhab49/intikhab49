"""Paints every image on the profile into assets/. Run from anywhere: python .github/sky/build.py [name ...]

Needs numpy, Pillow and uharfbuzz. The daily stats card is separate (field_log.py, standard library only);
this script also bakes the glyphs and the painted background it uses.
"""
import os
import sys

from PIL import Image, ImageFilter

import paint
import scenes
import scenes_more as more
import svg
import type as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT, os.environ.get("SKY_ASSETS", "assets"))
CREAM, GOLD, MIST, DIM = "#f4ead2", "#e8c98e", "#c9d3ec", "#9aa6c8"


def write(name, parts):
    path = os.path.join(ASSETS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg.close(parts))
    print(f"{name}: {os.path.getsize(path) // 1024} KB")


def hero():
    W, H = 1280, 760
    ref, angle, dens, info = scenes.hero(W * 2, H * 2)
    img = paint.repaint(ref, angle, seed=11)
    img, bright = paint.stars(img, 5, 11000, dens, bright=0.006, size=1.5, keep=70)
    img, _ = scenes.observer(img, info["rock_top"])
    img = paint.canvas_texture(img, 2).resize((W, H), Image.LANCZOS)
    img.save(os.path.join(HERE, "out", "hero.png"))
    # keep the name's corner clear of twinkles
    bright = [(x, y, r) for x, y, r in bright if not (x < 1650 and y < 600)]
    p = svg.open_svg(W, H, "Intikhab Azam: AI/ML engineer, researcher and systems architect",
                     "A painted night: the Milky Way rising over a mountain lake, its pink core above the left ridge, "
                     "and someone on a rock at the right shore looking up at it through a small telescope. "
                     "Stars twinkle and the odd meteor crosses the sky.")
    p.append(svg.painting(svg.jpeg(img, 84), W, H))
    p.append('<ellipse class="breathe" cx="400" cy="380" rx="230" ry="130" fill="#e7a2b8" opacity="0" '
             'filter="url(#soft)" style="mix-blend-mode:screen"/>')
    p.append(svg.twinkles(bright, 0.5, 4))
    p.append(svg.meteors([(980, 70, 152, 150, 11, 2.5), (520, 40, 158, 120, 17, 9), (1180, 210, 148, 110, 23, 15)]))
    for i, (x, y, rw) in enumerate([(330, 628, 70), (410, 668, 46), (300, 712, 54), (470, 640, 30), (380, 740, 40)]):
        p.append(f'<ellipse class="shimmer" cx="{x}" cy="{y}" rx="{rw}" ry="1.3" fill="#f4cfd9" filter="url(#blur2)" '
                 f'style="animation-duration:{4.5 + i * 1.6:.1f}s;animation-delay:-{i * 1.3:.1f}s"/>')
    p.append(svg.text("Intikhab Azam", "display-bold", 108, 70, 150, CREAM, glow="#070a1e"))
    p.append(svg.text("AI/ML engineer, researcher & systems architect", "serif", 32, 73, 204, MIST, glow="#070a1e"))
    p.append(svg.text("انتخاب اعظم", "urdu", 44, 76, 300, GOLD, glow="#070a1e"))
    write("hero.svg", p)


# (repo, card art, title, pitch, fact line, nebula colours, constellation points in a 0..1 box, edges)
CARDS = [
    ("fairfax", "fairfax", "fairfax", "Is it available in GCC High? Checks a Microsoft gov-cloud plan against Microsoft's own "
     "tables, with every row cited.", "633 features · PyPI · GitHub Action", ("#2f8f9c", "#3b5fb8"),
     [(.1, .8), (.2, .45), (.5, .2), (.8, .45), (.9, .8), (.5, .62), (.5, .95)], [(0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 3), (5, 6)]),
    ("blueprint-runtime", "blueprint-runtime", "blueprint-runtime", "Test Make.com scenarios offline. Replays real Make "
     "runs and catches broken mappings before you deploy.", "71 of 79 real runs reproduced · npm", ("#7a4fc0", "#c06aa8"),
     [(.05, .6), (.27, .4), (.5, .55), (.72, .35), (.95, .5), (.6, .9)], [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)]),
    ("pgvector-cpu-check", "pgvector-cpu-check", "pgvector-cpu-check", "Which CPU crashes your Postgres image? Runs it on 7 "
     "CPU models and names the faulting instruction.", "13 images audited · 3 build bugs found", ("#2b9a7c", "#4bb3c8"),
     [(.2, .2), (.8, .2), (.8, .8), (.2, .8), (.5, .5), (.05, .5), (.95, .5)], [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 2), (5, 3), (6, 1)]),
    ("diff-gate", "diff-gate", "diff-gate", "Fails your coding agent's diff when an import resolves to nothing, before "
     "attackers register the name.", "Claude Code skill · GitHub Action", ("#b8435e", "#d07a52"),
     [(.15, .95), (.15, .45), (.35, .15), (.65, .15), (.85, .45), (.85, .95), (.5, .55)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 3)]),
    ("lifeboat", "lifeboat", "lifeboat", "Bitnami's PostgreSQL and PostgreSQL HA images, rebuilt from upstream source as "
     "drop-ins for the Helm charts.", "every source pinned · amd64 + arm64", ("#2c4fa8", "#5a86d8"),
     [(.05, .62), (.25, .85), (.75, .85), (.95, .62), (.5, .62), (.5, .1), (.78, .45)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (4, 5), (5, 6), (6, 4)]),
    ("open-jev-typed-decision-engine", "open-jev", "open-jev", "An open 150M typed decision engine: label, choice and "
     "score in one pass, with calibrated confidence.", "0.697 vs 0.727 · 2.5x better calibrated", ("#c09a3a", "#d8673f"),
     [(.5, .95), (.5, .6), (.2, .3), (.8, .3), (.08, .05), (.35, .05), (.92, .08)], [(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]),
    ("rag-cost-curve", "rag-cost-curve", "rag-cost-curve", "What agentic RAG really costs: cost per correct answer for four "
     "RAG designs on multi-hop questions.", "+32.5 exact match at 2.5x the cost", ("#c4762f", "#b04870"),
     [(.05, .9), (.3, .75), (.5, .58), (.68, .38), (.82, .2), (.95, .05)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),
    ("vapi-voice-agent-crm", "voice-agent-crm", "vapi-voice-agent-crm", "Call ops for AI voice agents: webhooks, a "
     "predictive dialer, auto-redial and Stripe-verified conversions.", "Node.js · Twilio · Stripe", ("#a53f9a", "#5a4fc4"),
     [(.0, .5), (.15, .3), (.3, .7), (.45, .15), (.6, .85), (.75, .3), (.9, .65), (1, .5)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]),
]


def wrap(text, font, size, width):
    import type as T
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if T.width(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def cards():
    W, H = 640, 360
    for i, (repo, art, title, pitch, fact, (h1, h2), pts, edges) in enumerate(CARDS):
        ref, angle, dens = scenes.card(W * 2, H * 2, 100 + i * 7, h1, h2)
        img = paint.repaint(ref, angle, seed=200 + i, passes=((18, 0.0), (9, 0.03), (4.5, 0.028), (2.4, 0.026)))
        img, bright = paint.stars(img, 300 + i, 2600, dens, bright=0.006, size=1.3, keep=24)
        img = paint.canvas_texture(img, 9 + i).resize((W, H), Image.LANCZOS)
        p = svg.open_svg(W, H, f"{title}: {pitch}", f"A painted patch of night sky with a nebula, and {title} drawn as a "
                         f"constellation. {fact}.")
        p.append(svg.painting(svg.jpeg(img, 78), W, H))
        bright = [(x, y, r) for x, y, r in bright if x > W * 0.9]
        p.append(svg.twinkles(bright, 0.5, i, 0.8))
        # the constellation, drawn into the right half
        bx, by, bw, bh = 392, 70, 210, 200
        P = [(bx + x * bw, by + y * bh) for x, y in pts]
        for k, (a, b) in enumerate(edges):
            (x1, y1), (x2, y2) = P[a], P[b]
            ln = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#dfe6ff" stroke-opacity=".55" '
                     f'stroke-width="1.4" class="glint" style="animation-duration:{5 + k % 3}s;animation-delay:-{k * 0.7:.1f}s"/>')
        for k, (x, y) in enumerate(P):
            r = 4.2 if k % 3 == 0 else 3.2
            dur = 3 + (k * 1.37) % 3
            p.append(f'<g>'
                     f'<circle class="tw" cx="{x:.1f}" cy="{y:.1f}" r="{r * 3.4:.1f}" fill="url(#sg)" '
                     f'style="animation-duration:{dur:.1f}s"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 0.55:.1f}" fill="#fff"/></g>')
        size = min(52, 52 * 340 / max(1, __import__("type").width(title, "display-bold", 52)))
        p.append(svg.text(title, "display-bold", size, 34, 88, CREAM, glow="#060818"))
        lines = wrap(pitch, "serif", 25, 345)
        assert len(lines) <= 4, (title, lines)
        for j, line in enumerate(lines):
            p.append(svg.text(line, "serif", 25, 36, 136 + j * 33, MIST, glow="#060818"))
        fs = min(18.5, 18.5 * 560 / max(1, __import__("type").width(fact, "mono", 18.5)))
        p.append(svg.text(fact, "mono", fs, 36, 330, GOLD, glow="#060818"))
        write(f"cards/{art}.svg", p)


WORLDS = [
    ("Voice AI agents", "Vapi · Twilio · CRMs", ("#3a1650", "#9a3f8e", "#f0a6d0"), 5, False),
    ("RAG and LLM agents", "tools · memory · search", ("#0f2f45", "#2f8f9c", "#a6e6e0"), 7, False),
    ("LLM evals", "calibration · benchmarks", ("#3d2a0e", "#c09a3a", "#f6e0a0"), 4, True),
    ("Multi-tenant SaaS", "Postgres RLS · BFF auth", ("#10204a", "#3b6fc8", "#c8dcff"), 6, False),
    ("Agentic coding", "Claude Code · MCP", ("#3c1420", "#c45a5a", "#f6c0a0"), 8, False),
    ("Developer tools", "PyPI · npm · Actions", ("#0f3324", "#3c9a62", "#c8f0b0"), 5, True),
]


def worlds():
    W, H = 1280, 380
    ref, angle, dens = more.sky_strip(W * 2, H * 2, 41)
    centers = [(110 + i * 212, y) for i, y in enumerate((146, 156, 140, 152, 158, 144))]
    radii = [128, 96, 112, 136, 90, 108]
    for i, ((name, sub, cols, bands, ring), (x, y)) in enumerate(zip(WORLDS, centers)):
        more.planet(ref, angle, dens, x * 2, y * 2, radii[i], 60 + i, cols, bands, 0.12 + 0.1 * i, ring)
    img = paint.repaint(ref, angle, seed=61, passes=((16, 0.0), (8, 0.03), (4, 0.028), (2.2, 0.026)))
    img, bright = paint.stars(img, 62, 2600, dens, bright=0.005, size=1.3, keep=20)
    img = paint.canvas_texture(img, 63).resize((W, H), Image.LANCZOS)
    p = svg.open_svg(W, H, "What I build: voice AI agents, RAG and LLM agents, LLM evals, multi-tenant SaaS, agentic "
                     "coding and developer tools", "Six painted planets in a row, one for each kind of work, each with "
                     "a small moon going round it.",
                     ".orb{animation:orbit linear infinite}"
                     "@keyframes orbit{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}")
    p.append(svg.painting(svg.jpeg(img, 80), W, H))
    p.append(svg.twinkles(bright, 0.5, 64, 0.8))
    for i, ((name, sub, cols, bands, ring), (x, y)) in enumerate(zip(WORLDS, centers)):
        r = radii[i] / 2
        a, b, dur = r + 20, (r + 20) * 0.3, 12 + i * 3
        orbit = f"M{x + a:.0f},{y} A{a:.0f},{b:.0f} 0 1 1 {x - a:.0f},{y} A{a:.0f},{b:.0f} 0 1 1 {x + a:.0f},{y}"
        p.append(f'<circle r="3.6" fill="#eef2ff"><animateMotion dur="{dur}s" begin="-{i * 2.3:.1f}s" '
                 f'repeatCount="indefinite" path="{orbit}"/><animate attributeName="opacity" dur="{dur}s" '
                 f'begin="-{i * 2.3:.1f}s" repeatCount="indefinite" values="1;1;0;0;1" keyTimes="0;.6;.64;.86;1"/></circle>')
        p.append(svg.text(name, "serif-bold", 25, x, 268, CREAM, "middle", glow="#060818"))
        fs = min(18, 18 * 196 / max(1, T.width(sub, "serif", 18)))
        p.append(svg.text(sub, "serif", fs, x, 296, GOLD, "middle", glow="#060818", opacity=.95))
    write("worlds.svg", p)


STACK = [
    ("AI and LLMs", ["Claude", "Claude Code", "MCP", "OpenAI", "Codex", "Gemini", "DeepSeek", "OpenRouter", "LangChain",
                     "Hugging Face", "NotebookLM"]),
    ("Voice", ["Vapi", "Twilio", "ElevenLabs", "Deepgram", "Retell AI"]),
    ("Machine learning", ["PyTorch", "scikit-learn", "LightGBM", "XGBoost", "ONNX", "NumPy", "pandas", "OpenCV",
                          "Jupyter", "Colab"]),
    ("Backend", ["Python", "FastAPI", "Flask", "Node.js", "NestJS", "Express", "Prisma", "Drizzle", "PostgreSQL",
                 "Neon", "MySQL", "SQLite", "MongoDB", "Stripe", "Resend"]),
    ("Frontend", ["TypeScript", "JavaScript", "React", "Next.js", "Vite", "Tailwind CSS", "Astro", "Streamlit",
                  "better-auth"]),
    ("Infra and automation", ["Docker", "Kubernetes", "NGINX", "Prometheus", "GitHub Actions", "GHCR",
                              "Cloudflare Workers", "Vercel", "MinIO", "Linux", "Bash", "n8n", "Playwright", "Jest"]),
]


def catalogue():
    import random
    import type as T
    W = 1280
    rows = max(len(items) for _, items in STACK)
    H = 150 + rows * 30 + 40
    ref, angle, dens = more.sky_strip(W * 2, H * 2, 71, lift=-0.1)
    img = paint.repaint(ref, angle, seed=72, passes=((18, 0.0), (9, 0.03), (4.5, 0.028)))
    img, _ = paint.stars(img, 73, 1400, dens * 0.6, bright=0.003, size=1.2, keep=0)
    img = paint.canvas_texture(img, 74).resize((W, H), Image.LANCZOS)
    names = ", ".join(n for _, items in STACK for n in items)
    p = svg.open_svg(W, H, "Tech stack", "A page from a star catalogue, one column per field, each tool listed as a "
                     "star: " + names + ".")
    p.append(svg.painting(svg.jpeg(img.filter(ImageFilter.GaussianBlur(0.6)), 66), W, H))
    p.append(svg.text("A catalogue of the tools I work with", "display-bold", 40, 60, 72, CREAM, glow="#060818"))
    colw = (W - 120) / len(STACK)
    rng = random.Random(5)
    for c, (head, items) in enumerate(STACK):
        x = 60 + c * colw
        p.append(svg.text(head, "serif-bold", 21, x, 128, GOLD, glow="#060818"))
        p.append(f'<line x1="{x:.0f}" y1="140" x2="{x + colw - 24:.0f}" y2="140" stroke="#e8c98e" stroke-opacity=".35"/>')
        for k, item in enumerate(items):
            y = 172 + k * 30
            r = 3.2 if k < 3 else 2.4 if k < 7 else 1.8
            dur = rng.uniform(2.5, 6)
            p.append(f'<circle class="tw" cx="{x + 5:.0f}" cy="{y - 6}" r="{r * 3:.1f}" fill="url(#sg)" '
                     f'style="animation-duration:{dur:.1f}s;animation-delay:-{rng.uniform(0, dur):.1f}s"/>'
                     f'<circle cx="{x + 5:.0f}" cy="{y - 6}" r="{r * 0.6:.1f}" fill="#fff"/>')
            fs = min(19, 19 * (colw - 44) / max(1, T.width(item, "serif", 19)))
            p.append(svg.text(item, "serif", fs, x + 18, y, MIST))
    write("catalogue.svg", p)


def contact():
    W, H = 1280, 340
    ref, angle, dens = more.dawn(W * 2, H * 2, 81)
    img = paint.repaint(ref, angle, seed=82, passes=((18, 0.0), (9, 0.03), (4.5, 0.028), (2.4, 0.026)))
    img, bright = paint.stars(img, 83, 1600, dens, bright=0.006, size=1.3, keep=24)
    img = paint.canvas_texture(img, 84).resize((W, H), Image.LANCZOS)
    p = svg.open_svg(W, H, "Open to contract work. Message @AzamIntikhab on X.",
                     "The sky just before sunrise over dark hills, the last stars fading.")
    p.append(svg.painting(svg.jpeg(img, 82), W, H))
    p.append(svg.twinkles([(x, y, r) for x, y, r in bright if y < 300], 0.5, 85, 0.8))
    p.append('<ellipse class="breathe" cx="640" cy="300" rx="420" ry="60" fill="#f6c08a" filter="url(#soft)" '
             'opacity="0" style="mix-blend-mode:screen;animation-duration:7s"/>')
    p.append(svg.meteors([(1060, 40, 160, 110, 13, 4)]))
    p.append(svg.text("Open to contract work", "display-bold", 60, 640, 112, CREAM, "middle", glow="#070a1e"))
    p.append(svg.text("voice AI agents · RAG and LLM evals · multi-tenant SaaS · automation · developer tools",
                      "serif", 25, 640, 160, MIST, "middle", glow="#070a1e"))
    p.append(svg.text("message @AzamIntikhab on X", "mono", 21, 640, 206, GOLD, "middle", glow="#070a1e"))
    write("contact.svg", p)


def stats():
    """The background and glyphs for field_log.py, which draws the live card every day in Actions."""
    import json
    W, H = 1280, 470
    ref, angle, dens = more.sky_strip(W * 2, H * 2, 91, lift=0.05)
    img = paint.repaint(ref, angle, seed=92, passes=((18, 0.0), (9, 0.03), (4.5, 0.028)))
    img, _ = paint.stars(img, 93, 1500, dens * 0.5, bright=0.003, size=1.2, keep=0)
    img = paint.canvas_texture(img, 94).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))
    img.save(os.path.join(HERE, "stats_bg.jpg"), "JPEG", quality=74, optimize=True, progressive=True)
    chars = [chr(c) for c in range(32, 127)] + ["·"]
    fonts = {}
    for key, font in (("display", "display-bold"), ("serif", "serif"), ("mono", "mono")):
        f, upem = T._font(font)
        glyphs = {}
        for ch in chars:
            gl, _, adv = T.runs(ch, font)
            glyphs[ch] = [round(adv), T.glyph_d(font, gl[0][0])]
        fonts[key] = {"upem": upem, "glyphs": glyphs}
    with open(os.path.join(HERE, "glyphs.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(fonts, fh, separators=(",", ":"), ensure_ascii=False)
    print(f"stats_bg.jpg: {os.path.getsize(os.path.join(HERE, 'stats_bg.jpg')) // 1024} KB, "
          f"glyphs.json: {os.path.getsize(os.path.join(HERE, 'glyphs.json')) // 1024} KB")


JOBS = {"hero": hero, "cards": cards, "worlds": worlds, "catalogue": catalogue, "contact": contact, "stats": stats}

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for name in sys.argv[1:] or JOBS:
        JOBS[name]()
