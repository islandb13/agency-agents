#!/usr/bin/env python3
"""Adds dark-cover text styles and updates create_cover_page to use them.

Without this, cover_title (#6B2D5E plum) and cover_tag (#3A3A3A charcoal)
are invisible against the new dark plum background. The certificate page
keeps the original dark styles untouched.
"""
import os

# ── 1. Add dark variants to _make_styles ──────────────────────────────────────
OLD_STYLES = (
    "            'habit_label': s('hl', fontSize=9, textColor=HexColor('#6B2D5E'),\n"
    "                             alignment=TA_LEFT, fontName='Helvetica-Bold'),\n"
    "        }"
)
NEW_STYLES = (
    "            'habit_label': s('hl', fontSize=9, textColor=HexColor('#6B2D5E'),\n"
    "                             alignment=TA_LEFT, fontName='Helvetica-Bold'),\n"
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

# ── 2. Update create_cover_page to use dark variants ──────────────────────────
OLD_COVER = (
    "    def create_cover_page(self, title, subtitle, price, tagline):\n"
    "        s = self.styles\n"
    "        return [\n"
    "            Spacer(1, 1.6 * inch),\n"
    "            HRFlowable(width='80%', thickness=2, color=Brand.GOLD,\n"
    "                       spaceAfter=18, lineCap='round'),\n"
    "            Paragraph(title,    s['cover_title']),\n"
    "            Paragraph(subtitle, s['cover_sub']),\n"
    "            Spacer(1, 0.2 * inch),\n"
    "            HRFlowable(width='40%', thickness=0.75, color=Brand.ROSE_GOLD, spaceAfter=10),\n"
    "            Paragraph(price,   s['cover_price']),\n"
    "            Spacer(1, 0.15 * inch),\n"
    "            Paragraph(tagline, s['cover_tag']),\n"
    "            HRFlowable(width='80%', thickness=2, color=Brand.GOLD, spaceBefore=20),\n"
    "        ]"
)
NEW_COVER = (
    "    def create_cover_page(self, title, subtitle, price, tagline):\n"
    "        s  = self.styles\n"
    "        dk = os.path.exists(os.path.join('assets', 'backgrounds', 'cover_bg.png'))\n"
    "        return [\n"
    "            Spacer(1, 1.6 * inch),\n"
    "            HRFlowable(width='80%', thickness=1.5, color=Brand.GOLD,\n"
    "                       spaceAfter=18, lineCap='round'),\n"
    "            Paragraph(title,    s['cover_title_dk']   if dk else s['cover_title']),\n"
    "            Paragraph(subtitle, s['cover_sub_dk']     if dk else s['cover_sub']),\n"
    "            Spacer(1, 0.2 * inch),\n"
    "            HRFlowable(width='40%', thickness=0.75, color=Brand.GOLD, spaceAfter=10),\n"
    "            Paragraph(price,   s['cover_price_dk']   if dk else s['cover_price']),\n"
    "            Spacer(1, 0.15 * inch),\n"
    "            Paragraph(tagline, s['cover_tag_dk']     if dk else s['cover_tag']),\n"
    "            HRFlowable(width='80%', thickness=1.5, color=Brand.GOLD, spaceBefore=20),\n"
    "        ]"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

assert OLD_STYLES in src, 'Styles block not found'
assert OLD_COVER  in src, 'create_cover_page block not found'

src = src.replace(OLD_STYLES, NEW_STYLES, 1)
src = src.replace(OLD_COVER,  NEW_COVER,  1)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Dark-cover styles injected.')
print('  cover_title_dk  -> white  #FFFFFF')
print('  cover_sub_dk    -> blush  #F9B8C0')
print('  cover_price_dk  -> gold   #D4A574  (unchanged)')
print('  cover_tag_dk    -> cream  #FFF8F0')
print('  create_cover_page auto-selects dark/light based on cover_bg.png presence')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
