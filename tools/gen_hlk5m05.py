"""Hi-Link HLK-5M05 (5 V, 5 W, 85-264 VAC in, 4 through-hole pins) part kit generator.
Writes, under parts/HLK-5M05/: 3d/ (VRML mm, VRML KiCad scale, OBJ zip), eda/ (EAGLE library for EasyEDA Pro),
kicad/ (footprint and symbol).

Dimensions: taken from the KiCad library footprint Converter_ACDC_Hi-Link_HLK-5Mxx, which cites the Hi-Link 5 W
series datasheet V2.8 (pin 1 at 0/0, pin 2 at 0/6, pin 3 at 33.6/-6, pin 4 at 33.6/12 in KiCad's y-down frame, body
39.0 x 23.5 mm, height about 18.1 mm, pins about 4.9 mm below the PCB surface). Only these numbers are used; the
mesh is drawn here from scratch. Pin names: 1 AC, 2 AC, 3 -Vo, 4 +Vo.
Model frame: origin = body centre on the PCB top surface, y up, pin 1 at upper left.
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bluepill_3d as g          # reuse the small mesh + pixel-font helpers

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART = os.path.join(ROOT, "parts", "HLK-5M05")
NAME = "HLK-5M05"
L, W, H = 39.0, 23.5, 18.1           # body length (x), width (y), total height
STANDOFF = 0.2
PIN_TIP = -4.9                       # lowest point of the pins
# pads in the model / EAGLE frame (y up), mm
PADS = [("1", -16.8, 3.0, "AC"), ("2", -16.8, -3.0, "AC"), ("3", 16.8, 9.0, "-Vo"), ("4", 16.8, -9.0, "+Vo")]
DRILL, PAD_W, PAD_H = 1.0, 1.7, 2.0
REV = "rev1"


def build():
    g.clear()
    g.box("black", 0, 0, STANDOFF, L, W, 17.85 - STANDOFF)
    g.box("chip", 0, 0, 17.85, L - 4.0, W - 4.0, H - 17.85)                 # label plate
    g.text("silk", "HLK-5M05", 0, -4.0, H + 0.01, (-1, 0), (0, -1), 0.34, mid=True)
    g.text("silk", "5V 1A 5W", 0, 3.0, H + 0.01, (-1, 0), (0, -1), 0.22, mid=True)
    for _, x, y, _n in PADS:
        g.box("metal", x, y, PIN_TIP, 0.8, 0.8, 2.0 - PIN_TIP)              # pin, from tip up into the body
    # pin-1 mark on the body edge, and pin names on the label side
    g.box("silk", -L / 2 + 0.6, W / 2 - 0.6, H + 0.01, 1.0, 1.0, 0.02)


def emit(zip_title):
    build()
    d3 = os.path.join(PART, "3d")
    os.makedirs(d3, exist_ok=True)
    g.write_wrl(os.path.join(d3, "HLK-5M05_mm.wrl"), 1.0)
    g.write_wrl(os.path.join(d3, "HLK-5M05_kicad_scale.wrl"), 2.54)
    g.write_obj_zip(os.path.join(d3, "HLK-5M05_obj.zip"), zip_title)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lbr():
    hx, hy = L / 2, W / 2
    o = ['<?xml version="1.0" encoding="utf-8"?>', '<!DOCTYPE eagle SYSTEM "eagle.dtd">',
         '<eagle version="9.6.2"><drawing><settings><setting alwaysvectorfont="no"/><setting verticaltext="up"/></settings>',
         '<grid distance="2.54" unitdist="mm" unit="mm" style="lines" multiple="1" display="no" altdistance="0.254" altunitdist="mm" altunit="mm"/>',
         "<layers>" + "".join('<layer number="%d" name="%s" color="%d" fill="1" visible="yes" active="yes"/>' % t for t in
                              [(1, "Top", 4), (16, "Bottom", 1), (17, "Pads", 2), (18, "Vias", 2), (20, "Dimension", 15), (21, "tPlace", 7),
                               (25, "tNames", 7), (27, "tValues", 7), (51, "tDocu", 7), (91, "Nets", 2), (94, "Symbols", 4), (95, "Names", 7), (96, "Values", 7)]) + "</layers>",
         '<library name="HLK5M05"><description>Hi-Link HLK-5M05 AC-DC 5 V 5 W module, 4 through-hole pins</description>',
         '<packages><package name="HLK-5M05_TH"><description>HLK-5M05, body 39.0 x 23.5 mm, pins 33.6 x 6/18 mm apart</description>']
    for n, x, y, _ in PADS:
        o.append('<pad name="%s" x="%.3f" y="%.3f" drill="%.2f" diameter="2.0" shape="%s"/>' % (n, x, y, DRILL, "square" if n == "1" else "round"))
    for (a, b, c, d) in ((-hx, -hy, hx, -hy), (hx, -hy, hx, hy), (hx, hy, -hx, hy), (-hx, hy, -hx, -hy)):
        o.append('<wire x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" width="0.2" layer="21"/>' % (a, b, c, d))
    o.append('<text x="0" y="%.1f" size="1.27" layer="25" align="center">&gt;NAME</text><text x="0" y="%.1f" size="1.27" layer="27" align="center">&gt;VALUE</text></package></packages>' % (hy + 1.5, -hy - 1.5))
    o.append('<symbols><symbol name="HLK-5M05">')
    o.append('<wire x1="-7.62" y1="5.08" x2="7.62" y2="5.08" width="0.254" layer="94"/><wire x1="7.62" y1="5.08" x2="7.62" y2="-5.08" width="0.254" layer="94"/>'
             '<wire x1="7.62" y1="-5.08" x2="-7.62" y2="-5.08" width="0.254" layer="94"/><wire x1="-7.62" y1="-5.08" x2="-7.62" y2="5.08" width="0.254" layer="94"/>')
    o.append('<text x="-7.62" y="6.35" size="1.778" layer="95">&gt;NAME</text><text x="-7.62" y="-7.62" size="1.778" layer="96" align="top-left">&gt;VALUE</text>')
    o.append('<pin name="AC1" x="-12.7" y="2.54" length="middle" direction="pas"/><pin name="AC2" x="-12.7" y="-2.54" length="middle" direction="pas"/>')
    o.append('<pin name="-VO" x="12.7" y="2.54" length="middle" direction="pas" rot="R180"/><pin name="+VO" x="12.7" y="-2.54" length="middle" direction="pas" rot="R180"/></symbol></symbols>')
    o.append('<devicesets><deviceset name="HLK-5M05_3D" prefix="PS"><description>Hi-Link HLK-5M05, 5 V 1 A</description><gates><gate name="G$1" symbol="HLK-5M05" x="0" y="0"/></gates>'
             '<devices><device name="" package="HLK-5M05_TH"><connects>'
             '<connect gate="G$1" pin="AC1" pad="1"/><connect gate="G$1" pin="AC2" pad="2"/><connect gate="G$1" pin="-VO" pad="3"/><connect gate="G$1" pin="+VO" pad="4"/>'
             '</connects><technologies><technology name=""/></technologies></device></devices></deviceset></devicesets></library></drawing></eagle>')
    return "\n".join(o) + "\n"


def kicad_mod():
    hx, hy = L / 2, W / 2
    o = ['(footprint "HLK-5M05" (version 20221018) (generator gen_hlk5m05)', '  (layer "F.Cu")',
         '  (descr "Hi-Link HLK-5M05 AC-DC module, 4 pins, body 39.0 x 23.5 mm")', '  (tags "HLK-5M05 ACDC 5V 5W THT")', '  (attr through_hole)',
         '  (fp_text reference "REF**" (at 0 %.2f) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))' % (-hy - 1.5),
         '  (fp_text value "HLK-5M05" (at 0 %.2f) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))' % (hy + 1.5),
         '  (fp_rect (start %.2f %.2f) (end %.2f %.2f) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS"))' % (-hx, -hy, hx, hy),
         '  (fp_rect (start %.2f %.2f) (end %.2f %.2f) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))' % (-hx - .25, -hy - .25, hx + .25, hy + .25)]
    for n, x, y, _ in PADS:                      # KiCad y points down
        o.append('  (pad "%s" thru_hole %s (at %.2f %.2f) (size %.1f %.1f) (drill %.1f) (layers "*.Cu" "*.Mask"))' % (n, "rect" if n == "1" else "oval", x, -y, PAD_W, PAD_H, DRILL))
    o.append('  (model "${KIPRJMOD}/HLK-5M05_kicad_scale.wrl" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    o.append(')')
    return "\n".join(o) + "\n"


def kicad_sym():
    o = ['(kicad_symbol_lib (version 20220914) (generator gen_hlk5m05)', '  (symbol "HLK-5M05" (in_bom yes) (on_board yes)',
         '    (property "Reference" "PS" (at 0 7.62 0) (effects (font (size 1.27 1.27))))', '    (property "Value" "HLK-5M05" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))',
         '    (property "Footprint" "HLK-5M05" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))', '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
         '    (symbol "HLK-5M05_0_1" (rectangle (start -7.62 5.08) (end 7.62 -5.08) (stroke (width 0.254) (type default)) (fill (type background))))',
         '    (symbol "HLK-5M05_1_1"']
    for nm, num, x, y, rot in (("AC", 1, -10.16, 2.54, 0), ("AC", 2, -10.16, -2.54, 0), ("-Vo", 3, 10.16, 2.54, 180), ("+Vo", 4, 10.16, -2.54, 180)):
        o.append('      (pin passive line (at %.2f %.2f %d) (length 2.54) (name "%s" (effects (font (size 1.27 1.27)))) (number "%d" (effects (font (size 1.27 1.27)))))' % (x, y, rot, nm, num))
    o += ['    )', '  )', ')']
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    emit("hlk-5m05_" + REV)
    for sub, fn, txt in (("eda", "HLK-5M05.lbr", lbr()), ("kicad", "HLK-5M05.kicad_mod", kicad_mod()), ("kicad", "HLK-5M05.kicad_sym", kicad_sym())):
        os.makedirs(os.path.join(PART, sub), exist_ok=True)
        open(os.path.join(PART, sub, fn), "w", encoding="utf-8", newline="\n").write(txt)
    import shutil
    os.makedirs(os.path.join(PART, "kicad"), exist_ok=True)
    shutil.copy(os.path.join(PART, "3d", "HLK-5M05_kicad_scale.wrl"), os.path.join(PART, "kicad", "HLK-5M05_kicad_scale.wrl"))
    print("written to", PART)
