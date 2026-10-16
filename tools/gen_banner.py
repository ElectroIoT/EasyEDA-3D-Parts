"""Builds assets/banner.svg: an animated banner (pure SVG/SMIL, works inside a GitHub README <img>).
Cross-fades the 3D pictures of the part, with animated pin lights. Run: python tools/gen_banner.py"""
import base64
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")


def b64(name):
    return base64.b64encode(open(os.path.join(A, name), "rb").read()).decode()


W, H = 1280, 440
CX, CY, CW, CH = 700, 40, 540, 360            # picture card
SLIDES = [("bluepill_iso.jpg", "3D view: solder-in header pins", 800, 764),
          ("bluepill_top.jpg", "Top view: silkscreen and parts", 800, 765),
          ("bluepill_side.jpg", "Side view: pins go through the PCB", 800, 546)]
T = 12.0                                       # seconds for the whole cycle
o = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Segoe UI, Helvetica, Arial, sans-serif">' % (W, H, W, H)]
o.append('<title>EasyEDA 3D Parts: 3D models, footprints and symbols</title>')
o.append('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1633"/><stop offset="1" stop-color="#0f3a63"/></linearGradient>
<linearGradient id="ttl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5ee7ff"/><stop offset="1" stop-color="#7cf2a8"/></linearGradient>
<clipPath id="card"><rect x="%d" y="%d" width="%d" height="%d" rx="22"/></clipPath>
<filter id="glow" x="-20%%" y="-20%%" width="140%%" height="140%%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#5ee7ff" stroke-opacity="0.07"/></pattern>
</defs>''' % (CX, CY, CW, CH))
o.append('<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H))
o.append('<rect width="%d" height="%d" fill="url(#grid)"><animateTransform attributeName="transform" type="translate" from="0 0" to="40 40" dur="6s" repeatCount="indefinite"/></rect>' % (W + 80, H + 80))
# traces
for i, (y, d) in enumerate([(70, 9), (370, 11), (400, 8)]):
    o.append('<path d="M0 %d H380 L420 %d H%d" fill="none" stroke="#5ee7ff" stroke-opacity="0.25" stroke-width="2"/>' % (y, y + 30, W))
    o.append('<circle r="4" fill="#7cf2a8" filter="url(#glow)"><animateMotion dur="%ds" repeatCount="indefinite" path="M0 %d H380 L420 %d H%d"/></circle>' % (d, y, y + 30, W))
# title
o.append('<g><text x="60" y="150" font-size="30" font-weight="600" fill="#8fb3d9" letter-spacing="6">ELECTROIOT</text>'
         '<text x="60" y="222" font-size="68" font-weight="800" fill="url(#ttl)">EasyEDA</text>'
         '<text x="60" y="292" font-size="68" font-weight="800" fill="url(#ttl)">3D Parts</text>'
         '<animate attributeName="opacity" from="0" to="1" dur="1.2s" fill="freeze"/></g>')
o.append('<text x="62" y="338" font-size="22" fill="#cfe3ff">3D models, footprints and symbols you can drop</text>')
o.append('<text x="62" y="368" font-size="22" fill="#cfe3ff">straight into a custom PCB.</text>')
# chips
x = 62
for label, col in (("EasyEDA Pro", "#5ee7ff"), ("KiCad", "#7cf2a8"), ("VRML / OBJ", "#ffd166"), ("CC BY 4.0", "#ff8fa3")):
    w = 22 + 11 * len(label)
    o.append('<rect x="%d" y="394" width="%d" height="30" rx="15" fill="none" stroke="%s" stroke-width="1.6"/><text x="%d" y="414" font-size="15" fill="%s" text-anchor="middle">%s</text>' % (x, w, col, x + w / 2, col, label))
    x += w + 12
# card
o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="22" fill="#dfe6f2" filter="url(#glow)"/>' % (CX, CY, CW, CH))
o.append('<g clip-path="url(#card)">')
n = len(SLIDES)
for i, (img, cap, iw, ih) in enumerate(SLIDES):
    s = max(CW / iw, (CH - 44) / ih)
    w, h = iw * s, ih * s
    ix, iy = CX + (CW - w) / 2, CY + (CH - 44 - h) / 2
    a_, b_, f = i / n, (i + 1) / n, 0.04 / n
    if i == 0:
        vals, kts = "1;1;0;0;1", "0;%.4f;%.4f;%.4f;1" % (b_ - f, b_, 1 - f)
    elif i == n - 1:
        vals, kts = "0;0;1;1", "0;%.4f;%.4f;1" % (a_, a_ + f)
    else:
        vals, kts = "0;0;1;1;0;0", "0;%.4f;%.4f;%.4f;%.4f;1" % (a_, a_ + f, b_ - f, b_)
    o.append('<g opacity="%d"><image x="%.1f" y="%.1f" width="%.1f" height="%.1f" xlink:href="data:image/jpeg;base64,%s"/>'
             '<rect x="%d" y="%d" width="%d" height="44" fill="#0b1633"/><text x="%d" y="%d" font-size="19" fill="#cfe3ff" text-anchor="middle">%s</text>'
             '<animate attributeName="opacity" values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite"/></g>'
             % (1 if i == 0 else 0, ix, iy, w, h, b64(img), CX, CY + CH - 44, CW, CX + CW / 2, CY + CH - 15, cap, vals, kts, T))
o.append('</g>')
o.append('</svg>')
open(os.path.join(A, "banner.svg"), "w", encoding="utf-8").write("\n".join(o))
print("banner.svg", os.path.getsize(os.path.join(A, "banner.svg")) // 1024, "KB")
