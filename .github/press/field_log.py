"""The daily Markets page: the last twelve months of GitHub activity, set like a newspaper's market report.

Standard library only. The newsprint (markets_bg.jpg) and glyph outlines (glyphs.json) are made by build.py.
Env: GITHUB_TOKEN, GH_USER (default intikhab49), OUT_DIR (default dist). Writes OUT_DIR/stats.svg.
Every animation rests on the finished page, so nothing is hidden when motion is off.
"""
import base64
import datetime as dt
import json
import math
import os
import random
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
USER = os.environ.get("GH_USER", "intikhab49")
OUT = os.environ.get("OUT_DIR", "dist")
W, H = 1280, 560
INK, RED, GREY = "#1d1b18", "#b3261e", "#5b564d"


def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": USER,
                                          "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"] and not r["private"]]
    langs = {}
    for r in own:
        if r["language"] and not r.get("archived"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
           totalContributions weeks{contributionDays{contributionCount date}}}}}}"""
    cal = api("https://api.github.com/graphql", {"query": q, "variables": {"u": USER}})
    cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]
    return dict(repos=len(own), stars=sum(r["stargazers_count"] for r in own), total=cal["totalContributions"],
                longest=longest, weeks=weeks, langs=sorted(langs.items(), key=lambda kv: -kv[1]))


class Text:
    """Text from pre-baked glyph outlines: each glyph defined once per page, then reused."""

    def __init__(self):
        self.fonts = json.load(open(os.path.join(HERE, "glyphs.json"), encoding="utf-8"))
        self.used = {}

    def width(self, s, font, size):
        f = self.fonts[font]
        return sum(f["glyphs"].get(ch, f["glyphs"]["?"])[0] for ch in s) * size / f["upem"]

    def __call__(self, s, font, size, x, y, fill=INK, anchor="start"):
        f = self.fonts[font]
        w = self.width(s, font, size)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        uses, cx = [], 0
        for ch in s:
            adv, d = f["glyphs"].get(ch, f["glyphs"]["?"])
            key = f"{font}-{ord(ch)}"
            if d:
                self.used[key] = d
                uses.append(f'<use href="#{key}" x="{cx}"/>')
            cx += adv
        return (f'<g fill="{fill}" transform="translate({x0:.1f} {y:.1f}) scale({size / f["upem"]:.5f})">'
                f'{"".join(uses)}</g>')

    def defs(self):
        return "".join(f'<path id="{k}" d="{d}"/>' for k, d in self.used.items())


def splitflap(T, x, y, value, css, n, cw=34, ch=50, size=34):
    out = []
    for i, c in enumerate(value):
        cx = x + i * (cw + 5)
        out.append(f'<rect x="{cx}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="#1f1d1a"/>')
        if c.isdigit():
            d = int(c)
            start = (d + 5) % 10
            spins = (d - start) % 10 + 10
            k = f"sf{n}x{i}"
            css.append(f"@keyframes {k}{{0%,100%{{transform:translateY(-{spins * ch}px)}}2%{{transform:translateY(0)}}"
                       f"22%{{transform:translateY(-{spins * ch}px)}}}}.{k}{{transform:translateY(-{spins * ch}px);"
                       f"animation:{k} 12s steps({spins},end) {1 + n * 0.5 + i * 0.15:.2f}s infinite}}")
            out.append(f'<clipPath id="c{k}"><rect x="{cx}" y="{y}" width="{cw}" height="{ch}"/></clipPath>'
                       f'<g clip-path="url(#c{k})"><g class="{k}">')
            for j in range(spins + 1):
                out.append(T(str((start + j) % 10), "mono", size, cx + cw / 2, y + ch * 0.73 + j * ch, "#f3ead6", "middle"))
            out.append("</g></g>")
        else:
            out.append(T(c, "mono", size, cx + cw / 2, y + ch * 0.73, "#f3ead6", "middle"))
        out.append(f'<rect x="{cx}" y="{y + ch / 2 - 0.6}" width="{cw}" height="1.2" fill="#000" opacity=".55"/>')
    return "".join(out)


def ring(cx, cy, rx, ry, css, seed=4):
    rng = random.Random(seed)
    pts = []
    for i in range(52):
        a = -2.4 + i / 46 * 6.283
        wob = 1 + rng.uniform(-0.04, 0.04)
        pts.append((cx + rx * wob * math.cos(a), cy + ry * wob * math.sin(a)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    css.append(f"@keyframes ring{{0%,100%{{stroke-dashoffset:0}}2%{{stroke-dashoffset:{length:.0f}}}"
               f"18%{{stroke-dashoffset:0}}}}.ring{{stroke-dasharray:{length:.0f};animation:ring 11s ease-in-out "
               f"2s infinite}}")
    return (f'<path class="ring" d="{d}" fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round" '
            f'opacity=".85"/>')


def render(s, today):
    T = Text()
    css = []
    bg = base64.b64encode(open(os.path.join(HERE, "markets_bg.jpg"), "rb").read()).decode()
    M = 44
    p = [f'<image href="data:image/jpeg;base64,{bg}" width="{W}" height="{H}" preserveAspectRatio="none"/>']
    p.append(f'<rect x="{M}" y="38" width="{W - 2 * M}" height="3" fill="{INK}"/>'
             f'<rect x="{M}" y="44" width="{W - 2 * M}" height="1" fill="{INK}"/>')
    p.append(T("Markets", "mast", 54, M, 100))
    p.append(T("THE LAST TWELVE MONTHS ON GITHUB", "body-bold", 14, W - M, 82, INK, "end"))
    p.append(T(f"redrawn every day · {today}", "body", 15, W - M, 102, GREY, "end"))
    p.append(f'<rect x="{M}" y="118" width="{W - 2 * M}" height="1" fill="{INK}"/>')
    # the board
    rows = [(f'{s["total"]:,}', "contributions"), (str(s["repos"]), "public repositories"),
            (str(s["stars"]), "stars earned"), (str(s["longest"]), "longest streak, days")]
    for n, (val, label) in enumerate(rows):
        y = 148 + n * 82
        p.append(splitflap(T, M, y, val, css, n))
        p.append(T(label, "body", 19, M + 5 * 39 + 16, y + 34))
    p.append(f'<rect x="530" y="140" width="1" height="330" fill="{INK}" opacity=".6"/>')
    # the chart: weekly contributions as bars, with a four-week average on top
    weeks = s["weeks"]
    top = max(weeks) or 1
    cx0, cx1, cy0, cy1 = 600, W - M, 170, 450
    p.append(T("CONTRIBUTIONS, WEEK BY WEEK", "body-bold", 14, cx0, 152))
    for k in range(5):
        v = top * k / 4
        y = cy1 - (cy1 - cy0) * k / 4
        p.append(f'<rect x="{cx0}" y="{y:.1f}" width="{cx1 - cx0}" height="{1 if k == 0 else 0.6}" fill="{INK}" '
                 f'opacity="{1 if k == 0 else 0.25}"/>')
        p.append(T(f"{v:.0f}", "mono", 12, cx0 - 8, y + 4, GREY, "end"))
    bw = (cx1 - cx0) / len(weeks)
    for i, c in enumerate(weeks):
        h = (cy1 - cy0) * c / top
        p.append(f'<rect x="{cx0 + i * bw + 1:.1f}" y="{cy1 - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" '
                 f'fill="{INK}" opacity=".78"/>')
    avg = [sum(weeks[max(0, i - 3):i + 1]) / len(weeks[max(0, i - 3):i + 1]) for i in range(len(weeks))]
    line = " ".join(f"{cx0 + (i + 0.5) * bw:.1f},{cy1 - (cy1 - cy0) * a / top:.1f}" for i, a in enumerate(avg))
    p.append(f'<polyline points="{line}" fill="none" stroke="{RED}" stroke-width="2.2"/>')
    b = max(range(len(weeks)), key=lambda i: weeks[i])
    bx, by = cx0 + (b + 0.5) * bw, cy1 - (cy1 - cy0) * weeks[b] / top
    p.append(ring(bx, by + 18, 30, 34, css))
    lx = min(max(bx, cx0 + 110), cx1 - 110)
    p.append(T(f"busiest week: {weeks[b]}", "body-bold", 15, lx, by - 26, RED, "middle"))
    p.append(T("bars: weekly contributions · red line: four-week average", "body", 14, cx0, cy1 + 24, GREY))
    # ticker: most used languages
    langs = [name for name, _ in s["langs"][:6]]
    items = ["MOST USED LANGUAGES: " + " · ".join(langs), f"{s['total']:,} CONTRIBUTIONS IN 12 MONTHS",
             f"LONGEST STREAK: {s['longest']} DAYS", "OPEN TO CONTRACT WORK: @AZAMINTIKHAB ON X"]
    sep = "   •   "
    tline = sep.join(items) + sep
    tw = T.width(tline, "mono", 17)
    css.append(f"@keyframes tick{{from{{transform:translateX(0)}}to{{transform:translateX(-{tw:.0f}px)}}}}"
               f".tick{{animation:tick {tw / 70:.1f}s linear infinite}}"
               "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}")
    ty = H - 44
    p.append(f'<rect x="0" y="{ty}" width="{W}" height="44" fill="#151412"/><clipPath id="tk"><rect x="96" y="{ty}" '
             f'width="{W - 96}" height="44"/></clipPath><g clip-path="url(#tk)"><g class="tick">'
             + T(tline + tline, "mono", 17, 112, ty + 29, "#efe6d2") + "</g></g>"
             f'<rect x="0" y="{ty}" width="96" height="44" fill="{RED}"/>'
             f'<circle cx="20" cy="{ty + 22}" r="5" fill="#fff" style="animation:pulse 1.4s ease-in-out infinite"/>'
             + T("LIVE", "body-bold", 17, 34, ty + 28, "#fff"))
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-labelledby="t d"><title id="t">Markets: GitHub activity of {USER}, last twelve months</title>'
            f'<desc id="d">{s["total"]} contributions, {s["repos"]} public repositories, {s["stars"]} stars, longest '
            f'streak {s["longest"]} days, busiest week {weeks[b]} contributions. Set as a newspaper market report.</desc>'
            f"<style>{''.join(css)}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>")
    return head + "".join(p) + f"<defs>{T.defs()}</defs></svg>\n"


def main():
    s = collect()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8") as fh:
        fh.write(render(s, dt.date.today().isoformat()))
    print(f"stats.svg: {s['total']} contributions, {s['repos']} repos, {s['stars']} stars, streak {s['longest']}")


if __name__ == "__main__":
    main()
