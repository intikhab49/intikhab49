"""Daily live-stats card from the GitHub API, in the same theme as art.py. Standard library only.

Env: GITHUB_TOKEN (the Actions token is enough), GH_USER (default intikhab49), OUT_DIR (default dist).
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import AMBER, BLUE, CARD, CORAL, EDGE, LIME, MUTED, PINK, TEXT, svg, x  # noqa: E402

USER = os.environ.get("GH_USER", "intikhab49")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = os.environ.get("OUT_DIR", "dist")


def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": USER,
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
        if r["language"]:
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
    weeks = [(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"])) for w in cal["weeks"]]
    return dict(repos=len(own), total=cal["totalContributions"], longest=longest,
                busiest=max(v for _, v in weeks) if weeks else 0, weeks=weeks,
                langs=sorted(langs.items(), key=lambda kv: -kv[1]))


def heat(f):
    return LIME if f < .25 else AMBER if f < .5 else CORAL if f < .75 else PINK


def render(s, today):
    W, H = 1200, 470
    tiles = [("PUBLIC REPOS", s["repos"], CORAL), ("CONTRIBUTIONS · 12 MO", s["total"], AMBER),
             ("LONGEST STREAK", f"{s['longest']} days", LIME), ("BUSIEST WEEK · CONTRIBUTIONS", s["busiest"], PINK)]
    out = [f'<text x="32" y="44" class="mono" font-size="12" font-weight="700" fill="{AMBER}">● LIVE GITHUB STATS</text>',
           f'<text x="1168" y="44" class="mono" font-size="11" fill="{MUTED}" text-anchor="end">UPDATED DAILY · {x(today)}</text>']
    for i, (k, v, c) in enumerate(tiles):
        tx = 32 + i * 288
        out.append(f'<rect x="{tx}" y="62" width="272" height="100" rx="14" fill="{CARD}" stroke="{EDGE}"/>'
                   f'<rect x="{tx}" y="62" width="4" height="100" rx="2" fill="{c}"/>'
                   f'<text x="{tx + 22}" y="90" class="mono" font-size="11" fill="{MUTED}">{x(k)}</text>'
                   f'<text x="{tx + 20}" y="142" class="sans" font-size="40" font-weight="800" fill="{c}">{x(v)}</text>')

    # 3D contribution skyline
    weeks = s["weeks"][-52:]
    peak = max((v for _, v in weeks), default=1) or 1
    bx, base, bw, gap, hmax = 44, 410, 10, 4.2, 170
    out.append(f'<text x="32" y="200" class="mono" font-size="11" fill="{MUTED}">WEEKLY CONTRIBUTIONS · LAST 12 MONTHS</text>'
               f'<path d="M{bx - 12} {base} L{bx + 52 * (bw + gap)} {base} l8 -6" fill="none" stroke="{EDGE}" stroke-width="1.5"/>')
    last_month = None
    for i, (date, v) in enumerate(weeks):
        px = bx + i * (bw + gap)
        h = max(3, v / peak * hmax)
        c = heat(v / peak)
        out.append(f'<g class="grow" style="animation-delay:{i * .02:.2f}s">'
                   f'<rect x="{px}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" fill="{c}" opacity="{.55 if v else .25}"/>'
                   f'<path d="M{px + bw} {base - h:.1f} l5 -4 v{h:.1f} l-5 4z" fill="{c}" opacity="{.3 if v else .12}"/>'
                   f'<path d="M{px} {base - h:.1f} l5 -4 h{bw} l-5 4z" fill="{c}" opacity="{.95 if v else .35}"/></g>')
        m = date[:7]
        if m != last_month:
            if last_month is not None and i < 51:
                out.append(f'<text x="{px}" y="{base + 22}" class="mono" font-size="10" fill="{MUTED}">{dt.date.fromisoformat(date).strftime("%b").upper()}</text>')
            last_month = m

    # language donut
    cx, cy, r = 930, 318, 72
    top = s["langs"][:5]
    total = sum(v for _, v in s["langs"]) or 1
    colors = [CORAL, AMBER, PINK, LIME, BLUE]
    out.append(f'<text x="850" y="200" class="mono" font-size="11" fill="{MUTED}">PRIMARY LANGUAGE · SHARE OF REPOS</text>'
               f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="22"/>')
    start = 0
    for (name, v), c in zip(top, colors):
        frac = v / total * 100
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="22" pathLength="100" '
                   f'stroke-dasharray="{max(frac - 1, .5):.1f} 100" stroke-dashoffset="{-start:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        start += frac
    if top:
        out.append(f'<text x="{cx}" y="{cy + 2}" class="sans" font-size="26" font-weight="800" fill="{TEXT}" text-anchor="middle">{100 * top[0][1] / total:.0f}%</text>'
                   f'<text x="{cx}" y="{cy + 22}" class="mono" font-size="10" fill="{MUTED}" text-anchor="middle">{x(top[0][0].upper())}</text>')
    for i, ((name, v), c) in enumerate(zip(top, colors)):
        ly = 262 + i * 26
        out.append(f'<rect x="1030" y="{ly - 10}" width="12" height="12" rx="3" fill="{c}"/>'
                   f'<text x="1050" y="{ly}" class="sans" font-size="13" fill="{TEXT}">{x({"Jupyter Notebook": "Jupyter"}.get(name, name))}</text>'
                   f'<text x="1168" y="{ly}" class="mono" font-size="11" fill="{MUTED}" text-anchor="end">{100 * v / total:.0f}%</text>')
    return svg(W, H, f"Live GitHub stats for {USER}: {s['repos']} public repos, {s['total']} contributions in the last 12 months, longest streak {s['longest']} days", "".join(out), blobs=False)


if __name__ == "__main__":
    s = collect()
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/stats.svg", "w", encoding="utf-8") as f:
        f.write(render(s, today))
    print(json.dumps({k: v for k, v in s.items() if k != "weeks"})[:300])
