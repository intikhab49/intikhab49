"""Build the daily "field log" stats card from the GitHub API. Standard library only.

Env: GITHUB_TOKEN (the Actions token is enough), GH_USER (default intikhab49), OUT_DIR (default dist).
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from theme import THEMES, corners, frame, grid, x  # noqa: E402

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
    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)).isoformat()
    q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
           totalContributions weeks{contributionDays{contributionCount date}}}}}}"""
    cal = api("https://api.github.com/graphql", {"query": q, "variables": {"u": USER}})
    cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    return dict(repos=len(own), active=sum(r["pushed_at"] >= cutoff[:19] for r in own),
                total=cal["totalContributions"], longest=longest,
                weeks=[(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"]))
                       for w in cal["weeks"]],
                langs=sorted(langs.items(), key=lambda kv: -kv[1]))


def render(t, s, today):
    W, H = 1200, 380
    stats = [("PUBLIC REPOS", s["repos"]), ("UPDATED · 90 DAYS", s["active"]),
             ("CONTRIBUTIONS · 12 MO", s["total"]), ("LONGEST STREAK", f"{s['longest']}d")]
    blocks = "".join(
        f'<text x="{56 + (i % 2) * 190}" y="{110 + (i // 2) * 104}" class="mono" font-size="11">{x(k)}</text>'
        f'<text x="{54 + (i % 2) * 190}" y="{160 + (i // 2) * 104}" class="serif" font-size="46">{x(v)}</text>'
        for i, (k, v) in enumerate(stats))

    # seismograph of weekly contributions
    gx, gy, gw, gh = 470, 84, 674, 176
    vals = [v for _, v in s["weeks"]] or [0]
    peak = max(vals) or 1
    step = gw / max(len(vals) - 1, 1)
    pts = [(gx + i * step, gy + gh - (v / peak) * (gh - 12)) for i, v in enumerate(vals)]
    line = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    area = f"{line} L{gx + gw:.1f} {gy + gh} L{gx} {gy + gh} Z"
    months, last = [], None
    for i, (date, _) in enumerate(s["weeks"]):
        m = date[:7]
        if m != last and i % 1 == 0:
            if last is not None and i < len(s["weeks"]) - 2:
                months.append(f'<text x="{gx + i * step:.1f}" y="{gy + gh + 22}" class="mono" font-size="10">'
                              f'{dt.date.fromisoformat(date).strftime("%b").upper()}</text>')
            last = m
    seis = (f'<text x="{gx}" y="64" class="mono" font-size="11">WEEKLY ACTIVITY · PEAK {peak}</text>'
            f'<line x1="{gx}" y1="{gy + gh}" x2="{gx + gw}" y2="{gy + gh}" stroke="{t["rule"]}"/>'
            f'<path d="{area}" fill="{t["signal"]}" opacity="0.10"/>'
            f'<path d="{line}" pathLength="1" class="draw" fill="none" stroke="{t["signal"]}" stroke-width="1.8" stroke-linejoin="round"/>'
            + "".join(months))

    # language bar
    top = s["langs"][:6]
    total = sum(v for _, v in s["langs"]) or 1
    shades = [t["signal"], t["sage"], t["text"], t["muted"], t["rule"], t["faint"]]
    bx, by, bw = 56, 322, 1088
    cur, bars, labels = bx, [], []
    for i, (name, v) in enumerate(top):
        w = bw * v / total
        bars.append(f'<rect x="{cur:.1f}" y="{by}" width="{max(w - 2, 1):.1f}" height="8" fill="{shades[i]}"/>')
        cur += w
    lx = bx
    for i, (name, v) in enumerate(top):
        label = f"{name} {100 * v / total:.0f}%"
        labels.append(f'<rect x="{lx}" y="{by + 22}" width="8" height="8" fill="{shades[i]}" stroke="{t["rule"]}"/>'
                      f'<text x="{lx + 14}" y="{by + 30}" class="mono" font-size="11">{x(label.upper())}</text>')
        lx += 14 + len(label) * 8.6 + 26
    langs = (f'<text x="{bx}" y="{by - 14}" class="mono" font-size="11">PRIMARY LANGUAGE · SHARE OF REPOS</text>'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="8" fill="{t["faint"]}"/>' + "".join(bars) + "".join(labels))

    body = (f"{grid(t, 'fg')}<rect width='{W}' height='{H}' rx='14' fill='url(#fg)'/>{corners(t, W, H)}"
            f'<text x="56" y="48" class="mono" font-size="12">FIELD LOG · <tspan class="sig">LIVE</tspan></text>'
            f'<text x="1144" y="48" class="mono" font-size="11" text-anchor="end">UPDATED {x(today)} UTC</text>'
            f"{blocks}{seis}{langs}")
    return frame(t, W, H, f"GitHub activity for {USER}: {s['repos']} public repos, {s['total']} contributions in the last year", body)


if __name__ == "__main__":
    s = collect()
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(OUT, exist_ok=True)
    for mode, t in THEMES.items():
        with open(f"{OUT}/field-log-{mode}.svg", "w", encoding="utf-8") as f:
            f.write(render(t, s, today))
    print(json.dumps({k: v for k, v in s.items() if k != "weeks"})[:400])
