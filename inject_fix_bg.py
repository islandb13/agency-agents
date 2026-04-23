#!/usr/bin/env python3
"""Fixes dark background bleeding onto content pages of SKUs without a cover.

Root cause: _header_footer uses doc.page==1 for dark bg, but activity_pack
and card_pack start with content (no create_cover_page call), so their page 1
incorrectly gets the dark cover background.

Fix: add self._has_cover flag set by create_cover_page; _header_footer checks
this flag before deciding which background to apply.
"""
import os

# ── 1. Add _has_cover flag to __init__ ────────────────────────────────────────
OLD_INIT = (
    "    def __init__(self):\n"
    "        self.styles = self._make_styles()"
)
NEW_INIT = (
    "    def __init__(self):\n"
    "        self.styles = self._make_styles()\n"
    "        self._has_cover = False  # set True by create_cover_page"
)

# ── 2. Set flag in create_cover_page ──────────────────────────────────────────
OLD_COVERFN = (
    "    def create_cover_page(self, title, subtitle, price, tagline):\n"
    "        s  = self.styles\n"
    "        dk = os.path.exists(os.path.join('assets', 'backgrounds', 'cover_bg.png'))"
)
NEW_COVERFN = (
    "    def create_cover_page(self, title, subtitle, price, tagline):\n"
    "        self._has_cover = True   # tells _header_footer page 1 is a cover\n"
    "        s  = self.styles\n"
    "        dk = os.path.exists(os.path.join('assets', 'backgrounds', 'cover_bg.png'))"
)

# ── 3. Gate dark bg behind self._has_cover ────────────────────────────────────
OLD_BG = (
    "        # ── AI Premium Backgrounds (graceful fallback if absent) ─────────\n"
    "        _cover_bg   = os.path.join('assets', 'backgrounds', 'cover_bg.png')\n"
    "        _content_bg = os.path.join('assets', 'backgrounds', 'content_bg.png')\n"
    "        if doc.page == 1 and os.path.exists(_cover_bg):\n"
    "            canv.drawImage(_cover_bg, 0, 0, width=w, height=h,\n"
    "                          preserveAspectRatio=False, mask=None)\n"
    "        elif doc.page > 1 and os.path.exists(_content_bg):\n"
    "            canv.drawImage(_content_bg, 0, 0, width=w, height=h,\n"
    "                          preserveAspectRatio=False, mask=None)"
)
NEW_BG = (
    "        # ── AI Premium Backgrounds (graceful fallback if absent) ─────────\n"
    "        _cover_bg   = os.path.join('assets', 'backgrounds', 'cover_bg.png')\n"
    "        _content_bg = os.path.join('assets', 'backgrounds', 'content_bg.png')\n"
    "        if self._has_cover and doc.page == 1 and os.path.exists(_cover_bg):\n"
    "            canv.drawImage(_cover_bg, 0, 0, width=w, height=h,\n"
    "                          preserveAspectRatio=False, mask=None)\n"
    "        elif os.path.exists(_content_bg) and not (self._has_cover and doc.page == 1):\n"
    "            canv.drawImage(_content_bg, 0, 0, width=w, height=h,\n"
    "                          preserveAspectRatio=False, mask=None)"
)

# ── 4. Reset flag per-build so SKUs don't bleed state ─────────────────────────
OLD_RESET_A = "    def build_coupon_book(self):\n        path = os.path.join(Brand.OUT, 'sku1_coupon_book.pdf')"
NEW_RESET_A = "    def build_coupon_book(self):\n        self._has_cover = False\n        path = os.path.join(Brand.OUT, 'sku1_coupon_book.pdf')"

OLD_RESET_B = "    def build_daily_planner(self):\n        path = os.path.join(Brand.OUT, 'sku2_daily_planner.pdf')"
NEW_RESET_B = "    def build_daily_planner(self):\n        self._has_cover = False\n        path = os.path.join(Brand.OUT, 'sku2_daily_planner.pdf')"

OLD_RESET_C = "    def build_card_pack(self):\n        from reportlab.pdfgen import canvas as pdfcanvas"
NEW_RESET_C = "    def build_card_pack(self):\n        self._has_cover = False\n        from reportlab.pdfgen import canvas as pdfcanvas"

OLD_RESET_D = "    def build_activity_pack(self):\n        path = os.path.join(Brand.OUT, 'sku4_activity_pack.pdf')"
NEW_RESET_D = "    def build_activity_pack(self):\n        self._has_cover = False\n        path = os.path.join(Brand.OUT, 'sku4_activity_pack.pdf')"

OLD_RESET_E = "    def build_mom_manual(self):\n        path = os.path.join(Brand.OUT, 'sku5_mom_manual.pdf')"
NEW_RESET_E = "    def build_mom_manual(self):\n        self._has_cover = False\n        path = os.path.join(Brand.OUT, 'sku5_mom_manual.pdf')"

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

for old, new, label in [
    (OLD_INIT,    NEW_INIT,    '__init__ flag'),
    (OLD_COVERFN, NEW_COVERFN, 'create_cover_page flag'),
    (OLD_BG,      NEW_BG,      '_header_footer bg logic'),
    (OLD_RESET_A, NEW_RESET_A, 'reset SKU1'),
    (OLD_RESET_B, NEW_RESET_B, 'reset SKU2'),
    (OLD_RESET_C, NEW_RESET_C, 'reset SKU3'),
    (OLD_RESET_D, NEW_RESET_D, 'reset SKU4'),
    (OLD_RESET_E, NEW_RESET_E, 'reset SKU5'),
]:
    assert old in src, f'Block not found: {label}'
    src = src.replace(old, new, 1)
    print(f'  Patched: {label}')

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Background routing fixed.')
print('  SKUs WITH create_cover_page  -> dark bg p.1, cream bg p.2+')
print('  SKUs WITHOUT create_cover_page -> cream bg ALL pages')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
