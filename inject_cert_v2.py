#!/usr/bin/env python3
"""Upgrades certificate name field from HRFlowable to Table + LINEBELOW.
Per project standards: Table structure is more robust for premium design.
"""
import os

OLD = (
    "        story.append(Spacer(1, 0.2*inch))\n"
    "        # Clean single name-line (no stacked rules)\n"
    "        story.append(HRFlowable(width=3.5*inch, thickness=1.0,\n"
    "                                color=Brand.ROSE_GOLD, spaceAfter=14))"
)
NEW = (
    "        story.append(Spacer(1, 0.2*inch))\n"
    "        # Name field: Table + LINEBELOW per project standards (premium, robust)\n"
    "        _cert_name = Table([['']], colWidths=[3.5*inch], rowHeights=[0.45*inch])\n"
    "        _cert_name.setStyle(TableStyle([\n"
    "            ('LINEBELOW', (0, 0), (0, 0), 1.5, Brand.ROSE_GOLD),\n"
    "        ]))\n"
    "        _cert_name.hAlign = 'CENTER'\n"
    "        story.append(_cert_name)"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

assert OLD in src, 'Block not found — check prior patches'
src = src.replace(OLD, NEW, 1)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Certificate name field: HRFlowable -> Table + LINEBELOW')
print('launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
