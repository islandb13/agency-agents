#!/usr/bin/env python3
"""Fixes the Certificate of Appreciation layout in build_activity_pack.

Root cause: HRFlowable(60%) + '____' paragraph + another sub-paragraph stack
three horizontal rules visually, causing alignment confusion.
Fix: replace underscores with a clean centred 3.5" name-line HR; increase top
Spacer from 0.8" to 1.6" for proper vertical centring; add explicit Spacers
between every element for breathing room.
"""
import os

OLD = (
        "        # ── Page 3: Certificate of Appreciation ───────────────────────────────\n"
        "        story.append(Spacer(1, 0.8*inch))\n"
        "        story.append(HRFlowable(width='90%', thickness=2,\n"
        "                                color=Brand.GOLD, spaceAfter=20))\n"
        "        story.append(Paragraph('Certificate of Appreciation', s['cover_title']))\n"
        "        story.append(Paragraph('This certifies that', s['cover_sub']))\n"
        "        story.append(HRFlowable(width='60%', thickness=0.75,\n"
        "                                color=Brand.ROSE_GOLD, spaceAfter=6))\n"
        "        story.append(Paragraph('________________________________', s['cover_price']))\n"
        "        story.append(Paragraph('is officially the', s['cover_sub']))\n"
        "        story.append(Paragraph(\"World's Greatest Mom\", s['cover_title']))\n"
        "        story.append(Spacer(1, 0.2*inch))\n"
        "        story.append(Paragraph(\n"
        "            'Awarded with love, gratitude, and absolutely zero conditions.',\n"
        "            s['cover_tag']))\n"
        "        story.append(HRFlowable(width='90%', thickness=2,\n"
        "                                color=Brand.GOLD, spaceBefore=30))"
)

NEW = (
        "        # ── Page 3: Certificate of Appreciation ───────────────────────────────\n"
        "        story.append(Spacer(1, 1.6*inch))   # vertical centre\n"
        "        story.append(HRFlowable(width='85%', thickness=2.5, color=Brand.GOLD,\n"
        "                                spaceAfter=22, lineCap='round'))\n"
        "        story.append(Paragraph('Certificate of Appreciation', s['cover_title']))\n"
        "        story.append(Spacer(1, 0.14*inch))\n"
        "        story.append(Paragraph('This certifies that', s['cover_sub']))\n"
        "        story.append(Spacer(1, 0.2*inch))\n"
        "        # Clean single name-line (no stacked rules)\n"
        "        story.append(HRFlowable(width=3.5*inch, thickness=1.0,\n"
        "                                color=Brand.ROSE_GOLD, spaceAfter=14))\n"
        "        story.append(Paragraph('is officially the', s['cover_sub']))\n"
        "        story.append(Spacer(1, 0.1*inch))\n"
        "        story.append(Paragraph(\"World's Greatest Mom\", s['cover_title']))\n"
        "        story.append(Spacer(1, 0.28*inch))\n"
        "        story.append(Paragraph(\n"
        "            'Awarded with love, gratitude, and absolutely zero conditions.',\n"
        "            s['cover_tag']))\n"
        "        story.append(Spacer(1, 0.38*inch))\n"
        "        story.append(HRFlowable(width='85%', thickness=2.5, color=Brand.GOLD,\n"
        "                                lineCap='round'))"
)

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

assert OLD in src, 'ERROR: certificate block not found — check for prior patches'
src = src.replace(OLD, NEW, 1)

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

print('Certificate layout patched.')
print('  Spacer        0.8" -> 1.6" (vertical centre)')
print('  Name field    HR(60%)+underscores -> single HR(3.5") name line')
print('  Spacing       explicit Spacers between every element')
print('  launch_build.py:', os.path.getsize('launch_build.py'), 'bytes')
