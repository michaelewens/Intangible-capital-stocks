"""Favicon for intangiblesdata.org: indigo rounded square with a rising white bar mark (knowledge over
organization capital). Writes site/static/favicon.svg and favicon.ico (16/32/48 px)."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "static"
ACCENT = (67, 56, 202)   # #4338ca, the site accent

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#4338ca"/>
<rect x="12" y="38" width="10" height="14" rx="2" fill="#ffffff" opacity="0.85"/>
<rect x="27" y="28" width="10" height="24" rx="2" fill="#ffffff" opacity="0.92"/>
<rect x="42" y="14" width="10" height="38" rx="2" fill="#ffffff"/>
</svg>'''
(OUT / "favicon.svg").write_text(svg)

def render(px):
    scale = 8; n = px * scale
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 14 / 64), fill=ACCENT)
    for x, y, w, h, a in [(12, 38, 10, 14, 217), (27, 28, 10, 24, 235), (42, 14, 10, 38, 255)]:
        d.rounded_rectangle([x * n / 64, y * n / 64, (x + w) * n / 64, (y + h) * n / 64], radius=n / 32, fill=(255, 255, 255, a))
    return im.resize((px, px), Image.LANCZOS)

frames = [render(p) for p in (16, 32, 48)]
frames[0].save(OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=frames[1:])
render(180).save(OUT / "apple-touch-icon.png")
print("wrote", sorted(p.name for p in OUT.iterdir()))
