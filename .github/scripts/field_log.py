"""Daily live-stats card, painted as a truck dashboard. Standard library only.

Glyph outlines, the reflective-tape pattern and the mini truck come pre-baked in truck_glyphs.json
(regenerate with build_art.py). Env: GITHUB_TOKEN, GH_USER (default intikhab49), OUT_DIR (default dist).
"""
import datetime as dt
import json
import math
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
USER = os.environ.get("GH_USER", "intikhab49")
OUT = os.environ.get("OUT_DIR", "dist")
ART = json.load(open(os.path.join(HERE, "truck_glyphs.json"), encoding="utf-8"))

INK, NIGHT, GOLD, WHITE = "#120d0a", "#0d0b16", "#f2c14e", "#ffffff"
RED, GREEN, BLUE, PINK, TEAL, ORANGE, PURPLE, SAFFRON = ("#e0262b", "#1fa34a", "#1f4fd8", "#ff3e8a", "#16b3c4",
                                                          "#ff6a00", "#6a2bb8", "#ffb400")
W, H = 1280, 572


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
    return dict(repos=len(own), stars=sum(r["stargazers_count"] for r in own), total=cal["totalContributions"],
                longest=longest, busiest=max(v for _, v in weeks) if weeks else 0, weeks=weeks,
                langs=sorted(langs.items(), key=lambda kv: -kv[1]))


# ---------------------------------------------------------------- tiny text-as-paths engine
class Canvas:
    def __init__(self):
        self.defs, self.body, self.used = [], [], set()

    def width(self, font, s, size, ls=0.0):
        f = ART["fonts"][font]
        adv = sum(f["glyphs"].get(ch, f["glyphs"][" "])[0] for ch in s)
        return adv * size / f["upem"] + ls * size * max(0, len(s) - 1)

    def text(self, font, s, x, y, size, fill=INK, anchor="start", ls=0.0, outline=None, ow=3.0):
        f = ART["fonts"][font]
        k = size / f["upem"]
        w = self.width(font, s, size, ls)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        uses, pen = [], 0.0
        for ch in s:
            adv, d = f["glyphs"].get(ch, f["glyphs"][" "])
            if d:
                gid = f"{font}{ord(ch)}"
                if gid not in self.used:
                    self.used.add(gid)
                    self.defs.append(f'<path id="{gid}" d="{d}"/>')
                uses.append(f'<use href="#{gid}" x="{pen:.0f}"/>')
            pen += adv + ls * size / k
        g = f'<g transform="translate({x0:.1f} {y:.1f}) scale({k:.5f})">{"".join(uses)}</g>'
        if outline:
            self.body.append(f'<g fill="{outline}" stroke="{outline}" stroke-width="{ow / k:.0f}" stroke-linejoin="round">{g}</g>')
        self.body.append(f'<g fill="{fill}">{g}</g>')

    def add(self, *s):
        self.body.extend(s)


def nice_ceil(v):
    if v <= 10:
        return 10
    m = 10 ** int(math.log10(v))
    for step in (1, 2, 2.5, 5, 10):
        if v <= step * m:
            return int(step * m)
    return int(10 * m)


def smooth(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


def render(s, today):
    c = Canvas()
    css = ("@keyframes roll{to{transform:translateY(var(--y))}}"
           "@keyframes needle{from{transform:rotate(-120deg)}to{transform:rotate(var(--a))}}"
           "@keyframes flutter{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}"
           "@keyframes twinkle{0%,100%{opacity:.2}50%{opacity:1}}"
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    c.defs.append(ART["tape"])
    c.defs.append('<linearGradient id="mtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a3fd0"/><stop offset="1" stop-color="#1b1f6b"/></linearGradient>'
                  '<linearGradient id="dial" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2150"/><stop offset="1" stop-color="#141030"/></linearGradient>'
                  '<linearGradient id="chr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#9aa6b4"/><stop offset="1" stop-color="#e9eef3"/></linearGradient>')
    c.add(f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="24" fill="{INK}"/>'
          f'<rect x="9" y="9" width="{W - 18}" height="{H - 18}" rx="20" fill="url(#tp)"/>'
          f'<rect x="25" y="25" width="{W - 50}" height="{H - 50}" rx="12" fill="{INK}"/>'
          f'<rect x="28" y="28" width="{W - 56}" height="{H - 56}" rx="10" fill="{NIGHT}"/>')
    # ---- bunting: languages by number of repos
    x0, x1, sag, top = 60, W - 60, 22, 46
    c.add(f'<path d="M{x0} {top}Q{W / 2} {top + sag * 2} {x1} {top}" fill="none" stroke="#c9d1db" stroke-width="2.5"/>')
    langs = [{"Jupyter Notebook": "Jupyter"}.get(name, name) for name, _ in s["langs"][:7]]
    cols = [RED, SAFFRON, GREEN, PINK, TEAL, ORANGE, BLUE, PURPLE]
    nflags = 15
    li = 0
    for i in range(nflags):
        t = (i + 0.5) / nflags
        fx = x0 + (x1 - x0) * t
        fy = top + sag * 2 * 2 * t * (1 - t)
        labeled = i % 2 == 1 and li < len(langs)
        fw = 112 if labeled else 44
        fh = 62 if labeled else 40
        col = cols[i % len(cols)]
        flag = (f'<path d="M{fx - fw / 2:.1f} {fy:.1f}L{fx + fw / 2:.1f} {fy:.1f}L{fx:.1f} {fy + fh:.1f}Z" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M{fx - fw / 2 + 8:.1f} {fy + 5:.1f}L{fx + fw / 2 - 8:.1f} {fy + 5:.1f}" stroke="#fff" stroke-width="2" stroke-dasharray="2 5" opacity=".8"/>')
        c.add(f'<g style="transform-origin:{fx:.1f}px {fy:.1f}px;animation:flutter {2.4 + (i % 3) * 0.3:.1f}s ease-in-out {-i * 0.3:.1f}s infinite">{flag}</g>')
        if labeled:
            size = 19
            while c.width("tekob", langs[li], size) > fw - 26:
                size -= 0.5
            c.text("tekob", langs[li], fx, fy + 24, size, fill=WHITE, anchor="middle", outline=INK, ow=4)
            li += 1
    # ---- odometer
    c.text("tekob", "CONTRIBUTIONS · LAST 12 MONTHS", 70, 158, 24, fill=GOLD, ls=0.04)
    digits = str(s["total"])
    cw, ch_, gap = 66, 92, 8
    ox, oy = 70, 172
    c.add(f'<rect x="{ox - 12}" y="{oy - 12}" width="{len(digits) * (cw + gap) - gap + 24}" height="{ch_ + 24}" rx="12" fill="url(#chr)" stroke="{INK}" stroke-width="4"/>')
    for i, dg in enumerate(digits):
        wx = ox + i * (cw + gap)
        last = i == len(digits) - 1
        c.defs.append(f'<clipPath id="w{i}"><rect x="{wx}" y="{oy}" width="{cw}" height="{ch_}" rx="6"/></clipPath>')
        c.add(f'<rect x="{wx}" y="{oy}" width="{cw}" height="{ch_}" rx="6" fill="{RED if last else "#1b1634"}" stroke="{INK}" stroke-width="3"/>')
        strip_canvas = Canvas()
        strip_canvas.used = c.used
        target = int(dg)
        seq = list(range(10)) + list(range(target + 1))
        for k, v in enumerate(seq):
            strip_canvas.text("tekob", str(v), wx + cw / 2, oy + 74 + k * ch_, 80, fill=WHITE, anchor="middle")
        c.defs.extend(strip_canvas.defs)
        c.add(f'<g clip-path="url(#w{i})"><g style="--y:-{(len(seq) - 1) * ch_}px;animation:roll {2.2 + i * 0.25:.2f}s cubic-bezier(.2,.7,.2,1) forwards">'
              f'{"".join(strip_canvas.body)}</g></g>'
              f'<path d="M{wx + 4} {oy + 8}H{wx + cw - 4}" stroke="#fff" stroke-width="3" opacity=".25"/>')
    # ---- gauges
    dials = [("PUBLIC REPOS", s["repos"], nice_ceil(s["repos"] * 1.25), GREEN),
             ("STARS EARNED", s["stars"], nice_ceil(max(10, s["stars"]) * 1.25), SAFFRON),
             ("LONGEST STREAK", s["longest"], nice_ceil(max(10, s["longest"]) * 1.25), PINK)]
    for i, (label, val, mx, col) in enumerate(dials):
        cx, cy, r = 700 + i * 190, 222, 74
        c.add(f'<circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="url(#chr)" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#dial)" stroke="{INK}" stroke-width="3"/>')
        for k in range(13):
            a = math.radians(-210 + k * 20)
            r0 = r - (14 if k % 3 == 0 else 9)
            c.add(f'<path d="M{cx + r0 * math.cos(a):.1f} {cy + r0 * math.sin(a):.1f}L{cx + (r - 4) * math.cos(a):.1f} {cy + (r - 4) * math.sin(a):.1f}" '
                  f'stroke="{col if k < 10 else RED}" stroke-width="{3.5 if k % 3 == 0 else 2}" stroke-linecap="round"/>')
        ang = -120 + 240 * min(1.0, val / mx)
        c.add(f'<g style="--a:{ang:.1f}deg;transform-origin:{cx}px {cy}px;transform:rotate({ang:.1f}deg);animation:needle 2.2s cubic-bezier(.2,.8,.2,1) both">'
              f'<path d="M{cx - 5} {cy}L{cx} {cy - r + 14}L{cx + 5} {cy}Z" fill="{RED}" stroke="{INK}" stroke-width="2"/></g>'
              f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="4" fill="{GOLD}"/>')
        c.text("tekob", str(val), cx, cy + 50, 40, fill=WHITE, anchor="middle")
        c.text("tekob", label, cx, cy + r + 34, 20, fill=GOLD, anchor="middle", ls=0.04)
    # ---- mountain range of weekly contributions, with a truck on the ridge
    weeks = s["weeks"][-53:]
    mx = max(1, max(v for _, v in weeks))
    mx0, mx1, base, hmax = 60, W - 60, 512, 112
    pts = [(mx0 + (mx1 - mx0) * i / (len(weeks) - 1), base - 14 - hmax * (v / mx) ** 0.55) for i, (_, v) in enumerate(weeks)]
    ridge = smooth(pts)
    c.defs.append(f'<clipPath id="snow"><rect x="0" y="0" width="{W}" height="{base - 14 - hmax * 0.62:.1f}"/></clipPath>')
    for i in range(16):
        sx = 80 + (i * 197) % (W - 160)
        sy = 345 + (i * 53) % 50
        c.add(f'<circle cx="{sx}" cy="{sy}" r="{1.5 + i % 3}" fill="#fff" style="animation:twinkle {2 + i % 4 * 0.5:.1f}s ease-in-out {-i * 0.4:.1f}s infinite"/>')
    area = f"{ridge}L{mx1} {base}L{mx0} {base}Z"
    c.add(f'<path d="{area}" fill="url(#mtn)" stroke="{INK}" stroke-width="3"/>'
          f'<path d="{area}" fill="#f4f1ff" clip-path="url(#snow)"/>'
          f'<path d="{ridge}" fill="none" stroke="{INK}" stroke-width="3"/>')
    peak = max(range(len(pts)), key=lambda i: -pts[i][1])
    px, py = pts[peak]
    c.add(f'<path d="M{px:.1f} {py:.1f}V{py - 34:.1f}" stroke="{INK}" stroke-width="3"/>'
          f'<path d="M{px:.1f} {py - 34:.1f}L{px + 30:.1f} {py - 27:.1f}L{px:.1f} {py - 20:.1f}Z" fill="{RED}" stroke="{INK}" stroke-width="2"/>')
    c.text("tekob", f"BUSIEST WEEK: {s['busiest']}", px + (36 if px < W - 260 else -6), py - 24, 18, fill=WHITE,
           anchor="start" if px < W - 260 else "end", outline=INK, ow=4)
    last_m = None
    for i, (day, _) in enumerate(weeks):
        m = day[5:7]
        if m != last_m and i > 0:
            name = dt.date(int(day[:4]), int(m), 1).strftime("%b").upper()
            c.text("tekob", name, pts[i][0], base + 24, 16, fill="#b9b2d6", anchor="middle")
        last_m = m
    c.add(f'<g><g transform="translate(-22 2) scale(.62)">{ART["truck"]}</g>'
          f'<animateMotion dur="22s" repeatCount="indefinite" rotate="auto" path="{ridge}"/></g>')
    c.text("pop", f"Painted daily by this repo's own GitHub Action · {today}", 70, 312, 15, fill="#8f88b5")
    alt = (f"Live GitHub stats for {USER}: {s['total']} contributions in the last 12 months, {s['repos']} public repos, "
           f"{s['stars']} stars, longest streak {s['longest']} days, busiest week {s['busiest']} contributions")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{alt}">'
            f'<title>{alt}</title><style>{css}</style><defs>{"".join(c.defs)}</defs>{"".join(c.body)}</svg>')


if __name__ == "__main__":
    s = collect()
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/stats.svg", "w", encoding="utf-8") as f:
        f.write(render(s, today))
    print(json.dumps({k: v for k, v in s.items() if k != "weeks"})[:300])
