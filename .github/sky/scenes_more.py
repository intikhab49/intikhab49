"""More scenes: a plain strip of sky, painted planets, and the sky just before dawn."""
import numpy as np

from paint import hexrgb, mix, noise
from scenes import C, ridge


def sky_strip(w, h, seed, lift=0.0):
    """Plain deep sky for strips, with a faint band of light across it."""
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
    xx = np.mgrid[0:h, 0:w][1].astype(np.float32) / w
    sky = mix(C["zenith"][None, None], C["high"], np.clip(yy * 1.1 + lift, 0, 1))
    sky *= (0.88 + 0.24 * noise(h, w, seed, 4, 3))[..., None]
    band = np.exp(-((yy - 0.25 - 0.5 * xx) / 0.22) ** 2) * noise(h, w, seed + 1, 6, 6)
    sky = sky + C["cool"] * band[..., None] * 0.14
    angle = 0.3 * (noise(h, w, seed + 2, 3, 5) - 0.5)
    return np.clip(sky, 0, 1).astype(np.float32), angle.astype(np.float32), (0.3 + band).astype(np.float32)


def planet(ref, angle, dens, cx, cy, r, seed, cols, bands=6, tilt=0.15, ring=False):
    """Paint a lit sphere with latitude bands into ref (in place). cols: dark, mid, light hex."""
    h, w, _ = ref.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (xx - cx) / r, (yy - cy) / r
    rr = dx * dx + dy * dy
    disk = rr <= 1
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    lat = dy * np.cos(tilt) + dx * np.sin(tilt)
    n = noise(h, w, seed, 6, 14)
    n2 = noise(h, w, seed + 50, 5, 30)
    warp = 7.0 * (n - 0.5) + 2.5 * (n2 - 0.5)
    stripes = 0.5 + 0.5 * np.sin(lat * bands * np.pi + warp + seed) * (0.55 + 0.45 * np.sin(lat * bands * 2.3 + seed))
    dark, midc, light = (hexrgb(c) for c in cols)
    tex = mix(mix(dark[None, None], midc, np.clip(0.35 + stripes * 0.9, 0, 1)), light, np.clip(stripes * 1.3 - 0.85, 0, 0.6))
    lit = np.clip(0.06 + 1.05 * np.clip(-0.6 * dx - 0.5 * dy + 0.62 * z, 0, 1) ** 1.25, 0, 1.1)
    body = tex * lit[..., None]
    rim = np.exp(-((np.sqrt(rr) - 1.0) / 0.06) ** 2) * np.clip(-dx * 0.7 - dy * 0.5 + 0.4, 0, 1)
    ref[:] = np.where(disk[..., None], body, ref)
    ref[:] = ref + (light * 0.8)[None, None] * rim[..., None] * 0.6
    angle[:] = np.where(disk, tilt + 0.2 * (n - 0.5), angle)
    dens[:] = np.where(rr < 1.3, 0.0, dens)
    if ring:
        ex = dx * np.cos(-0.35) - dy * np.sin(-0.35)
        ey = dx * np.sin(-0.35) + dy * np.cos(-0.35)
        e = np.sqrt((ex / 1.9) ** 2 + (ey / 0.42) ** 2)
        band = np.exp(-((e - 0.86) / 0.07) ** 2) * (0.6 + 0.4 * np.sin(e * 90))
        front = (ey > 0) | ~disk
        show = (band > 0.05) & front
        ref[:] = np.where(show[..., None], mix(ref, light * 0.9, np.clip(band, 0, 0.85)), ref)


def dawn(w, h, seed):
    """The sky just before sunrise: night overhead, a warm band low down, hills in front."""
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
    xx = np.mgrid[0:h, 0:w][1].astype(np.float32) / w
    t = np.clip(yy / 0.78, 0, 1)
    sky = mix(C["zenith"][None, None], C["mid"], np.clip(t * 1.5, 0, 1))
    sky = mix(sky, hexrgb("#5a3f78"), np.clip(t * 2.2 - 1.0, 0, 1))
    sky = mix(sky, hexrgb("#c46a6a"), np.clip(t * 3.4 - 2.3, 0, 1))
    sky = mix(sky, hexrgb("#f0b070"), np.clip(t * 5 - 4.1, 0, 1) * np.exp(-((xx - 0.5) / 0.45) ** 2))
    sky *= (0.92 + 0.16 * noise(h, w, seed, 4, 4))[..., None]
    clouds = np.clip(noise(h, w, seed + 1, 6, 7) * 1.5 - 0.75, 0, 1) * np.exp(-((yy - 0.62) / 0.12) ** 2)
    sky = mix(sky, hexrgb("#2a1f3e"), clouds * 0.8)
    sky = sky + hexrgb("#f6b49a") * (np.exp(-((yy - 0.6) / 0.03) ** 2) * clouds * 0.6)[..., None]
    hills = ridge(w, seed + 3, 0.92, 0.16, 0.5)
    land = yy >= hills[None, :]
    ref = np.where(land[..., None], C["near"] * (0.8 + 0.3 * noise(h, w, seed + 4, 4, 12))[..., None], sky)
    angle = np.where(land, 0.3 * (noise(h, w, seed + 5, 3, 8) - 0.5), 0.02 + 0.1 * (noise(h, w, seed + 6, 3, 4) - 0.5))
    density = np.where(land, 0, np.clip(1 - t * 1.6, 0, 1))
    return np.clip(ref, 0, 1).astype(np.float32), angle.astype(np.float32), density.astype(np.float32)
