#!/usr/bin/env python3
"""Adapts PDF styles for Option D — Classic Gold Foil Feminine.

Changes:
1. _dk cover styles: white-on-dark -> dark-on-light (cover_bg.png is now ivory)
2. Header bar: solid plum rect -> elegant gold double-rule with plum text
"""
import os

# ── 1. Update _dk styles to dark text (light marble background) ───────────────
OLD_DK_STYLES = (
    "            # Dark-background cover variants (used on page 1 over dark PNG)\n"
    "            'cover_title_dk': s('ctdk', fontSize=28, leading=35,\n"
    "                                textColor=HexColor('#FFFFFF'), alignment=TA_CENTER,\n"
    "                                spaceAfter=30, fontName='Helvetica-Bold', charSpace=1.5),\n"
    "            'cover_sub_dk':   s('csdk', fontSize=16, leading=20,\n"
    "                                textColor=HexColor('#F9B8C0'), alignment=TA_CENTER,\n"
    "                                spaceAfter=10, fontName='Helvetica-Oblique'),\n"
    "            'cover_price_dk': s('cpdk', fontSize=22, textColor=HexColor('#D4A574'),\n"
    "                                alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold'),\n"
    "            'cover_tag_dk':   s('cgdk', fontSize=11, textColor=HexColor('#FFF8F0'),\n"
    "                                alignment=TA_CENTER, fontName='Helvetica'),\n"
    "        }"
)
NEW_DK_STYLES = (
    "            # Cover-with-background variants (used on page 1 over cover_bg.png)\n"
    "            'cover_title_dk': s('ctdk', fontSize=28, leading=35,\n"
    "                                textColor=HexColor('#6B2D5E'), alignment=TA_CENTER,\n"
    "                                spaceAfter=30, fontName='Helvetica-Bold', charSpace=1.5),\n"
    "            'cover_sub_dk':   s('csdk', fontSize=16, leading=20,\n"
    "                                textColor=HexColor('#B76E79'), alignment=TA_CENTER,\n"
    "                                spaceAfter=10, fontName='Helvetica-Oblique'),\n"
    "            'cover_price_dk': s('cpdk', fontSize=22, textColor=HexColor('#C4963A'),\n"
    "                                alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold'),\n"
    "            'cover_tag_dk':   s('cgdk', fontSize=11, textColor=HexColor('#3A3A3A'),\n"
    "                                alignment=TA_CENTER, fontName='Helvetica'),\n"
    "        }"
)

# ── 2. Replace plum header bar with gold double-rule elegant header ────────────
OLD_HEADER = (
    "        # Plum header bar\n"
    "        canv.setFillColor(Brand.PLUM)\n"
    "        canv.rect(m, h - m - 0.45*inch, w - 2*m, 0.45*inch, fill=1, stroke=0)\n"
    "\n"
    "        # Logo (embedded if present)\n"
    "        if os.path.exists(Brand.LOGO):\n"
    "            canv.drawImage(Brand.LOGO, m + 4, h - m - 0.42*inch,\n"
    "                           width=0.38*inch, height=0.38*inch,\n"
    "                           preserveAspectRatio=True, mask='auto')\n"
    "\n"
    "        canv.setFont('Helvetica-Bold', 10)\n"
    "        canv.setFillColor(white)\n"
    "        canv.drawString(m + 0.48*inch, h - m - 0.29*inch, 'MOM RESCUE PACK')\n"
    "\n"
    "        canv.setFont('Helvetica', 9)\n"
    "        canv.drawRightString(w - m - 4, h - m - 0.29*inch, title)"
)
NEW_HEADER = (
    "        # Gold double-rule header (Option D — Classic Gold Foil)\n"
    "        canv.setStrokeColor(Brand.GOLD)\n"
    "        canv.setLineWidth(1.8)\n"
    "        canv.line(m, h - m - 0.06*inch, w - m, h - m - 0.06*inch)\n"
    "        canv.setLineWidth(0.4)\n"
    "        canv.line(m, h - m - 0.12*inch, w - m, h - m - 0.12*inch)\n"
    "\n"
    "        # Logo (embedded if present)\n"
    "        if os.path.exists(Brand.LOGO):\n"
    "            canv.drawImage(Brand.LOGO, m + 4, h - m - 0.44*inch,\n"
    "                           width=0.30*inch, height=0.30*inch,\n"
    "                           preserveAspectRatio=True, mask='auto')\n"
    "\n"
    "        canv.setFont('Helvetica-Bold', 9)\n"
    "        canv.setFillColor(Brand.PLUM)\n"
    "        canv.drawString(m + 0.42*inch, h - m - 0.32*inch, 'MOM RESCUE PACK')\n"
    "\n"
    "        canv.setFont('Helvetica-Oblique', 9)\n"
    "        canv.setFillColor(Brand.ROSE_GOLD)\n"
    "        canv.drawRightString(w - m - 4, h - m - 0.32*inch, title)\n"
    "\n"
    "        canv.setStrokeColor(Brand.GOLD)\n"
    "        canv.setLineWidth(0.4)\n"
    "        canv.line(m, h - m - 0.46*inch, w - m, h - m - 0.46*inch)"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

assert OLD_DK_STYLES in src, 'Block not found: _dk styles'
assert OLD_HEADER    in src, 'Block not found: header bar'

src = src.replace(OLD_DK_STYLES, NEW_DK_STYLES, 1)
src = src.replace(OLD_HEADER,    NEW_HEADER,    1)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Option D styles applied.')
print('  cover_title_dk  -> plum   #6B2D5E  (on light marble)')
print('  cover_sub_dk    -> rose   #B76E79')
print('  cover_price_dk  -> gold   #C4963A  (deeper for light bg)')
print('  cover_tag_dk    -> charcoal #3A3A3A')
print('  header          -> gold double-rule + plum text (no filled bar)')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
