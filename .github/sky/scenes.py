"""The scenes, as light fields for paint.repaint. Coordinates are fractions of the canvas."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from paint import hexrgb, mix, noise, smooth

C = {k: hexrgb(v) for k, v in {
    "zenith": "#050816", "high": "#0a1030", "mid": "#141c48", "low": "#262a5c", "horizon": "#3a2f5e",
    "warm": "#7a4a5a", "ember": "#b0705a", "airglow": "#1d4a4c",
    "core": "#f6e6c4", "peach": "#e9b58e", "rose": "#c98aa6", "cool": "#a9b9ec", "ice": "#d6e2ff",
    "dust": "#120c1a", "nebula": "#d0607e", "teal": "#4fb3b0",
    "far": "#1a1f45", "near": "#0b0d1f", "ink": "#04050c",
}.items()}


def band_frame(w, h, x0, y0, x1, y1, bend):
    """Coordinates along (s) and across (t) a gently curved band from (x0, y0) to (x1, y1)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xx, yy = xx / w, yy / h * (h / w)
    y0, y1 = y0 * h / w, y1 * h / w
    dx, dy = x1 - x0, y1 - y0
    L = np.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    s = ((xx - x0) * ux + (yy - y0) * uy) / L          # 0 at start, 1 at end
    t = (-(xx - x0) * uy + (yy - y0) * ux) / L         # signed distance across
    t = t - bend * (s - 0.5) ** 2 + bend * 0.25        # bow the band
    return s, t, np.arctan2(uy, ux)


def milky_way(w, h, seed, x0, y0, x1, y1, bend=0.18, width=0.075, core_at=0.12):
    """Light, colour and stroke direction of a Milky Way band, plus a star density map."""
    s, t, ang = band_frame(w, h, x0, y0, x1, y1, bend)
    n1 = noise(h, w, seed, 6, 5)
    n2 = noise(h, w, seed + 1, 5, 9)
    widen = 1 + 1.1 * np.exp(-((s - core_at) / 0.22) ** 2)            # fatter near the core
    across = t / (width * widen)
    glow = np.exp(-across ** 2) * (0.55 + 0.6 * n1)
    glow *= np.clip(1.15 - 0.55 * s, 0.25, 1)                          # fades away from the core
    # dust lanes: streaks that run along the band, cut into its middle
    lane_n = noise(h, w, seed + 2, 5, 7)
    lanes = np.exp(-((across - 0.15 + 0.5 * (lane_n - 0.5)) / 0.32) ** 2)
    lanes *= np.clip((lane_n - 0.35) * 2.4, 0, 1) * np.exp(-((s - 0.35) / 0.55) ** 2)
    glow = glow * (1 - 0.8 * lanes)
    clouds = noise(h, w, seed + 4, 6, 40, 0.6)
    glow = glow * (0.6 + 0.8 * clouds)
    core = np.exp(-((s - core_at) / 0.16) ** 2) * np.exp(-(across / 0.9) ** 2)
    col = mix(C["cool"][None, None], C["ice"][None, None], n2)
    col = mix(col, C["rose"], np.clip(core * 1.3, 0, 1) * 0.6)
    col = mix(col, C["peach"], np.clip(core * 1.6 - 0.2, 0, 1))
    col = mix(col, C["core"], np.clip(core * 2.0 - 0.8, 0, 1))
    # a few emission nebulae inside the band
    neb = np.zeros((h, w), np.float32)
    rng = np.random.default_rng(seed)
    for _ in range(4):
        cs, ct = rng.uniform(0.15, 0.75), rng.uniform(-0.6, 0.6)
        neb += np.exp(-(((s - cs) / 0.05) ** 2 + ((across - ct) / 0.6) ** 2)) * rng.uniform(0.4, 0.9)
    neb *= noise(h, w, seed + 3, 4, 12)
    density = 0.15 + glow * 2.5
    return glow, col, neb, density, np.full((h, w), ang, np.float32) + 0.25 * (n2 - 0.5)


def ridge(w, seed, base, amp, rough, octaves=6):
    """A mountain line: y (fraction of height) for every x."""
    rng = np.random.default_rng(seed)
    xs = np.linspace(0, 1, w)
    y = np.zeros(w)
    a, f = 1.0, 2.0
    for _ in range(octaves):
        knots = rng.random(int(f) + 2)
        y += a * np.interp(xs * (len(knots) - 1), np.arange(len(knots)), knots)
        a *= rough
        f *= 2.1
    y = (y - y.min()) / (y.max() - y.min())
    return base - amp * y


def hero(w, h, seed=7, quiet=(0.24, 0.20, 0.34, 0.20)):
    """Night mountain lake under a rising Milky Way. Returns (ref, angle, star_density, masks)."""
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
    xx = np.mgrid[0:h, 0:w][1].astype(np.float32) / w
    horizon = 0.70
    # sky: night gradient, warm glow low on the left where the core rises, airglow near the horizon
    v = np.clip(yy / horizon, 0, 1)
    sky = mix(C["zenith"][None, None], C["high"], np.clip(v * 1.6, 0, 1))
    sky = mix(sky, C["mid"], np.clip(v * 1.8 - 0.6, 0, 1))
    sky = mix(sky, C["low"], np.clip(v * 2.2 - 1.2, 0, 1))
    sky = mix(sky, C["horizon"], np.clip(v * 3.0 - 2.1, 0, 1))
    warm = np.exp(-(((xx - 0.16) / 0.30) ** 2 + ((yy - horizon) / 0.16) ** 2))
    sky = mix(sky, C["warm"], warm * 0.55)
    sky = mix(sky, C["ember"], warm ** 3 * 0.45)
    air = np.exp(-((yy - horizon + 0.07) / 0.05) ** 2) * (0.6 + 0.4 * noise(h, w, seed + 9, 3, 6))
    sky = mix(sky, C["airglow"], air * 0.35)
    sky *= (0.92 + 0.16 * noise(h, w, seed + 4, 4, 3))[..., None]   # uneven paint in the open sky
    glow, mcol, neb, density, mang = milky_way(w, h, seed, 0.10, 0.80, 0.98, -0.10)
    ref = sky + mcol * np.clip(glow, 0, 1.4)[..., None] * 0.62
    ref = mix(ref, C["nebula"], np.clip(neb * glow * 1.6, 0, 0.55))
    ref = np.clip(ref, 0, 1)
    angle = np.where(glow > 0.18, mang, 0.04 * np.sin(xx * 6) + 0.02 * (yy - 0.3))
    # a quieter, darker patch of sky where the title sits
    qx, qy, qw, qh = quiet
    hush = np.exp(-(((xx - qx) / qw) ** 2 + ((yy - qy) / qh) ** 2))
    ref = ref * (1 - 0.55 * hush)[..., None]
    density = density * (1 - 0.85 * hush)

    # mountains: a far, hazy range and a near, dark one
    far = ridge(w, seed + 20, horizon - 0.015, 0.16, 0.5)
    near = ridge(w, seed + 21, horizon + 0.005, 0.10, 0.55)
    near += 0.07 * np.exp(-((np.linspace(0, 1, w) - 0.86) / 0.12) ** 2) * -1   # a shoulder on the right
    far_mask = (yy >= far[None, :]) & (yy < horizon + 0.01)
    near_mask = (yy >= near[None, :]) & (yy < horizon + 0.01)
    fcol = mix(C["far"][None, None], C["horizon"], np.clip((yy - far[None, :]) * -6 + 0.35, 0, 0.35))
    ref = np.where(far_mask[..., None], fcol * (0.9 + 0.2 * noise(h, w, seed + 5, 4, 10))[..., None], ref)
    rim = np.exp(-((yy - near[None, :]) / 0.003) ** 2) * (warm * 0.6 + 0.12)
    ref = np.where(near_mask[..., None], C["near"] * (0.85 + 0.3 * noise(h, w, seed + 6, 5, 14))[..., None], ref)
    ref = ref + rim[..., None] * C["rose"] * 0.3
    angle = np.where(far_mask | near_mask, -0.35 + 0.7 * noise(h, w, seed + 7, 3, 8), angle)

    # lake: the sky above, mirrored, darker, cooler and smeared sideways by the water
    lake = yy >= horizon
    src = np.clip((2 * horizon - yy) * h, 0, h - 1).astype(int)
    mirror = ref[src, np.arange(w)[None, :]]
    mirror = smooth(mirror, 6)
    ripple = 0.75 + 0.25 * np.sin(yy * h * 0.9 + 8 * noise(h, w, seed + 8, 3, 6))
    depth = np.clip((yy - horizon) / (1 - horizon), 0, 1)
    water = mirror * (0.78 - 0.3 * depth)[..., None] * ripple[..., None]
    water = mix(water, C["ink"], depth * 0.35)
    ref = np.where(lake[..., None], water, ref)
    angle = np.where(lake, 0.0, angle)
    # the rock on the right shore, painted like everything else (dark, with sky light on its top edge)
    xs = np.linspace(0, 1, w)
    rise = np.clip((xs - 0.64) / 0.16, 0, 1)
    rock_top = horizon + 0.03 - 0.075 * (3 * rise ** 2 - 2 * rise ** 3)        # a smooth shoulder, no cliff
    rock_top -= 0.015 * np.clip((xs - 0.90) / 0.1, 0, 1)
    rock_top += 0.008 * (noise(1, w, seed + 30, 5, 30)[0] - 0.5)
    shore = horizon + 0.03 + np.clip((0.64 - xs) / 0.16, 0, 1) ** 1.4 * (1.02 - horizon)   # slopes into the water
    rock_top = np.where(xs < 0.64, shore, rock_top)
    rock = yy >= rock_top[None, :]
    rcol = C["ink"] * 1.6 * (0.8 + 0.5 * noise(h, w, seed + 31, 5, 16))[..., None]
    edge = np.exp(-((yy - rock_top[None, :]) / 0.006) ** 2)
    ref = np.where(rock[..., None], rcol + edge[..., None] * C["horizon"] * 0.5, ref)
    angle = np.where(rock, 0.6 + 0.6 * noise(h, w, seed + 32, 3, 9), angle)
    density = np.where(rock, 0, density)
    density = np.where(yy < horizon - 0.01, density, 0)
    density = np.where(far_mask | near_mask, 0, density)
    return np.clip(ref, 0, 1).astype(np.float32), angle.astype(np.float32), density.astype(np.float32), \
        dict(horizon=horizon, near=near, rock_top=rock_top)


def observer(img, rock_top, x_frac=0.80, seed=3):
    """Someone on the rock at a small refractor, leaning in, the tube pointed up at the core."""
    w, h = img.size
    d = ImageDraw.Draw(img)
    ink = (6, 7, 16)
    s = h / 760 * 1.25
    gx = x_frac * w
    gy = rock_top[int(gx)] * h + 1.5 * s

    def P(pts):
        return [(gx + x * s, gy + y * s) for x, y in pts]
    # person, facing left, one hand on the focuser
    d.polygon(P([(-8, 0), (-4.5, 0), (-2.5, -29), (0.5, -29), (2.5, 0), (6.5, 0), (6.5, -33), (9, -36), (10.5, -48),
                 (9.5, -58), (5, -63), (-3, -64), (-8, -61), (-11, -55), (-19, -55.5), (-20.5, -52.5), (-11, -48),
                 (-9.5, -36), (-7, -33)]), fill=ink)
    d.polygon(P([(-3, -63), (1, -63), (0.5, -67), (-2.5, -67)]), fill=ink)                   # neck
    d.ellipse([gx - 7.5 * s, gy - 76 * s, gx + 1.5 * s, gy - 66 * s], fill=ink)               # head, tipped back
    # tripod and tube
    head = (-34, -47)
    for fx in (-50, -33, -17):
        d.line(P([head, (fx, 0)]), fill=ink, width=max(2, int(2.6 * s)))
    e = np.radians(38)                                   # elevation, pointing up and to the left
    back = (-21, -55)
    front = (back[0] - 66 * np.cos(e), back[1] - 66 * np.sin(e))
    d.line(P([back, front]), fill=ink, width=int(8 * s))
    dew = (front[0] - 10 * np.cos(e), front[1] - 10 * np.sin(e))
    d.line(P([front, dew]), fill=ink, width=int(11 * s))
    d.line(P([head, ((back[0] + front[0]) / 2 + 6, (back[1] + front[1]) / 2 + 3)]), fill=ink, width=int(4 * s))
    d.line(P([(-21, -55), (-19.5, -53)]), fill=ink, width=int(4 * s))                        # eyepiece
    return img, (gx, gy)


def card(w, h, seed, hue, hue2):
    """A small patch of deep sky with one nebula on the right and a quiet left side for text."""
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
    xx = np.mgrid[0:h, 0:w][1].astype(np.float32) / w
    sky = mix(C["zenith"][None, None], C["high"], np.clip(yy * 1.2, 0, 1))
    sky = mix(sky, C["mid"], np.clip(xx * 0.8 - 0.1, 0, 0.6) * np.clip(yy + 0.3, 0, 1))
    sky *= (0.9 + 0.2 * noise(h, w, seed, 4, 3))[..., None]
    n = noise(h, w, seed + 1, 6, 5)
    n2 = noise(h, w, seed + 2, 5, 11)
    cloud = np.exp(-(((xx - 0.74) / 0.30) ** 2 + ((yy - 0.48) / 0.42) ** 2)) * np.clip(n * 1.6 - 0.35, 0, 1)
    col = mix(hexrgb(hue)[None, None], hexrgb(hue2), n2)
    ref = sky + col * cloud[..., None] * 0.75
    lanes = np.clip((noise(h, w, seed + 3, 5, 8) - 0.55) * 3, 0, 1) * cloud
    ref = ref * (1 - 0.5 * lanes)[..., None]
    hush = np.exp(-(((xx - 0.18) / 0.38) ** 2 + ((yy - 0.55) / 0.55) ** 2))
    ref = ref * (1 - 0.35 * hush)[..., None]
    angle = 0.5 * (n2 - 0.5) + np.where(cloud > 0.1, 0.7 * (n - 0.5), 0.0)
    density = 0.2 + cloud * 3 - hush * 0.15
    return np.clip(ref, 0, 1).astype(np.float32), angle.astype(np.float32), np.clip(density, 0.02, None).astype(np.float32)
