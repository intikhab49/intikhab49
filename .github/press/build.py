"""Prints the profile as a newspaper into assets/. Run: python .github/press/build.py [front ...]

Needs numpy, Pillow and uharfbuzz. Every figure in the copy comes from the repositories' own READMEs.
"""
import os
import sys

import press as P
import svg
import type as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT, os.environ.get("PRESS_ASSETS", "assets"))
INK, RED = P.INK, P.RED
GREY = "#5b564d"


def write(name, parts):
    path = os.path.join(ASSETS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg.close(parts))
    print(f"{name}: {os.path.getsize(path) // 1024} KB")


def headline(lines, font, size, x, y, lead, anchor="start"):
    return "".join(P.text(s, font, size, x, y + i * lead, INK, anchor) for i, s in enumerate(lines))


def front():
    W, H = 1280, 1225
    paper = P.jpeg(P.newsprint(W, H, 11), 78)
    p = P.open_page(W, H, "The Intikhab Times: front page", "A newspaper front page about Intikhab Azam's open-source "
                    "work. Lead story: Microsoft edits a Teams page and fairfax catches it the same day. Also: "
                    "blueprint-runtime reproduces 71 of 79 real Make.com runs, pgvector-cpu-check finds 3 build bugs "
                    "in 13 Postgres images, Open Jev loses on accuracy and wins on calibration, and agentic RAG costs "
                    "2.5 times more per correct answer.", paper)
    p.append('<g filter="url(#ink)">')
    M = 44
    # ears and masthead
    p.append(P.rule(M, 250, 40, 1) + P.rule(M, 250, 112, 1))
    p.append(P.text("Portfolio", "head-bold", 21, M + 103, 70, INK, "middle"))
    p.append(P.text("intikhab49.github.io", "body", 15, M + 103, 96, INK, "middle"))
    p.append(P.rule(W - 250, W - M, 40, 1) + P.rule(W - 250, W - M, 112, 1))
    p.append(P.text("Open to contract", "head-bold", 21, W - M - 103, 70, RED, "middle"))
    p.append(P.text("message @AzamIntikhab on X", "body", 15, W - M - 103, 96, INK, "middle"))
    p.append(P.text("The Intikhab Times", "mast", 92, W / 2, 112, INK, "middle"))
    p.append(P.rule(M, W - M, 136, 3) + P.rule(M, W - M, 142, 1))
    p.append(P.text("PAKISTAN · REMOTE EDITION", "body-bold", 14, M, 162))
    p.append(P.text("AI/ML ENGINEER · RESEARCHER · SYSTEMS ARCHITECT", "body-bold", 14, W / 2, 162, INK, "middle"))
    p.append(P.text("VOL. I · EST. 2023", "body-bold", 14, W - M, 162, INK, "end"))
    p.append(P.rule(M, W - M, 174, 1) + P.rule(M, W - M, 178, 3))

    # lead story, left three columns
    LX, LW = M, 820
    b, bw = P.breaking(LX, 214)
    p.append(b)
    p.append(P.text("GOV CLOUD", "body-bold", 15, LX + bw + 12, 212, RED))
    p.append(headline(["Microsoft quietly edits a Teams page.", "fairfax catches it the same day."],
                      "head", 47, LX, 270, 54))
    deck = P.text("The free gov-cloud checker re-reads 33 Microsoft sources every week, and keeps a", "body", 21,
                  LX, 352, GREY) + P.text("Wayback Machine copy of each one.", "body", 21, LX, 380, GREY)
    p.append(P.typewriter(deck, LX, 330, LW, 60, period=13, delay=0.8))
    p.append(P.rule(LX, LX + LW, 400, 1))
    by = "By Intikhab Azam"
    p.append(P.text(by, "body-bold", 15, LX, 424) +
             P.text("· AI/ML engineer and systems architect", "body", 15, LX + T.width(by, "body-bold", 15) + 8, 424, GREY))
    body = [
        "On 12 October 2026 Microsoft reworded two rows in its Teams service description. No feature changed "
        "status, but fairfax flagged the edit the same day, because its check compares every row it quotes with "
        "the live page.",
        "fairfax checks a Microsoft 365 GCC, GCC High or DoD plan, and an Azure Government one, against "
        "Microsoft's own availability tables: 633 features, and every answer quotes the row it came from.",
        "It also scans code for commercial endpoints that break in government clouds, decodes sign-in errors such "
        "as AADSTS900439, and runs as a GitHub Action or as an MCP server for coding agents.",
        "Since version 0.2.2 every cited page has an archived copy that was checked to hold the same rows, so a "
        "citation survives even if Microsoft deletes the page. Install it with pip install fairfax.",
    ]
    p.append(P.flow(body, "body", 16.5, 23, LX, 460, 258, 2, 23, 16))
    p.append(f'<rect x="{LX + 268}" y="440" width="0.8" height="380" fill="{INK}" opacity=".5"/>'
             f'<rect x="{LX + 549}" y="440" width="0.8" height="380" fill="{INK}" opacity=".5"/>')
    # pull quote in the third column
    QX = LX + 562
    p.append(P.text("“", "head", 80, QX - 8, 492, RED))
    p.append(headline(["Is this feature", "available in", "GCC High?"], "head", 31, QX + 6, 510, 37))
    p.append(P.text("The question fairfax answers,", "body", 15, QX + 6, 636, GREY) +
             P.text("with Microsoft's own rows.", "body", 15, QX + 6, 656, GREY))
    p.append("</g>")
    p.append(P.highlighter(QX + 2, 568, 152, 30, period=10, delay=2.0))
    p.append(P.stamp(QX + 128, 740, ["VERIFIED", "1,164 ROWS"], rot=-8, period=11, delay=3))
    p.append('<g filter="url(#ink)">')

    # right column: second story and the figures board
    RX, RW = M + LW + 24, W - M - (M + LW + 24)
    p.append(f'<rect x="{RX - 12}" y="196" width="1" height="600" fill="{INK}"/>')
    p.append(P.text("AUTOMATION", "body-bold", 15, RX, 212, RED))
    p.append(headline(["71 of 79 real", "Make.com runs,", "reproduced exactly"], "head", 33, RX, 254, 38))
    p.append("</g>")
    p.append(P.highlighter(RX - 2, 228, 214, 34, period=9, delay=1.0))
    p.append('<g filter="url(#ink)">')
    p.append(P.column([
        "blueprint-runtime runs exported Make scenarios on your own machine and compares every module with what "
        "Make recorded. The other 8 runs use behavior it has no recording of, so it refuses them instead of "
        "guessing.",
        "A filter that silently drops every record now fails the test, with the filter named. Install it with npm "
        "install -g blueprint-runtime."], "body", 15.5, 21, RX, 368, RW)[0])
    p.append(P.rule(RX, W - M, 588, 3) + P.text("TODAY'S FIGURES", "head-bold", 19, RX, 616))
    figures = [("633", "features cited"), ("1164", "rows re-checked"), ("13", "images audited"),
               ("3", "build bugs found"), ("9", "PDF parsers tested")]
    p.append("</g>")
    for i, (val, label) in enumerate(figures):
        y = 634 + i * 52
        board, bwid = P.splitflap(RX, y, val, cw=26, ch=40, period=12, delay=1.0 + i * 0.4, size=27)
        p.append(board)
        p.append(f'<g filter="url(#ink)">{P.text(label, "body", 16, RX + 4 * 30 + 10, y + 27)}</g>')
    p.append('<g filter="url(#ink)">')

    # below the fold
    FY = 900
    p.append(P.rule(M, W - M, FY - 18, 3) + P.rule(M, W - M, FY - 12, 1))
    cw = (W - 2 * M - 2 * 30) / 3
    stories = [
        ("INFRASTRUCTURE", ["Old CPUs crash popular", "Postgres images. Now", "you can find out first."],
         "pgvector-cpu-check replays an image on 7 CPU models, from a 2008 Nehalem to a Raspberry Pi and AWS "
         "Graviton2, and names the exact instruction behind Illegal instruction. Of 13 popular images it audited, "
         "3 had build bugs."),
        ("RESEARCH", ["An open decision engine", "loses on accuracy and", "wins on calibration"],
         "Open Jev reproduces TypeSafe Jev with a 150M model that trains on a free Colab T4 in about 30 minutes. "
         "It scores 0.697 against Jev's 0.727, is 2.5 times better calibrated and 4 times faster, and the repo "
         "leads with the number it lost."),
        ("RESEARCH", ["Agentic RAG: 32.5 points", "better, 2.5 times the cost", "per correct answer"],
         "rag-cost-curve meters every LLM call to price each correct answer for agentic, iterative, reranked and "
         "naive RAG on MuSiQue multi-hop questions. Agentic RAG gains 32.5 points of exact match over naive RAG "
         "and pays 2.5 times more for each right answer."),
    ]
    for i, (kicker, head, body_text) in enumerate(stories):
        x = M + i * (cw + 30)
        p.append(P.text(kicker, "body-bold", 14, x, FY + 14, RED))
        p.append(headline(head, "head", 26, x, FY + 48, 30))
        p.append(P.column([body_text], "body", 15, 20.5, x, FY + 150, cw)[0])
        if i:
            p.append(f'<rect x="{x - 15}" y="{FY}" width="0.8" height="300" fill="{INK}" opacity=".6"/>')
    p.append("</g>")
    p.append(P.ticker(H - 44, 44, W, [
        "fairfax 0.2.2 on PyPI: every Microsoft source now archived",
        "blueprint-runtime: a > changed to >= is caught at the cutoff",
        "pgvector-cpu-check: 3 build bugs in 13 Postgres images",
        "pdf-cpu-bench: 9 PDF parsers for RAG, timed on a 4-core CPU",
        "whofetched: which AI really fetched your page",
        "portfolio, client case studies and every project: intikhab49.github.io",
        "open to contract work: message @AzamIntikhab on X"]))
    write("front.svg", p)


def clips():
    import clippings as C
    paper = P.jpeg(P.newsprint(640, 440, 21, fold=False), 76)
    for i, spec in enumerate(C.NEW + C.ARCHIVE):
        write(f"clips/{spec[1]}.svg", C.clipping(i, spec[0], *spec[2:], paper))


def inside():
    import sections as S
    write("services.svg", S.services(P.jpeg(P.newsprint(1280, 636, 31, fold=False), 74)))
    write("classifieds.svg", S.classifieds(P.jpeg(P.newsprint(1280, 520, 41, fold=False), 74)))
    write("advert.svg", S.advert(P.jpeg(P.newsprint(1280, 460, 51, fold=False), 74)))


def markets():
    """Newsprint and glyph outlines for field_log.py, which sets the Markets page every day in Actions."""
    import json
    P.newsprint(1280, 560, 61, fold=False).save(os.path.join(HERE, "markets_bg.jpg"), "JPEG", quality=72,
                                                 optimize=True, progressive=True)
    chars = [chr(c) for c in range(32, 127)] + ["·", "•"]
    fonts = {}
    for font in ("mast", "body", "body-bold", "mono"):
        _, upem = T._font(font)
        glyphs = {}
        for ch in chars:
            gl, _, adv = T.runs(ch, font)
            glyphs[ch] = [round(adv), T.glyph_d(font, gl[0][0])]
        fonts[font] = {"upem": upem, "glyphs": glyphs}
    with open(os.path.join(HERE, "glyphs.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(fonts, fh, separators=(",", ":"), ensure_ascii=False)
    print(f"markets_bg.jpg: {os.path.getsize(os.path.join(HERE, 'markets_bg.jpg')) // 1024} KB, glyphs.json: "
          f"{os.path.getsize(os.path.join(HERE, 'glyphs.json')) // 1024} KB")


JOBS = {"front": front, "clips": clips, "inside": inside, "markets": markets}

if __name__ == "__main__":
    for name in sys.argv[1:] or JOBS:
        JOBS[name]()
