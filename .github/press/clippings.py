"""Newspaper clippings: one torn, taped piece of newsprint per project, linked from the README."""
import random

import press as P
import type as T

# repo, art name, kicker, headline, phrase to highlight, body, get-it line, stamp
NEW = [
    ("fairfax", "fairfax", "GOV CLOUD", "Is it available in GCC High? Ask fairfax first.", "GCC High?",
     "Checks a Microsoft 365 GCC, GCC High or DoD and Azure Government plan against Microsoft's own availability "
     "tables: 633 features, every row cited. It also finds commercial endpoints in your code.",
     "pip install fairfax · GitHub Action", "ON PYPI"),
    ("blueprint-runtime", "blueprint-runtime", "AUTOMATION", "Test your Make.com scenarios before Make does.",
     "before Make does.", "Runs exported Make (Integromat) blueprints locally and replays real Make runs, so a broken "
     "mapping fails in CI instead of in production. 71 of 79 real runs reproduced exactly, 0 differ.",
     "npm install -g blueprint-runtime", "ON NPM"),
    ("lifeboat", "lifeboat", "CONTAINERS", "Bitnami's Postgres images, rebuilt from source.", "from source.",
     "PostgreSQL and PostgreSQL HA (repmgr) images with the same paths, scripts and env vars: a drop-in for the "
     "Bitnami Helm charts. Every upstream source SHA-256 pinned, amd64 and arm64.",
     "ghcr.io/intikhab49/lifeboat", "DROP-IN"),
    ("pgvector-cpu-check", "pgvector-cpu-check", "INFRASTRUCTURE", "Which CPU crashes your Postgres image?",
     "crashes", "Runs it on 7 CPU models, from a 2008 Intel to a Raspberry Pi and AWS Graviton2, and names the "
     "faulting instruction behind SIGILL. 13 popular images audited, 3 build bugs found.",
     "uses: intikhab49/pgvector-cpu-check@v1", "SIGILL"),
    ("pdf-cpu-bench", "pdf-cpu-bench", "BENCHMARK", "The best PDF parser for RAG, without a GPU.", "without a GPU.",
     "9 PDF-to-Markdown parsers on a plain 4-core CPU: olmocr-bench accuracy on 1,403 PDFs, seconds per page, "
     "peak RAM and install size. MinerU's CPU tier leads at 74.6%.", "benchmark and results on GitHub", "74.6%"),
    ("whofetched", "whofetched", "INVESTIGATION", "Which AI actually read your page?", "actually read",
     "Secret canary links, a Cloudflare Worker log and published-IP checks, tested on ChatGPT, Claude, Gemini, "
     "Grok, Perplexity and Copilot. Every log is in the repo, timestamped.",
     "Cloudflare Worker · evidence in the repo", "EVIDENCE"),
]
ARCHIVE = [
    ("open-jev-typed-decision-engine", "open-jev", "RESEARCH", "An open decision engine that reports the number it lost.",
     "the number it lost.", "A 150M model reproducing TypeSafe Jev: label, choice and score in one pass. 0.697 vs "
     "Jev's 0.727, 2.5x better calibrated, 4x faster, and it trains on a free Colab T4 in about 30 minutes.",
     "GitHub Action · ONNX · Colab", "OPEN"),
    ("diff-gate", "diff-gate", "SECURITY", "Attackers register the packages your AI invents.", "your AI invents.",
     "diff-gate reads your coding agent's git diff and fails on imports that resolve to nothing, before someone "
     "registers the name. A Claude Code skill and a GitHub Action, zero dependencies.",
     "GitHub Action · Claude Code skill", "BLOCKED"),
    ("rag-cost-curve", "rag-cost-curve", "RESEARCH", "What agentic RAG really costs per right answer.", "really costs",
     "A measured benchmark of agentic, iterative, reranked and naive RAG on MuSiQue multi-hop questions, metering "
     "every LLM call. Agentic RAG: +32.5 exact match, at 2.5x the cost per correct answer.",
     "benchmark · MuSiQue · every call metered", "+32.5 EM"),
    ("pushback", "pushback", "DEVELOPER TOOLS", "How often do you correct your coding agent?", "correct",
     "Measures it from your Claude Code transcripts, drafts CLAUDE.md rules from your recurring corrections, and "
     "exports them as preference pairs.", "pip install pushback", "ON PYPI"),
    ("minio-from-source", "minio-from-source", "CONTAINERS", "A free MinIO image, built from source.",
     "built from source.", "MinIO server and mc built from source at pinned, commit-verified releases. Multi-arch "
     "(amd64, arm64) and smoke-tested, a replacement for minio/minio and quay.io/minio. Unofficial.",
     "ghcr.io · GitHub Action", "MULTI-ARCH"),
    ("vapi-voice-agent-crm", "voice-agent-crm", "VOICE AI", "Call ops for AI voice agents.", "AI voice agents.",
     "A CRM and call-ops backend for Vapi voice agents: webhook ingestion, a predictive dialer, auto-redial and "
     "payment-verified conversions with Stripe, plus Twilio call status and analytics.",
     "Node.js · Express · Twilio · Stripe", "VOICE"),
]


def torn(x0, y0, x1, y1, rng, step=9, amp=3.2):
    """A polygon with torn top and bottom edges and slightly uneven sides."""
    pts = []
    x = x0
    while x < x1:
        pts.append((x, y0 + rng.uniform(-amp, amp)))
        x += rng.uniform(step * 0.6, step * 1.4)
    pts.append((x1, y0 + rng.uniform(-amp, amp)))
    y = y0
    while y < y1:
        pts.append((x1 + rng.uniform(-1, 1), y))
        y += rng.uniform(20, 40)
    x = x1
    while x > x0:
        pts.append((x, y1 + rng.uniform(-amp, amp)))
        x -= rng.uniform(step * 0.6, step * 1.4)
    pts.append((x0, y1 + rng.uniform(-amp, amp)))
    y = y1
    while y > y0:
        pts.append((x0 + rng.uniform(-1, 1), y))
        y -= rng.uniform(20, 40)
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)


def clipping(i, repo, kicker, head, phrase, body, getit, stamp_text, paper_uri):
    W, H = 640, 440
    rng = random.Random(i * 31 + 7)
    rot = rng.uniform(-1.3, 1.3)
    parts = P.open_page(W, H, f"{repo}: {head}", f"A newspaper clipping. {kicker}. {head} {body} {getit}.", "")
    parts.pop()                                   # no full-size paper: the clipping is torn out of it
    parts.append('<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="3" '
                 'stdDeviation="4" flood-opacity=".35"/></filter>'
                 f'<clipPath id="torn{i}"><polygon points="{torn(16, 22, W - 16, H - 16, rng)}"/></clipPath></defs>')
    parts.append(f'<g transform="rotate({rot:.2f} {W / 2} {H / 2})"><g filter="url(#sh)"><g clip-path="url(#torn{i})">'
                 f'<image href="{paper_uri}" width="{W}" height="{H}" preserveAspectRatio="none"/></g></g>')
    X, Y, CW = 40, 64, W - 80
    parts.append('<g filter="url(#ink)">')
    parts.append(P.text(kicker, "body-bold", 15, X, Y, P.RED))
    lines = P.wrap(head, "head", 33, CW)
    assert len(lines) <= 2, (repo, lines)
    hy = Y + 42
    hl = None
    words = phrase.split()
    # the longest run of the phrase's words that sits on one line (a wrap can split the phrase)
    candidates = [" ".join(words[a:b]) for n in range(len(words), 0, -1) for a in range(len(words) - n + 1)
                  for b in [a + n]]
    for j, line in enumerate(lines):
        parts.append(P.text(line, "head", 33, X, hy + j * 40))
    for cand in candidates:
        for j, line in enumerate(lines):
            if hl is None and cand in line:
                k = line.index(cand)
                hl = (X + T.width(line[:k], "head", 33) - 3, hy + j * 40 - 27, T.width(cand, "head", 33) + 6, 34)
    assert hl, (repo, phrase)
    ry = hy + (len(lines) - 1) * 40 + 20
    parts.append(P.rule(X, X + CW, ry, 1))
    blines = P.wrap(body, "body", 18.5, CW)
    assert len(blines) <= 5, (repo, len(blines))
    for j, line in enumerate(blines):
        parts.append(P.text(line, "body", 18.5, X, ry + 32 + j * 26))
    parts.append(P.rule(X, X + CW, H - 74, 0.8))
    fs = min(16, 16 * (CW - 150) / max(1, T.width(getit, "mono", 16)))
    parts.append(P.text(getit, "mono", fs, X, H - 48))
    parts.append(P.text("github.com/intikhab49/" + repo, "body", 13.5, X, H - 28, "#5b564d"))
    parts.append("</g>")
    parts.append(P.highlighter(*hl, period=8 + (i % 3), delay=0.8 + (i % 4) * 0.6))
    parts.append(P.stamp(W - 110, H - 68, [stamp_text], rot=rng.uniform(-14, -6), period=10 + i % 4,
                         delay=2 + (i % 5) * 0.9, size=22))
    tx = rng.uniform(220, 360)                     # a strip of tape across the top edge
    parts.append(f'<rect x="{tx:.0f}" y="8" width="120" height="30" fill="#f1e8c8" opacity=".82" stroke="#d8cba0" stroke-width=".8" '
                 f'transform="rotate({rng.uniform(-6, 6):.1f} {tx + 60:.0f} 23)"/>')
    parts.append("</g>")
    return parts
