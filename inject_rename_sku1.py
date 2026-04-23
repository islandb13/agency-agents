#!/usr/bin/env python3
"""Two fixes:
1. Rename SKU 1 from 'Last-Minute Dad's Gift Kit' -> 'Mom's Coupon Book'
   (user confirmed the title should reference Mom, not Dad)
2. Update logo loader to prefer .png (transparent) over .jpeg (white bg)
"""
import os

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

patches = []

# ── 1a. Rename in build_coupon_book on_page callback ─────────────────────────
patches.append((
    'self._header_footer(c, doc, "Last-Minute Dad\'s Gift Kit")',
    'self._header_footer(c, doc, "Mom\'s Coupon Book")',
    'header_footer title'
))

# ── 1b. Rename in Canva override fallback ─────────────────────────────────────
patches.append((
    '            story = self.create_cover_page(\n'
    '                "Last-Minute Dad\'s Gift Kit",\n'
    '                \'8 Heartfelt Coupons for Mom\',\n'
    '                \'$17\',\n'
    '                \'Because she deserves every single one.\')',
    '            story = self.create_cover_page(\n'
    '                "Mom\'s Coupon Book",\n'
    '                \'8 Heartfelt Gift Coupons — Just for Her\',\n'
    '                \'$17\',\n'
    '                \'Because she deserves every single one.\')',
    'create_cover_page title'
))

# ── 1c. Rename in bundle summary / run_all references ─────────────────────────
patches.append((
    "'SKU 1 — Last-Minute Dad Gift Kit (Coupon Book)<br/>'",
    "'SKU 1 — Mom\\u2019s Coupon Book (8 Heartfelt Gift Coupons)<br/>'",
    'bundle summary SKU1 line'
))

patches.append((
    "('SKU 1: Coupon Book',    self.build_coupon_book)",
    "('SKU 1: Mom\\'s Coupon Book', self.build_coupon_book)",
    'run_all tuple label'
))

# ── 2. Logo: prefer PNG (transparent) over JPEG (white bg) ───────────────────
OLD_LOGO_CHECK = (
    "        # Logo (embedded if present)\n"
    "        if os.path.exists(Brand.LOGO):\n"
    "            canv.drawImage(Brand.LOGO, m + 4, h - m - 0.44*inch,\n"
    "                           width=0.30*inch, height=0.30*inch,\n"
    "                           preserveAspectRatio=True, mask='auto')"
)
NEW_LOGO_CHECK = (
    "        # Logo: prefer PNG (transparent bg) over JPEG\n"
    "        _logo = next((f for f in [\n"
    "            'mom-rescue-pack-logo.png',\n"
    "            Brand.LOGO,\n"
    "        ] if os.path.exists(f)), None)\n"
    "        if _logo:\n"
    "            canv.drawImage(_logo, m + 4, h - m - 0.44*inch,\n"
    "                           width=0.30*inch, height=0.30*inch,\n"
    "                           preserveAspectRatio=True, mask='auto')"
)
patches.append((OLD_LOGO_CHECK, NEW_LOGO_CHECK, 'logo PNG preference'))

for old, new, label in patches:
    if old not in src:
        print(f'  SKIP (not found): {label}')
        continue
    src = src.replace(old, new, 1)
    print(f'  Patched: {label}')

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('\nSKU 1 renamed + logo fix applied.')
print('  Cover title: "Mom\'s Coupon Book"')
print('  Logo: checks mom-rescue-pack-logo.png first (transparent), falls back to .jpeg')
print('  To use transparent logo: export your logo as PNG with transparent background')
print('  and save it as mom-rescue-pack-logo.png in the project root')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
