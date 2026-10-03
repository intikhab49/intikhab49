"""Bake what the daily stats job needs (glyph outlines, tape pattern, mini truck) into one JSON,
so field_log.py runs on the standard library alone."""
import json
import os
import sys

from art_arch import mini_truck
from ta_core import Doc, RED
from ta_fonts import F
from ta_motifs import tape_defs

CHARS = [chr(c) for c in range(32, 127)] + ["·", "★", "→"]


def font_table(name):
    f = F(name)
    glyphs = {}
    cmap = f.tt.getBestCmap()
    for ch in CHARS:
        cp = ord(ch)
        if cp not in cmap:
            continue
        gname = cmap[cp]
        gid = f.order.index(gname)
        adv = f.tt["hmtx"][gname][0]
        glyphs[ch] = [adv, f.glyph_d(gid)]
    return {"upem": f.upem, "glyphs": glyphs}


def main(out):
    d = Doc(10, 10, "x")
    pid = tape_defs(d, 16, pid="tp")
    data = {
        "fonts": {k: font_table(k) for k in ("tekob", "pop", "popb")},
        "tape": "".join(d.defs),
        "truck": mini_truck(RED),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../out/truck_glyphs.json")
