"""The daily stats card: the last twelve months as a constellation, one star per week. Standard library only.

The painted background (stats_bg.jpg) and the glyph outlines (glyphs.json) are made by build.py.
Env: GITHUB_TOKEN, GH_USER (default intikhab49), OUT_DIR (default dist). Writes OUT_DIR/stats.svg.
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
W, H = 1280, 470
CREAM, GOLD, MIST, DIM = "#f4ead2", "#e8c98e", "#c9d3ec", "#9aa6c8"


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
    """Text from pre-baked glyph outlines: each glyph defined once, then reused."""

    def __init__(self):
        self.fonts = json.load(open(os.path.join(HERE, "glyphs.json"), encoding="utf-8"))
        self.used, self.n = {}, 0

    def width(self, s, font, size):
        f = self.fonts[font]
        return sum(f["glyphs"].get(ch, f["glyphs"]["?"])[0] for ch in s) * size / f["upem"]

    def __call__(self, s, font, size, x, y, fill, anchor="start", glow="#070a1e"):
        f = self.fonts[font]
        w = self.width(s, font, size)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        uses, cx = [], 0
        for ch in s:
            adv, d = f["glyphs"].get(ch, f["glyphs"]["?"])
            key = f"{font[0]}{ord(ch)}"
            if d:
                self.used[key] = d
                uses.append(f'<use href="#{key}" x="{cx}"/>')
            cx += adv
        self.n += 1
        body = (f'<g id="x{self.n}" transform="translate({x0:.1f} {y:.1f}) scale({size / f["upem"]:.5f})">'
                f'{"".join(uses)}</g>')
        halo = f'<use href="#x{self.n}" fill="{glow}" filter="url(#soft)" opacity=".75"/>' if glow else ""
        return f'{halo}<g fill="{fill}">{body}</g>'

    def defs(self):
        return "".join(f'<path id="{k}" d="{d}"/>' for k, d in self.used.items())


def render(s, today):
    T = Text()
    bg = base64.b64encode(open(os.path.join(HERE, "stats_bg.jpg"), "rb").read()).decode()
    weeks = s["weeks"]
    top = max(weeks) or 1
    rng = random.Random(len(weeks) + top)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-labelledby="t d"><title id="t">GitHub activity of {USER}, last twelve months</title>'
         f'<desc id="d">{s["total"]} contributions, {s["repos"]} public repositories, {s["stars"]} stars, longest '
         f'streak {s["longest"]} days. Each week is a star; the busier the week, the higher and brighter.</desc>',
         "<style>@keyframes tw{0%,100%{opacity:.2}50%{opacity:1}}"
         "@keyframes draw{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:0}}"
         "@keyframes glint{0%,100%{stroke-opacity:.25}50%{stroke-opacity:.6}}.glint{animation:glint ease-in-out infinite}"
         ".tw{animation:tw ease-in-out infinite}"
         "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>",
         '<defs><radialGradient id="sg"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff6e8" '
         'stop-opacity=".9"/><stop offset="1" stop-color="#cfd9ff" stop-opacity="0"/></radialGradient>'
         '<filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter></defs>',
         f'<image href="data:image/jpeg;base64,{bg}" width="{W}" height="{H}" preserveAspectRatio="none"/>']
    p.append(T("The last twelve months", "display", 42, 60, 78, CREAM))
    p.append(T(f"redrawn every day · {today}", "mono", 16, W - 60, 74, GOLD, "end"))
    stats = [(f'{s["total"]:,}', "contributions"), (str(s["repos"]), "public repositories"),
             (str(s["stars"]), "stars"), (str(s["longest"]), "longest streak, days")]
    for i, (num, label) in enumerate(stats):
        x = 60 + i * 300
        p.append(T(num, "display", 66, x, 172, CREAM))
        p.append(T(label, "serif", 21, x + 2, 204, MIST))
    # the year: one star per week, left to right
    x0, x1, base, rise = 80, W - 80, 420, 150
    pts = []
    for i, c in enumerate(weeks):
        f = math.sqrt(c / top)
        pts.append((x0 + (x1 - x0) * i / max(1, len(weeks) - 1), base - rise * f, f, c))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in pts)
    length = sum(math.dist(a[:2], b[:2]) for a, b in zip(pts, pts[1:]))
    p.append(f'<polyline points="{line}" fill="none" stroke="#dfe6ff" stroke-opacity=".35" stroke-width="1.2" '
             f'class="glint" style="animation-duration:6s"/>')
    for i, (x, y, f, c) in enumerate(pts):
        if c == 0:
            p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.3" fill="#8b95b8"/>')
            continue
        r = 1.6 + 4.2 * f
        dur = rng.uniform(2.5, 6)
        p.append(f'<g><circle class="tw" cx="{x:.1f}" cy="{y:.1f}" '
                 f'r="{r * 3:.1f}" fill="url(#sg)" style="animation-duration:{dur:.1f}s"/><circle cx="{x:.1f}" '
                 f'cy="{y:.1f}" r="{r * 0.45:.1f}" fill="#fff"/></g>')
    busiest = max(range(len(weeks)), key=lambda i: weeks[i])
    bx, by = pts[busiest][:2]
    p.append(T(f"busiest week: {weeks[busiest]}", "serif", 18, min(max(bx, 140), W - 140), by - 26, GOLD, "middle"))
    langs = " · ".join(name for name, _ in s["langs"][:5])
    p.append(T("each star is one week; the higher and brighter, the busier", "serif", 18, 60, 455, DIM))
    if langs:
        p.append(T(langs, "mono", 15, W - 60, 455, GOLD, "end"))
    p.append(f"<defs>{T.defs()}</defs></svg>\n")
    return "".join(p)


def main():
    s = collect()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8") as fh:
        fh.write(render(s, dt.date.today().isoformat()))
    print(f"stats.svg: {s['total']} contributions, {s['repos']} repos, {s['stars']} stars, streak {s['longest']}")


if __name__ == "__main__":
    main()
