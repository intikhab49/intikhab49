"""Regenerate every image on the profile: python .github/scripts/build_art.py  (needs fonttools + uharfbuzz).

Writes assets/*.svg, assets/cards/*.svg and .github/scripts/truck_glyphs.json (used by the daily stats job),
then parses every file as XML so a broken image never ships.
"""
import os
import sys
import xml.dom.minidom

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

import art_arch  # noqa: E402
import art_cards  # noqa: E402
import art_cta  # noqa: E402
import art_hero  # noqa: E402
import art_road  # noqa: E402
import art_services  # noqa: E402
import art_stack  # noqa: E402
import ta_export  # noqa: E402


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else ROOT
    a = os.path.join(root, "assets")
    jobs = [("hero.svg", art_hero.build), ("road.svg", art_road.build), ("services.svg", art_services.build),
            ("architecture.svg", art_arch.build), ("stack.svg", art_stack.build), ("cta.svg", art_cta.build)]
    written = []
    for name, fn in jobs:
        path = os.path.join(a, name)
        size = fn().save(path)
        written.append((path, size))
    for c in art_cards.CARDS:
        path = os.path.join(a, "cards", c["key"] + ".svg")
        written.append((path, art_cards.build(c).save(path)))
    ta_export.main(os.path.join(HERE, "truck_glyphs.json"))
    for path, size in written:
        xml.dom.minidom.parse(path)
        print(f"{size / 1024:7.1f} KB  {os.path.relpath(path, root)}")
    print(f"{sum(s for _, s in written) / 1024:7.1f} KB total")


if __name__ == "__main__":
    main()
