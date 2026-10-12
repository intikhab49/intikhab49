"""A small painting engine: build a soft light field for a scene, then repaint it with brush strokes.

Strokes go from big to small. The small brushes only touch places where the canvas still differs
from the reference, so open sky keeps its broad strokes and the Milky Way gets the fine ones.
Every function takes a seed, so the same build makes the same painting.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def noise(h, w, seed, octaves=5, base=4, persistence=0.55):
    """Fractal value noise in [0, 1], shape (h, w)."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        cells = base * 2 ** o
        gh, gw = max(2, int(cells * h / max(h, w)) + 2), max(2, int(cells * w / max(h, w)) + 2)
        grid = Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8))
        out += amp * np.asarray(grid.resize((w, h), Image.BICUBIC), np.float32) / 255.0
        total += amp
        amp *= persistence
    out /= total
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def smooth(a, radius):
    """Gaussian blur of a float field (h, w) or (h, w, 3)."""
    if a.ndim == 2:
        im = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
        return np.asarray(im.filter(ImageFilter.GaussianBlur(radius)), np.float32) / 255.0
    return np.stack([smooth(a[..., c], radius) for c in range(a.shape[2])], -1)


def mix(a, b, t):
    t = t[..., None] if np.ndim(t) == 2 else t
    return a * (1 - t) + b * t


_UNIT = np.stack([np.cos(np.linspace(0, 2 * np.pi, 14, endpoint=False)),
                  np.sin(np.linspace(0, 2 * np.pi, 14, endpoint=False))], 1)


def repaint(ref, angle, seed, passes=((26, 0.0), (13, 0.035), (6.5, 0.03), (3.2, 0.028)), jitter=0.035,
            stretch=(2.0, 3.4)):
    """Paint `ref` (h, w, 3 floats) with oriented elliptical strokes. `angle` (h, w) is the stroke
    direction in radians. Returns an RGB PIL image."""
    rng = np.random.default_rng(seed)
    h, w, _ = ref.shape
    canvas = Image.fromarray(np.clip(smooth(ref, 30) * 255, 0, 255).astype(np.uint8))
    for radius, threshold in passes:
        step = radius * 0.85
        ys, xs = np.mgrid[0:h:step, 0:w:step]
        ys = (ys + rng.uniform(-step / 2, step / 2, ys.shape)).clip(0, h - 1).astype(int).ravel()
        xs = (xs + rng.uniform(-step / 2, step / 2, xs.shape)).clip(0, w - 1).astype(int).ravel()
        if threshold > 0:
            err = np.abs(np.asarray(canvas, np.float32) / 255.0 - ref).mean(-1)
            err = smooth(err, radius / 2)
            keep = err[ys, xs] > threshold
            ys, xs = ys[keep], xs[keep]
        order = rng.permutation(len(xs))
        draw = ImageDraw.Draw(canvas)
        for i in order:
            y, x = ys[i], xs[i]
            col = ref[y, x] * (1 + rng.normal(0, jitter, 3)) + rng.normal(0, jitter / 3)
            a = angle[y, x] + rng.normal(0, 0.12)
            length = radius * rng.uniform(*stretch)
            wd = radius * rng.uniform(0.75, 1.05)
            ca, sa = np.cos(a), np.sin(a)
            pts = _UNIT * [length / 2, wd / 2]
            pts = np.stack([pts[:, 0] * ca - pts[:, 1] * sa + x, pts[:, 0] * sa + pts[:, 1] * ca + y], 1)
            draw.polygon([tuple(p) for p in pts], fill=tuple(int(c) for c in np.clip(col * 255, 0, 255)))
    return canvas


def stars(img, seed, count, density=None, bright=0.02, size=1.0, keep=60):
    """Paint stars as tiny dabs with soft halos. `density` (h, w) biases where they fall.
    Returns the image and the list of the brightest stars (x, y, r) for animation overlays."""
    rng = np.random.default_rng(seed)
    w, h = img.size
    if density is None:
        density = np.ones((h, w), np.float32)
    p = density.ravel() / density.sum()
    idx = rng.choice(h * w, count, p=p)
    ys, xs = np.divmod(idx, w)
    mag = rng.random(count) ** 5  # mostly faint, a few bright
    glow = Image.new("RGB", (w, h))
    gd = ImageDraw.Draw(glow)
    base = np.asarray(img, np.float32)
    dots = ImageDraw.Draw(img)
    big = []
    tints = [hexrgb(c) for c in ("#fff6e6", "#e9efff", "#ffe9d0", "#dfe8ff", "#fff1f0")]
    for x, y, m in zip(xs, ys, mag):
        t = tints[rng.integers(len(tints))]
        r = size * (0.6 + 2.4 * m ** 3)
        lum = 0.35 + 0.65 * m
        col = tuple(int(v) for v in np.clip((base[y, x] / 255 * (1 - lum) + t * lum) * 255, 0, 255))
        dots.ellipse([x - r, y - r, x + r, y + r], fill=col)
        big.append((int(x), int(y), r, m))
        if m > 1 - bright:
            hr = r * 2.6
            gd.ellipse([x - hr, y - hr, x + hr, y + hr], fill=tuple(int(v * 95) for v in t))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 2.2))
    out = np.asarray(img, np.float32) + np.asarray(glow, np.float32) * 0.9
    big.sort(key=lambda t: -t[3])
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), [(x, y, r) for x, y, r, _ in big[:keep]]


def canvas_texture(img, seed, strength=0.035):
    """A faint linen weave, the way paint sits on canvas."""
    w, h = img.size
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    weave = (np.sin(xx * 1.9) * np.sin(yy * 1.9) * 0.5 + 0.5) * 0.6 + rng.random((h, w)) * 0.4
    a = np.asarray(img, np.float32) * (1 - strength + strength * weave[..., None] * 2)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
