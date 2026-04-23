#!/usr/bin/env python3
"""Patches _make_styles() in launch_build.py:
   - cover_title: fontSize 28, leading 35 (1.25x), spaceAfter 30, charSpace 1.5
   - cover_sub:   add leading 20, spaceAfter 10
   - body:        add leading 14
   Note: ReportLab uses 'charSpace' for letter-spacing; 'letterSpacing' is ignored.
"""
import os

OLD_TITLE = (
    "            'cover_title': s('ct', fontSize=32, textColor=HexColor('#6B2D5E'),\n"
    "                             alignment=TA_CENTER, spaceAfter=8, fontName='Helvetica-Bold'),\n"
    "            'cover_sub':   s('cs', fontSize=16, textColor=HexColor('#B76E79'),\n"
    "                             alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica-Oblique'),"
)
NEW_TITLE = (
    "            'cover_title': s('ct', fontSize=28, leading=35,\n"
    "                             textColor=HexColor('#6B2D5E'), alignment=TA_CENTER,\n"
    "                             spaceAfter=30, fontName='Helvetica-Bold', charSpace=1.5),\n"
    "            'cover_sub':   s('cs', fontSize=16, leading=20,\n"
    "                             textColor=HexColor('#B76E79'),\n"
    "                             alignment=TA_CENTER, spaceAfter=10, fontName='Helvetica-Oblique'),"
)

OLD_BODY = (
    "            'body':        s('bd', fontSize=10, textColor=HexColor('#3A3A3A'),\n"
    "                             alignment=TA_LEFT, fontName='Helvetica'),"
)
NEW_BODY = (
    "            'body':        s('bd', fontSize=10, leading=14,\n"
    "                             textColor=HexColor('#3A3A3A'),\n"
    "                             alignment=TA_LEFT, fontName='Helvetica'),"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

assert OLD_TITLE in src, 'ERROR: cover_title block not found — already patched?'
assert OLD_BODY  in src, 'ERROR: body block not found — already patched?'

src = src.replace(OLD_TITLE, NEW_TITLE, 1)
src = src.replace(OLD_BODY,  NEW_BODY,  1)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Patched _make_styles():')
print('  cover_title  fontSize=28  leading=35  spaceAfter=30  charSpace=1.5')
print('  cover_sub    leading=20   spaceAfter=10')
print('  body         leading=14')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
