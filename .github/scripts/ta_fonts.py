"""Fonts used by the art (SIL OFL / Apache). Fetched from google/fonts on first use; only their
outlines end up in the SVGs."""
import os
import urllib.request
from functools import lru_cache

from ta_core import FONT_DIR, Font

GF = "https://raw.githubusercontent.com/google/fonts/main/"
TABLE = {
    "ultra": ("apache/ultra/Ultra-Regular.ttf", "u", None),
    "shri": ("ofl/shrikhand/Shrikhand-Regular.ttf", "s", None),
    "tekob": ("ofl/teko/Teko[wght].ttf", "K", 700),
    "teko": ("ofl/teko/Teko[wght].ttf", "k", 600),
    "pop": ("ofl/poppins/Poppins-Medium.ttf", "p", None),
    "popb": ("ofl/poppins/Poppins-Bold.ttf", "b", None),
    "nast": ("ofl/notonastaliqurdu/NotoNastaliqUrdu[wght].ttf", "n", 700),
    "mono": ("ofl/jetbrainsmono/JetBrainsMono[wght].ttf", "j", 600),
}


def ensure(rel):
    path = os.path.join(FONT_DIR, os.path.basename(rel))
    if not os.path.exists(path):
        os.makedirs(FONT_DIR, exist_ok=True)
        url = GF + rel.replace("[", "%5B").replace("]", "%5D")
        with urllib.request.urlopen(url, timeout=60) as r, open(path, "wb") as fh:
            fh.write(r.read())
    return path


@lru_cache(None)
def F(name):
    rel, key, wght = TABLE[name]
    return Font(ensure(rel), key, wght)
