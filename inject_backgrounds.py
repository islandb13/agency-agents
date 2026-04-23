#!/usr/bin/env python3
"""Patches _header_footer in launch_build.py to embed AI-generated backgrounds.
Cover page (doc.page==1): full premium art background.
Content pages (doc.page>1): subtle watermark texture.
Graceful fallback: if PNG files are absent, PDFs render exactly as before.
"""
import os

OLD = (
    "    def _header_footer(self, canv, doc, title='Mom Rescue Pack'):\n"
    "        canv.saveState()\n"
    "        m, w, h = Brand.MARGIN, Brand.W, Brand.H\n"
    "\n"
    "        # Plum header bar\n"
    "        canv.setFillColor(Brand.PLUM)"
)
NEW = (
    "    def _header_footer(self, canv, doc, title='Mom Rescue Pack'):\n"
    "        canv.saveState()\n"
    "        m, w, h = Brand.MARGIN, Brand.W, Brand.H\n"
    "\n"
    "        # ── AI Premium Backgrounds (graceful fallback if absent) ─────────\n"
    "        _cover_bg   = os.path.join('assets', 'backgrounds', 'cover_bg.png')\n"
    "        _content_bg = os.path.join('assets', 'backgrounds', 'content_bg.png')\n"
    "        if doc.page == 1 and os.path.exists(_cover_bg):\n"
    "            canv.drawImage(_cover_bg, 0, 0, width=w, height=h,\n"
    "                          preserveAspectRatio=False, mask=None)\n"
    "        elif doc.page > 1 and os.path.exists(_content_bg):\n"
    "            canv.drawImage(_content_bg, 0, 0, width=w, height=h,\n"
    "                          preserveAspectRatio=False, mask=None)\n"
    "\n"
    "        # Plum header bar\n"
    "        canv.setFillColor(Brand.PLUM)"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

assert OLD in src, 'Block not found — check prior patches'
src = src.replace(OLD, NEW, 1)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Background embedding patched into _header_footer.')
print('  cover_bg.png   -> page 1 of every SKU (full premium art)')
print('  content_bg.png -> pages 2+ of every SKU (subtle texture)')
print('launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
