#!/usr/bin/env python3
"""Increases document content margins to clear the botanical frame border.

The gold botanical border in cover_bg.png and content_bg.png occupies ~0.6 inch
on each side. With Brand.MARGIN=0.25inch, content bleeds into the decorative zone.
Setting leftMargin/rightMargin to 0.75inch pushes content into the clean center.

Bonus: CouponCard.CW=7.0inch, and 8.5 - 2*0.75 = 7.0inch exactly, so cards
fill the content area perfectly and are balanced on both sides.
"""
import os

OLD_DOC_MARGINS = (
    "                  leftMargin=m, rightMargin=m,\n"
    "                  topMargin=m + 0.6*inch, bottomMargin=m + 0.55*inch)"
)
NEW_DOC_MARGINS = (
    "                  leftMargin=0.75*inch, rightMargin=0.75*inch,\n"
    "                  topMargin=0.90*inch, bottomMargin=0.80*inch)"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

count = src.count(OLD_DOC_MARGINS)
assert count > 0, 'Margin block not found'
src = src.replace(OLD_DOC_MARGINS, NEW_DOC_MARGINS)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print(f'Content margins updated ({count} SimpleDocTemplate calls patched).')
print('  left/right: 0.25in -> 0.75in  (clears botanical frame border)')
print('  topMargin:  0.85in -> 0.90in  (extra clearance for top peony)')
print('  CouponCard: 7.0in card now fills 7.0in content area exactly (balanced)')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
