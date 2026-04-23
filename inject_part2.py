#!/usr/bin/env python3
"""Appends SKU 3, 4, 5 + run_all to launch_build.py; replaces __main__ block."""
import os

NEW_CODE = """
    # ── SKU 3: Mother's Day Card Pack — 5 A2 Foldable Cards ($9) ──────────────
    def build_card_pack(self):
        from reportlab.pdfgen import canvas as pdfcanvas
        path = os.path.join(Brand.OUT, 'sku3_card_pack.pdf')
        PAGE = (5.5 * inch, 8.5 * inch)   # flat A2 sheet: fold at 4.25"

        cards = [
            ("Happy Mother's Day",   "Wishing you the most wonderful day, Mom."),
            ("World's Best Mom",     "There is no one quite like you."),
            ("Thank You, Mom",       "For every hug, every sacrifice, every smile."),
            ("You Are My Sunshine",  "Thank you for always being my light."),
            ("I Love You, Mom",      "More than words could ever say."),
        ]

        c = pdfcanvas.Canvas(path, pagesize=PAGE)
        w, h = PAGE
        mid = h / 2        # fold line

        for title, msg in cards:
            # Corner cut marks
            c.setStrokeColor(Brand.CHARCOAL)
            c.setLineWidth(0.4)
            for cx, cy, dx, dy in [
                (0, h, 1, 0), (0, h, 0, -1),
                (w, h, -1, 0), (w, h, 0, -1),
                (0, 0, 1, 0), (0, 0, 0, 1),
                (w, 0, -1, 0), (w, 0, 0, 1),
            ]:
                c.line(cx, cy, cx + dx * 0.18 * inch, cy + dy * 0.18 * inch)

            # Dashed fold line
            c.saveState()
            c.setDash(6, 4)
            c.setStrokeColor(Brand.ROSE_GOLD)
            c.setLineWidth(0.75)
            c.line(0, mid, w, mid)
            c.restoreState()
            c.setFont('Helvetica', 6)
            c.setFillColor(Brand.ROSE_GOLD)
            c.drawCentredString(w / 2, mid + 3, 'FOLD HERE')

            # ── Card Front (top half) ──────────────────────────────────────────
            pad = 0.15 * inch
            c.setFillColor(Brand.PLUM)
            c.rect(pad, mid + pad, w - 2*pad, mid - 2*pad, fill=1, stroke=0)

            # Decorative blush circles
            c.setFillColor(Brand.BLUSH)
            c.circle(0.45*inch, mid + 0.45*inch, 0.28*inch, fill=1, stroke=0)
            c.circle(w - 0.45*inch, h - 0.45*inch, 0.28*inch, fill=1, stroke=0)
            c.setFillColor(Brand.GOLD)
            c.circle(w / 2, h - 0.5*inch, 0.12*inch, fill=1, stroke=0)

            # Card title
            c.setFont('Helvetica-Bold', 19)
            c.setFillColor(white)
            c.drawCentredString(w / 2, mid + mid / 2 + 0.08*inch, title)

            # Gold dashed accent line
            c.saveState()
            c.setStrokeColor(Brand.GOLD)
            c.setLineWidth(0.8)
            c.setDash(4, 3)
            c.line(w * 0.22, mid + mid / 2 - 0.1*inch, w * 0.78, mid + mid / 2 - 0.1*inch)
            c.restoreState()

            c.setFont('Helvetica', 7)
            c.setFillColor(Brand.BLUSH)
            c.drawCentredString(w / 2, mid + 0.28*inch, 'MOM RESCUE PACK')

            # ── Card Inside (bottom half — rotated 180 so it reads when folded) ─
            c.saveState()
            c.translate(w / 2, mid / 2)
            c.rotate(180)
            c.translate(-w / 2, -mid / 2)

            c.setFillColor(Brand.CREAM)
            c.rect(pad, pad, w - 2*pad, mid - 2*pad, fill=1, stroke=0)

            c.setStrokeColor(Brand.ROSE_GOLD)
            c.setLineWidth(1)
            c.rect(pad + 0.1*inch, pad + 0.1*inch,
                   w - 2*(pad + 0.1*inch), mid - 2*(pad + 0.1*inch),
                   fill=0, stroke=1)

            c.setFont('Helvetica-BoldOblique', 12)
            c.setFillColor(Brand.PLUM)
            c.drawCentredString(w / 2, mid * 0.62, msg)

            c.setFont('Helvetica', 9)
            c.setFillColor(Brand.CHARCOAL)
            c.drawCentredString(w / 2, mid * 0.35, 'With love,')
            c.setStrokeColor(Brand.GOLD)
            c.setLineWidth(0.5)
            c.line(w * 0.28, mid * 0.26, w * 0.72, mid * 0.26)

            c.restoreState()
            c.showPage()

        c.save()
        print('  OK  SKU 3 ->', path)

    # ── SKU 4: Activity Pack ($12) ─────────────────────────────────────────────
    def build_activity_pack(self):
        path = os.path.join(Brand.OUT, 'sku4_activity_pack.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, 'Mom Activity Pack')

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=m, rightMargin=m,
                  topMargin=m + 0.6*inch, bottomMargin=m + 0.55*inch)
        s     = self.styles
        story = []

        # ── Page 1: All About Mom Interview ───────────────────────────────────
        story.append(Paragraph('All About Mom', s['section_hdr']))
        story.append(Paragraph('A love letter in questions — fill this out together!',
                               s['cover_tag']))
        story.append(Spacer(1, 0.2*inch))

        questions = [
            "Mom's full name is:",
            "Mom's favorite color is:",
            "Mom's favorite meal is:",
            "The thing Mom does best is:",
            "Mom always says:",
            "Mom's superpower is:",
            "If Mom had a whole day to herself she would:",
            "The best thing Mom ever taught me is:",
            "Mom is happiest when:",
            "I love Mom because:",
            "Mom's funniest moment was:",
            "When I grow up I want to be like Mom because:",
        ]
        for q in questions:
            story.append(Paragraph(q, s['habit_label']))
            story.append(HRFlowable(width='100%', thickness=0.4,
                                    color=Brand.GOLD, spaceAfter=4))
            story.append(Spacer(1, 0.08*inch))
        story.append(PageBreak())

        # ── Page 2: Household Scavenger Hunt ──────────────────────────────────
        story.append(Paragraph('Household Scavenger Hunt', s['section_hdr']))
        story.append(Paragraph('Find these things that make Mom who she is!',
                               s['cover_tag']))
        story.append(Spacer(1, 0.18*inch))

        hunt = [
            'Something Mom uses every morning',
            "Mom's favorite snack",
            'Something Mom has read',
            'A photo Mom loves',
            'Something Mom has fixed',
            "Mom's go-to comfort item",
            'Something that smells like Mom',
            'A note or list Mom has written',
            'Something Mom has made by hand',
            "Mom's most-used kitchen item",
            'Something that makes Mom laugh',
            'A treasure Mom has kept for years',
        ]
        hdata = [['#', 'Find This...', 'Found?  Location']]
        hdata += [[str(i+1), item, ''] for i, item in enumerate(hunt)]
        htbl = Table(hdata, colWidths=[0.35*inch, 4.0*inch, 3.15*inch],
                     rowHeights=[0.3*inch] + [0.36*inch]*len(hunt))
        htbl.setStyle(TableStyle([
            ('BACKGROUND',  (0,0), (-1,0), Brand.PLUM),
            ('TEXTCOLOR',   (0,0), (-1,0), white),
            ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',    (0,0), (-1,-1), 9),
            ('ALIGN',       (0,0), (0,-1), 'CENTER'),
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('GRID',        (0,0), (-1,-1), 0.4, Brand.GOLD),
            ('BACKGROUND',  (0,1), (-1,-1), Brand.CREAM),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(htbl)
        story.append(PageBreak())

        # ── Page 3: Certificate of Appreciation ───────────────────────────────
        story.append(Spacer(1, 0.8*inch))
        story.append(HRFlowable(width='90%', thickness=2,
                                color=Brand.GOLD, spaceAfter=20))
        story.append(Paragraph('Certificate of Appreciation', s['cover_title']))
        story.append(Paragraph('This certifies that', s['cover_sub']))
        story.append(HRFlowable(width='60%', thickness=0.75,
                                color=Brand.ROSE_GOLD, spaceAfter=6))
        story.append(Paragraph('________________________________', s['cover_price']))
        story.append(Paragraph('is officially the', s['cover_sub']))
        story.append(Paragraph("World's Greatest Mom", s['cover_title']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            'Awarded with love, gratitude, and absolutely zero conditions.',
            s['cover_tag']))
        story.append(HRFlowable(width='90%', thickness=2,
                                color=Brand.GOLD, spaceBefore=30))
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        print('  OK  SKU 4 ->', path)

    # ── SKU 5: Mom Rescue Pack User Manual ($37) ───────────────────────────────
    def build_mom_manual(self):
        path = os.path.join(Brand.OUT, 'sku5_mom_manual.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, 'Mom Rescue Pack Manual')

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=m, rightMargin=m,
                  topMargin=m + 0.6*inch, bottomMargin=m + 0.55*inch)
        s     = self.styles
        story = self.create_cover_page(
            'Mom Rescue Pack',
            'Official User Manual — 2025 Edition',
            '$37 Value',
            'Everything you need to run this household like a pro.')
        story.append(PageBreak())

        # ── Page 2: Quick Reference / Emergency Protocols ─────────────────────
        story.append(Paragraph('Emergency Quick-Reference Guide', s['section_hdr']))
        story.append(Spacer(1, 0.1*inch))
        ref = [
            ['Situation',               'Deploy Coupon',               'Level'],
            ['Mom needs silence',        '#1 — Total Silence',          'CRITICAL'],
            ['Breakfast not made',       '#2 — Breakfast in Bed',       'Level 1'],
            ['Bath time interrupted',    '#3 — Uninterrupted Bath',     'Level 2'],
            ['Too much screen time',     '#4 — Full Remote Control',    'Level 1'],
            ['Argument happened',        '#5 — Heartfelt Apology',      'Level 2'],
            ['Dinner not made',          '#6 — Day Off Cooking',        'Level 1'],
            ['Bedtime chaos',            '#7 — Kids On Time, No Drama', 'Level 2'],
            ['Mom looks exhausted',      '#8 — Foot Massage',           'Level 1'],
        ]
        rtbl = Table(ref, colWidths=[2.5*inch, 2.6*inch, 2.4*inch],
                     rowHeights=[0.32*inch]*len(ref))
        rtbl.setStyle(TableStyle([
            ('BACKGROUND',  (0,0), (-1,0), Brand.PLUM),
            ('TEXTCOLOR',   (0,0), (-1,0), white),
            ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',    (0,0), (-1,-1), 9),
            ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('GRID',        (0,0), (-1,-1), 0.4, Brand.GOLD),
            ('BACKGROUND',  (0,1), (-1,-1), Brand.CREAM),
            ('TEXTCOLOR',   (2,1), (2,1),  Brand.PLUM),
            ('FONTNAME',    (2,1), (2,1),  'Helvetica-Bold'),
        ]))
        story.append(rtbl)
        story.append(PageBreak())

        # ── Page 3: Standard Operating Procedures ─────────────────────────────
        story.append(Paragraph('Standard Operating Procedures', s['section_hdr']))
        story.append(Spacer(1, 0.1*inch))
        sops = [
            ('SOP-001: Morning Activation',
             'Mom is to be greeted with coffee before any requests are made. '
             'A minimum 30-minute warm-up period applies on all weekends.'),
            ('SOP-002: Noise Management',
             'Volume above Level 7 is prohibited until Mom has consumed her '
             'first full cup of coffee. Violations result in immediate chores.'),
            ('SOP-003: Meal Scheduling',
             "Mom's meal preferences take priority on Mother's Day and all "
             'Coupon Days. No negotiations. No substitutions.'),
            ('SOP-004: Self-Care Maintenance',
             'This household is required to actively support the Daily Sanity '
             'Planner routine. Disruptions require a written apology.'),
            ('SOP-005: Appreciation Protocol',
             'Verbal appreciation is mandatory. Written appreciation via the '
             'included greeting cards is strongly encouraged.'),
            ('SOP-006: Emergency Response',
             'On Mom reaching Overwhelm Status, deploy Coupon #1 immediately '
             'and remove all children from the immediate vicinity.'),
        ]
        for code, desc in sops:
            story.append(KeepTogether([
                Paragraph(code, s['habit_label']),
                Paragraph(desc, s['body']),
                Spacer(1, 0.1*inch),
                HRFlowable(width='100%', thickness=0.3,
                           color=Brand.GOLD, spaceAfter=8),
            ]))
        story.append(PageBreak())

        # ── Page 4: Maintenance Schedule + Thank You ──────────────────────────
        story.append(Paragraph('Maintenance Schedule', s['section_hdr']))
        story.append(Spacer(1, 0.1*inch))
        maint = [
            ['Frequency',  'Action Required',                     'Owner'],
            ['Daily',      'Express gratitude to Mom',            'Everyone'],
            ['Weekly',     'Complete one Planner self-care block','Mom + family'],
            ['Monthly',    'Review habit tracker progress',       'Mom'],
            ['Quarterly',  'Refresh & reprint coupon book',       'Dad / Kids'],
            ['Annually',   'Full Mom Appreciation Day',           'Whole family'],
            ['As needed',  'Deploy emergency coupon at once',     'First available'],
        ]
        mtbl = Table(maint, colWidths=[1.5*inch, 3.5*inch, 2.5*inch],
                     rowHeights=[0.32*inch]*len(maint))
        mtbl.setStyle(TableStyle([
            ('BACKGROUND',  (0,0), (-1,0), Brand.PLUM),
            ('TEXTCOLOR',   (0,0), (-1,0), white),
            ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',    (0,0), (-1,-1), 9),
            ('ALIGN',       (0,0), (0,-1), 'CENTER'),
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('GRID',        (0,0), (-1,-1), 0.4, Brand.GOLD),
            ('BACKGROUND',  (0,1), (-1,-1), Brand.CREAM),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(mtbl)
        story.append(Spacer(1, 0.4*inch))
        story.append(HRFlowable(width='80%', thickness=1.5,
                                color=Brand.GOLD, spaceAfter=16))
        story.append(Paragraph('Thank You & Your Bundle Summary', s['section_hdr']))
        story.append(Paragraph(
            'Thank you for choosing the Mom Rescue Pack. Designed with one goal: '
            'give moms the recognition, rest, and resources they deserve.<br/><br/>'
            '<b>Your 5-SKU bundle includes:</b><br/>'
            '&bull; SKU 1 — Last-Minute Dad Gift Kit (Coupon Book)<br/>'
            '&bull; SKU 2 — Daily Sanity Planner (Self-Care Bundle)<br/>'
            '&bull; SKU 3 — Mother\'s Day Card Pack (5 A2 Foldable Cards)<br/>'
            '&bull; SKU 4 — Activity Pack (Interview + Scavenger Hunt)<br/>'
            '&bull; SKU 5 — This Official User Manual<br/><br/>'
            'Print once. Use forever. Share with a mom who deserves it.',
            s['body']))
        story.append(Spacer(1, 0.3*inch))
        story.append(HRFlowable(width='80%', thickness=1.5, color=Brand.GOLD))
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        print('  OK  SKU 5 ->', path)

    # ── Run All 5 SKUs ─────────────────────────────────────────────────────────
    def run_all(self):
        os.makedirs(Brand.OUT, exist_ok=True)
        print('Mom Rescue Pack — Building all 5 SKUs...')
        for label, fn in [
            ('SKU 1: Coupon Book',    self.build_coupon_book),
            ('SKU 2: Daily Planner',  self.build_daily_planner),
            ('SKU 3: Card Pack',      self.build_card_pack),
            ('SKU 4: Activity Pack',  self.build_activity_pack),
            ('SKU 5: User Manual',    self.build_mom_manual),
        ]:
            print('Building', label, '...')
            fn()
        print('\\nAll 5 SKUs complete! Check the products/ folder.')


if __name__ == '__main__':
    MomRescueBuilder().run_all()
"""

MARKER = "if __name__ == '__main__':"

with open('launch_build.py', encoding='utf-8') as f:
    src = f.read()

idx = src.index(MARKER)
src = src[:idx] + NEW_CODE

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(src)

size  = os.path.getsize('launch_build.py')
lines = src.count('\n')
print('launch_build.py: %d bytes, %d lines' % (size, lines))
