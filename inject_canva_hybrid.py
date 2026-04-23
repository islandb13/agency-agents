#!/usr/bin/env python3
"""Hybrid Canva/ReportLab cover system.

Drop a Canva-exported PNG into assets/canva_covers/skuN.png and it replaces
the programmatic cover page for that SKU. Content pages remain pure ReportLab.
No file = falls back to the current ReportLab cover automatically.

File naming:
  assets/canva_covers/sku1.png  ->  Last-Minute Dad's Gift Kit
  assets/canva_covers/sku2.png  ->  Daily Sanity Planner
  assets/canva_covers/sku4.png  ->  Mom Activity Pack
  assets/canva_covers/sku5.png  ->  Mom Rescue Pack (User Manual)
"""
import os

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

patches = []

# ── 1. Add CanvaCover class after CouponCard ──────────────────────────────────
OLD_AFTER_COUPON = (
    "\n\n# ── 7-Day Week Grid ────────────────────────────────────────────────────────────"
)
NEW_AFTER_COUPON = (
    "\n\n"
    "class CanvaCover(Flowable):\n"
    "    \"\"\"Full-page Canva-exported cover. Header/footer is suppressed on this page.\"\"\"\n"
    "    def __init__(self, path):\n"
    "        Flowable.__init__(self)\n"
    "        self._path = path\n"
    "    def wrap(self, aW, aH):\n"
    "        return aW, aH\n"
    "    def draw(self):\n"
    "        self.canv.drawImage(\n"
    "            self._path,\n"
    "            -(0.75 * inch), -(0.80 * inch),\n"
    "            width=Brand.W, height=Brand.H,\n"
    "            preserveAspectRatio=False, mask=None\n"
    "        )\n"
    "\n\n"
    "# ── 7-Day Week Grid ────────────────────────────────────────────────────────────"
)
patches.append((OLD_AFTER_COUPON, NEW_AFTER_COUPON, 'CanvaCover class'))

# ── 2. Add _skip_header_p1 flag to __init__ ───────────────────────────────────
OLD_INIT_FLAG = (
    "        self._has_cover = False  # set True by create_cover_page"
)
NEW_INIT_FLAG = (
    "        self._has_cover = False  # set True by create_cover_page\n"
    "        self._skip_header_p1 = False  # True when full Canva cover PNG is used"
)
patches.append((OLD_INIT_FLAG, NEW_INIT_FLAG, '__init__ _skip_header_p1 flag'))

# ── 3. Short-circuit _header_footer on Canva cover pages ─────────────────────
OLD_HF = (
    "        canv.saveState()\n"
    "        m, w, h = Brand.MARGIN, Brand.W, Brand.H\n"
    "\n"
    "        # ── AI Premium Backgrounds (graceful fallback if absent) ─────────"
)
NEW_HF = (
    "        canv.saveState()\n"
    "        m, w, h = Brand.MARGIN, Brand.W, Brand.H\n"
    "        if self._skip_header_p1 and doc.page == 1:\n"
    "            canv.restoreState()\n"
    "            return\n"
    "\n"
    "        # ── AI Premium Backgrounds (graceful fallback if absent) ─────────"
)
patches.append((OLD_HF, NEW_HF, '_header_footer Canva skip'))

# ── 4. SKU 1: Canva override for coupon book ──────────────────────────────────
OLD_SKU1 = (
    "        story = self.create_cover_page(\n"
    "            \"Last-Minute Dad's Gift Kit\",\n"
    "            '8 Heartfelt Coupons for Mom',\n"
    "            '$17',\n"
    "            'Because she deserves every single one.')\n"
    "        story.append(PageBreak())"
)
NEW_SKU1 = (
    "        _canva = os.path.join('assets', 'canva_covers', 'sku1.png')\n"
    "        if os.path.exists(_canva):\n"
    "            self._has_cover = True; self._skip_header_p1 = True\n"
    "            story = [CanvaCover(_canva), PageBreak()]\n"
    "        else:\n"
    "            self._skip_header_p1 = False\n"
    "            story = self.create_cover_page(\n"
    "                \"Last-Minute Dad's Gift Kit\",\n"
    "                '8 Heartfelt Coupons for Mom',\n"
    "                '$17',\n"
    "                'Because she deserves every single one.')\n"
    "            story.append(PageBreak())"
)
patches.append((OLD_SKU1, NEW_SKU1, 'SKU1 Canva override'))

# ── 5. SKU 2: Canva override for daily planner ───────────────────────────────
OLD_SKU2 = (
    "        story = self.create_cover_page(\n"
    "            'Daily Sanity Planner',\n"
    "            'Your Weekly Self-Care System',\n"
    "            '$27',\n"
    "            '7 days. One calm, intentional week.')\n"
    "        story.append(PageBreak())"
)
NEW_SKU2 = (
    "        _canva = os.path.join('assets', 'canva_covers', 'sku2.png')\n"
    "        if os.path.exists(_canva):\n"
    "            self._has_cover = True; self._skip_header_p1 = True\n"
    "            story = [CanvaCover(_canva), PageBreak()]\n"
    "        else:\n"
    "            self._skip_header_p1 = False\n"
    "            story = self.create_cover_page(\n"
    "                'Daily Sanity Planner',\n"
    "                'Your Weekly Self-Care System',\n"
    "                '$27',\n"
    "                '7 days. One calm, intentional week.')\n"
    "            story.append(PageBreak())"
)
patches.append((OLD_SKU2, NEW_SKU2, 'SKU2 Canva override'))

# ── 6. SKU 4: Canva override for activity pack (story starts empty) ───────────
OLD_SKU4 = (
    "        s     = self.styles\n"
    "        story = []"
)
NEW_SKU4 = (
    "        s     = self.styles\n"
    "        _canva = os.path.join('assets', 'canva_covers', 'sku4.png')\n"
    "        if os.path.exists(_canva):\n"
    "            self._has_cover = True; self._skip_header_p1 = True\n"
    "            story = [CanvaCover(_canva), PageBreak()]\n"
    "        else:\n"
    "            self._skip_header_p1 = False\n"
    "            story = []"
)
patches.append((OLD_SKU4, NEW_SKU4, 'SKU4 Canva override'))

# ── 7. SKU 5: Canva override for mom manual ───────────────────────────────────
OLD_SKU5 = (
    "        story = self.create_cover_page(\n"
    "            'Mom Rescue Pack',\n"
    "            'Official User Manual — 2025 Edition',\n"
    "            '$37 Value',\n"
    "            'Everything you need to run this household like a pro.')\n"
    "        story.append(PageBreak())"
)
NEW_SKU5 = (
    "        _canva = os.path.join('assets', 'canva_covers', 'sku5.png')\n"
    "        if os.path.exists(_canva):\n"
    "            self._has_cover = True; self._skip_header_p1 = True\n"
    "            story = [CanvaCover(_canva), PageBreak()]\n"
    "        else:\n"
    "            self._skip_header_p1 = False\n"
    "            story = self.create_cover_page(\n"
    "                'Mom Rescue Pack',\n"
    "                'Official User Manual — 2025 Edition',\n"
    "                '$37 Value',\n"
    "                'Everything you need to run this household like a pro.')\n"
    "            story.append(PageBreak())"
)
patches.append((OLD_SKU5, NEW_SKU5, 'SKU5 Canva override'))

for old, new, label in patches:
    assert old in src, f'Block not found: {label}'
    src = src.replace(old, new, 1)
    print(f'  Patched: {label}')

# Create the canva_covers directory (with a .gitkeep so it's tracked)
os.makedirs(os.path.join('assets', 'canva_covers'), exist_ok=True)
gitkeep = os.path.join('assets', 'canva_covers', '.gitkeep')
if not os.path.exists(gitkeep):
    open(gitkeep, 'w').close()

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('\nCanva hybrid system ready.')
print('  assets/canva_covers/sku1.png  ->  Last-Minute Dad\'s Gift Kit cover')
print('  assets/canva_covers/sku2.png  ->  Daily Sanity Planner cover')
print('  assets/canva_covers/sku4.png  ->  Mom Activity Pack cover')
print('  assets/canva_covers/sku5.png  ->  Mom Rescue Pack cover')
print('  No PNG = falls back to ReportLab cover automatically')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
