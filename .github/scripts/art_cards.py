"""Project cards: a painted truck side-panel per repo (arched art panel + cream sign board)."""
import os

import ta_animals as A
from ta_core import (BLUE, CREAM, DBLUE, DGREEN, DRED, GOLD, GREEN, INK, NIGHT, ORANGE, PINK, PURPLE, RED, SAFFRON,
                     TEAL, WHITE, Doc, n)
from ta_fonts import F
from ta_motifs import TWINKLE, dots, glint, rose, sparkle, tape_defs

W, H = 640, 400
AX, AY, AW, AH = 40, 40, 230, 320       # art panel
TX0, TX1 = 286, 602                      # sign board

CARDS = [
    dict(key="open-jev", repo="open-jev-typed-decision-engine", title="open-jev", sub="TYPED DECISION ENGINE",
         desc="Open reproduction of TypeSafe's Jev: a 150M model that answers typed questions in one forward pass. "
              "0.697 vs Jev's 0.727 accuracy, 2.5x better calibrated, 4x faster, free.",
         chips=["PYTHON", "PYTORCH", "MODERNBERT"], motif=A.eagle, ground=("#1f5fe0", "#8fd0ff"), accent=BLUE,
         alt="Open Jev: open-source typed decision engine, a 150M model reproducing TypeSafe Jev with calibrated confidence"),
    dict(key="pushback", repo="pushback", title="pushback", sub="HOW OFTEN YOU CORRECT YOUR AGENT",
         desc="Reads your Claude Code transcripts, measures how often you correct the agent and on what work, "
              "drafts CLAUDE.md rules from repeat mistakes and exports DPO preference pairs.",
         chips=["PYTHON", "PYPI", "CLAUDE CODE"], motif=A.parrot, ground=("#b3121f", "#ff5a5f"), accent=RED,
         alt="pushback: CLI that measures how often you correct your Claude Code agent and drafts CLAUDE.md rules"),
    dict(key="diff-gate", repo="diff-gate", title="diff-gate", sub="STOPS HALLUCINATED PACKAGES",
         desc="Attackers register the packages LLMs invent. diff-gate reads your coding agent's git diff "
              "and fails on imports that resolve to nothing. Claude Code skill + GitHub Action.",
         chips=["JAVASCRIPT", "GITHUB ACTION", "MIT"], motif=A.nazar, ground=("#141245", "#2d2a8a"), accent=PURPLE,
         alt="diff-gate: Claude Code skill and GitHub Action that blocks AI-hallucinated package imports (slopsquatting)"),
    dict(key="rag-cost-curve", repo="rag-cost-curve", title="rag-cost-curve", sub="WHAT AGENTIC RAG REALLY COSTS",
         desc="Meters every LLM call across naive, reranked, iterative and agentic RAG on multi-hop QA. "
              "Agentic RAG: +32.5 exact match at 2.5x the cost per correct answer. Reranking did not help.",
         chips=["PYTHON", "BENCHMARK", "MUSIQUE"], motif=A.kite, ground=("#0f8fb0", "#7fe0f0"), accent=TEAL,
         alt="rag-cost-curve: benchmark of cost per correct answer for agentic RAG, iterative RAG, reranking and naive RAG"),
    dict(key="minio-from-source", repo="minio-from-source", title="minio-from-source", sub="MINIO IMAGES THAT PULL AGAIN",
         desc="MinIO server + mc built from source at pinned, commit-verified releases. Multi-arch images on GHCR, "
              "smoke-tested in CI, with SBOM and provenance. Unofficial.",
         chips=["DOCKER", "GHCR", "AMD64 + ARM64"], motif=A.camel, ground=("#ff7a2e", "#ffc35a"), accent=ORANGE,
         alt="minio-from-source: free MinIO Docker image built from source, multi-arch amd64 and arm64 on GHCR"),
    dict(key="voice-agent-crm", repo="vapi-voice-agent-crm", title="voice-agent-crm", sub="CALL-OPS FOR AI VOICE AGENTS",
         desc="CRM and call-ops backend for Vapi voice agents: webhook ingestion, predictive dialer, auto-redial, "
              "Stripe-verified conversions and Twilio call status.",
         chips=["NODE.JS", "VAPI", "TWILIO", "STRIPE"], motif=A.bulbul, ground=("#0b5a32", "#2fa860"), accent=GREEN,
         alt="Vapi voice agent CRM: call-ops backend for AI voice agents with predictive dialer and Stripe conversions"),
    dict(key="edgeproof", repo="edgeproof-crypto-trading-backtest", title="edgeproof", sub="DOES THE EDGE SURVIVE FEES?",
         desc="Backtesting and ML validation for crypto perpetuals: triple-barrier labels, purged k-fold CV, "
              "deflated Sharpe and a planted-edge control. Result on BTC, ETH, SOL: no edge after fees.",
         chips=["PYTHON", "LIGHTGBM", "PYTORCH"], motif=A.scales, ground=("#3b137a", "#7a3fd0"), accent=PURPLE,
         alt="EdgeProof: crypto trading backtesting and machine-learning validation with purged CV and deflated Sharpe"),
    dict(key="lead-finder", repo="local-business-lead-finder", title="lead-finder", sub="LOCAL BUSINESS LEADS, PAST THE CAP",
         desc="Self-hosted lead generation: grid search past the Google Places 60-result cap, free OpenStreetMap "
              "fallback, e-mail enrichment, dedup and resumable runs.",
         chips=["PYTHON", "FASTAPI", "STREAMLIT"], motif=A.fishnet, ground=("#0a5f73", "#14a3b8"), accent=TEAL,
         alt="Local business lead finder: self-hosted lead generation past the Google Places 60-result limit"),
]



def wrap(font, text, size, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font.width(t, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def arch(x, y, w, h, k=0):
    x0, x1, y0, y1 = x + k, x + w - k, y + k, y + h - k
    m = (x0 + x1) / 2
    return (f"M{n(x0)} {n(y1)}L{n(x0)} {n(y0 + 70)}Q{n(x0)} {n(y0 + 8)} {n(m)} {n(y0)}"
            f"Q{n(x1)} {n(y0 + 8)} {n(x1)} {n(y0 + 70)}L{n(x1)} {n(y1)}Z")


def build(c):
    d = Doc(W, H, c["alt"], c["desc"])
    d.keyframes("twinkle", TWINKLE)
    tape = tape_defs(d, 16)
    # frame
    d.add(f'<rect x="4" y="8" width="{W - 8}" height="{H - 10}" rx="26" fill="{INK}" opacity=".35"/>')
    d.add(f'<rect x="4" y="4" width="{W - 8}" height="{H - 10}" rx="26" fill="{INK}"/>')
    d.add(f'<rect x="10" y="10" width="{W - 20}" height="{H - 22}" rx="21" fill="url(#{tape})"/>')
    d.define(f'<clipPath id="cframe"><rect x="10" y="10" width="{W - 20}" height="{H - 22}" rx="21"/></clipPath>')
    d.add(glint(d, "cframe", 10, 10, W - 20, H - 22, dur=6, band=70, delay=-(sum(map(ord, c["key"])) % 50) / 10, opacity=.65))
    d.add(f'<rect x="27" y="27" width="{W - 54}" height="{H - 56}" rx="12" fill="{INK}"/>')
    d.add(f'<rect x="30" y="30" width="{W - 60}" height="{H - 62}" rx="10" fill="{NIGHT}"/>')
    # art panel
    g0, g1 = c["ground"]
    gid = d.uid("gr")
    d.define(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g0}"/><stop offset="1" stop-color="{g1}"/></linearGradient>')
    d.define(f'<clipPath id="artclip"><path d="{arch(AX, AY, AW, AH, 0)}"/></clipPath>')
    d.add(f'<path d="{arch(AX - 6, AY - 6, AW + 12, AH + 12)}" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>')
    d.add(f'<path d="{arch(AX, AY, AW, AH)}" fill="url(#{gid})"/>')
    d.add(f'<g clip-path="url(#artclip)"><g transform="translate({AX} {AY})">{c["motif"](d)}</g></g>')
    d.add(f'<path d="{arch(AX, AY, AW, AH)}" fill="none" stroke="{INK}" stroke-width="4"/>')
    # sign board
    d.add(f'<rect x="{TX0}" y="{AY - 6}" width="{TX1 - TX0}" height="{AH + 12}" rx="14" fill="#fff6dc" stroke="{INK}" stroke-width="4"/>')
    d.add(f'<rect x="{TX0 + 7}" y="{AY + 1}" width="{TX1 - TX0 - 14}" height="{AH - 2}" rx="9" fill="none" stroke="{c["accent"]}" stroke-width="2.5"/>')
    cx = (TX0 + TX1) / 2
    size = 46
    while F("shri").width(c["title"], size) > TX1 - TX0 - 44:
        size -= 1
    d.painted(F("shri"), c["title"], cx, 98, size, c["accent"], ow=size * 0.09, shadow=(2.5, 3.5), shadow_fill=INK)
    ss = 24
    while F("tekob").width(c["sub"], ss, 0.03) > TX1 - TX0 - 34:
        ss -= 1
    d.text(F("tekob"), c["sub"], cx, 132, ss, fill=DRED, anchor="middle", ls=0.03)
    d.add(dots(TX0 + 24, 145, TX1 - 24, 145, 12, 2.2, c["accent"], GOLD))
    fs = 18.5
    lines = wrap(F("pop"), c["desc"], fs, TX1 - TX0 - 36)
    while len(lines) > 6:
        fs -= 0.5
        lines = wrap(F("pop"), c["desc"], fs, TX1 - TX0 - 36)
    lh = fs * 1.42
    y = 172
    for ln in lines:
        d.text(F("pop"), ln, TX0 + 18, y, fs, fill="#2a1a12")
        y += lh
    # chips
    chips = c["chips"]
    cs = 17
    widths = [F("tekob").width(t, cs, 0.04) + 18 for t in chips]
    total = sum(widths) + 8 * (len(chips) - 1)
    while total > TX1 - TX0 - 30:
        cs -= 0.5
        widths = [F("tekob").width(t, cs, 0.04) + 18 for t in chips]
        total = sum(widths) + 8 * (len(chips) - 1)
    x = cx - total / 2
    for i, (t, w) in enumerate(zip(chips, widths)):
        col = [c["accent"], INK, DRED, DGREEN][i % 4]
        d.add(f'<rect x="{n(x)}" y="322" width="{n(w)}" height="26" rx="6" fill="{col}" stroke="{INK}" stroke-width="2.5"/>')
        d.text(F("tekob"), t, x + w / 2, 342, cs, fill=WHITE, anchor="middle", ls=0.04)
        x += w + 8
    return d


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "../out/cards"
    for c in CARDS:
        print(c["key"], build(c).save(os.path.join(out, c["key"] + ".svg")))
