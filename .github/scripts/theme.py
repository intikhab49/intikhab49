"""Shared palette + helpers for the profile's hand-built SVGs ("signal / noise" theme)."""
from xml.sax.saxutils import escape

THEMES = {
    "dark": dict(bg="#0C0E0D", panel="#141816", rule="#2B312D", text="#ECE6D8",
                 muted="#8D958A", signal="#FF6B1A", sage="#9DB89A", faint="#1C211E"),
    "light": dict(bg="#F4F0E6", panel="#EBE5D6", rule="#CFC6B2", text="#17181A",
                  muted="#6A6E66", signal="#D2500A", sage="#4F6B4C", faint="#E4DDCB"),
}

SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def x(s):
    return escape(str(s))


def style(t):
    return f"""<style>
  .serif {{ font-family: {SERIF}; fill: {t['text']}; }}
  .mono  {{ font-family: {MONO}; fill: {t['muted']}; letter-spacing: 1.5px; }}
  .sig   {{ fill: {t['signal']}; }}
  .sage  {{ fill: {t['sage']}; }}
  .ink   {{ fill: {t['text']}; }}
  .blink {{ animation: blink 1.6s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0.15; }} }}
  .draw  {{ stroke-dasharray: 1; animation: draw 5.5s ease-out infinite backwards; }}
  .draw2 {{ animation-delay: 0.6s; }}
  @keyframes draw {{ 0% {{ stroke-dashoffset: 1; }} 55% {{ stroke-dashoffset: 0; }} 88% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .scan  {{ animation: scan 5.5s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateX(0); }} to {{ transform: translateX(364px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .draw, .scan, .blink {{ animation: none; stroke-dashoffset: 0; }} }}
</style>"""


def grid(t, pid, step=24, opacity=0.45):
    return (f'<defs><pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<path d="M {step} 0 L 0 0 0 {step}" fill="none" stroke="{t["rule"]}" stroke-width="0.6" opacity="{opacity}"/>'
            f'</pattern></defs>')


def corners(t, w, h, m=18, L=14):
    c = t["muted"]
    p = [f"M{m} {m+L}V{m}H{m+L}", f"M{w-m-L} {m}H{w-m}V{m+L}",
         f"M{m} {h-m-L}V{h-m}H{m+L}", f"M{w-m-L} {h-m}H{w-m}V{h-m-L}"]
    return "".join(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.2"/>' for d in p)


def frame(t, w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{x(title)}"><title>{x(title)}</title>{style(t)}'
            f'<rect width="{w}" height="{h}" rx="14" fill="{t["bg"]}"/>{body}</svg>')
