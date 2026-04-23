#!/usr/bin/env python3
"""Writes the full launch_build.py with SKU 1 & 2 Platypus implementations."""
import os

LAUNCH = """# launch_build.py — Mom Rescue Pack | Run locally: python3 launch_build.py
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether, Flowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
import os

# ── Brand ──────────────────────────────────────────────────────────────────────
class Brand:
    BLUSH     = HexColor('#F9B8C0')
    ROSE_GOLD = HexColor('#B76E79')
    PLUM      = HexColor('#6B2D5E')
    CREAM     = HexColor('#FFF8F0')
    SAGE      = HexColor('#A8C5A0')
    GOLD      = HexColor('#D4A574')
    CHARCOAL  = HexColor('#3A3A3A')
    MARGIN    = 0.25 * inch
    W, H      = letter
    OUT       = 'products'
    LOGO      = 'mom-rescue-pack-logo.jpeg'
    URL       = 'momrescuepack.com'

# ── Vector Coupon Card Flowable ────────────────────────────────────────────────
class CouponCard(Flowable):
    CW = 7.0 * inch
    CH = 2.2 * inch

    def __init__(self, title, desc, number):
        Flowable.__init__(self)
        self.title  = title
        self.desc   = desc
        self.number = number

    def wrap(self, aW, aH):
        return self.CW, self.CH

    def draw(self):
        c = self.canv
        w, h, pad = self.CW, self.CH, 10

        # Cream fill
        c.setFillColor(HexColor('#FFF8F0'))
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Dashed rose-gold border
        c.saveState()
        c.setDash(8, 5)
        c.setStrokeColor(HexColor('#B76E79'))
        c.setLineWidth(1.5)
        c.rect(pad, pad, w - 2*pad, h - 2*pad, fill=0, stroke=1)
        c.restoreState()

        # Scissors line
        c.setFont('Helvetica', 7)
        c.setFillColor(HexColor('#D4A574'))
        c.drawString(pad + 4, h - pad - 10, '\\u2702  \\u2014\\u2014\\u2014\\u2014\\u2014\\u2014\\u2014\\u2014\\u2014\\u2014\\u2014\\u2014')

        # Numbered badge
        c.setFillColor(HexColor('#6B2D5E'))
        c.circle(w - pad - 22, h - pad - 22, 15, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(white)
        c.drawCentredString(w - pad - 22, h - pad - 26, '#%02d' % self.number)

        # Title
        c.setFont('Helvetica-Bold', 17)
        c.setFillColor(HexColor('#6B2D5E'))
        c.drawCentredString(w / 2, h - 58, self.title)

        # Gold dashed divider
        c.saveState()
        c.setStrokeColor(HexColor('#D4A574'))
        c.setLineWidth(0.75)
        c.setDash(3, 3)
        c.line(w * 0.25, h - 70, w * 0.75, h - 70)
        c.restoreState()

        # Description
        c.setFont('Helvetica', 11)
        c.setFillColor(HexColor('#3A3A3A'))
        c.drawCentredString(w / 2, h - 90, self.desc)

        # Footer stamp
        c.setFont('Helvetica-Oblique', 7)
        c.setFillColor(HexColor('#B76E79'))
        c.drawCentredString(w / 2, pad + 8, 'MOM RESCUE PACK  \\u2022  Gift Certificate')


# ── 7-Day Week Grid ────────────────────────────────────────────────────────────
def make_week_grid(styles):
    days  = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    slots = ['Morning', 'Midday', 'Afternoon', 'Evening', 'Self-Care']
    col_w = (7.5 * inch) / 7

    data = [[Paragraph('<b>' + d + '</b>', styles['day_hdr']) for d in days]]
    for slot in slots:
        data.append([
            Paragraph('<font size="7" color="#B76E79">' + slot + '</font><br/>',
                      styles['cell'])
            for _ in days
        ])

    tbl = Table(data, colWidths=[col_w] * 7,
                rowHeights=[0.35 * inch] + [0.55 * inch] * len(slots))
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0),  HexColor('#6B2D5E')),
        ('TEXTCOLOR',  (0, 0), (-1, 0),  white),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#FFF8F0')),
        ('GRID',       (0, 0), (-1, -1), 0.5, HexColor('#D4A574')),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]))
    return tbl


# ── Builder ────────────────────────────────────────────────────────────────────
class MomRescueBuilder:

    def __init__(self):
        self.styles = self._make_styles()

    def _make_styles(self):
        def s(name, **kw):
            return ParagraphStyle(name, **kw)
        return {
            'cover_title': s('ct', fontSize=32, textColor=HexColor('#6B2D5E'),
                             alignment=TA_CENTER, spaceAfter=8, fontName='Helvetica-Bold'),
            'cover_sub':   s('cs', fontSize=16, textColor=HexColor('#B76E79'),
                             alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica-Oblique'),
            'cover_price': s('cp', fontSize=22, textColor=HexColor('#D4A574'),
                             alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold'),
            'cover_tag':   s('cg', fontSize=11, textColor=HexColor('#3A3A3A'),
                             alignment=TA_CENTER, fontName='Helvetica'),
            'section_hdr': s('sh', fontSize=14, textColor=HexColor('#6B2D5E'),
                             alignment=TA_CENTER, spaceBefore=10, spaceAfter=6,
                             fontName='Helvetica-Bold'),
            'body':        s('bd', fontSize=10, textColor=HexColor('#3A3A3A'),
                             alignment=TA_LEFT, fontName='Helvetica'),
            'day_hdr':     s('dh', fontSize=9, textColor=white,
                             alignment=TA_CENTER, fontName='Helvetica-Bold'),
            'cell':        s('cl', fontSize=8, textColor=HexColor('#3A3A3A'),
                             alignment=TA_CENTER, fontName='Helvetica'),
            'habit_label': s('hl', fontSize=9, textColor=HexColor('#6B2D5E'),
                             alignment=TA_LEFT, fontName='Helvetica-Bold'),
        }

    def _header_footer(self, canv, doc, title='Mom Rescue Pack'):
        canv.saveState()
        m, w, h = Brand.MARGIN, Brand.W, Brand.H

        # Plum header bar
        canv.setFillColor(Brand.PLUM)
        canv.rect(m, h - m - 0.45*inch, w - 2*m, 0.45*inch, fill=1, stroke=0)

        # Logo (embedded if present)
        if os.path.exists(Brand.LOGO):
            canv.drawImage(Brand.LOGO, m + 4, h - m - 0.42*inch,
                           width=0.38*inch, height=0.38*inch,
                           preserveAspectRatio=True, mask='auto')

        canv.setFont('Helvetica-Bold', 10)
        canv.setFillColor(white)
        canv.drawString(m + 0.48*inch, h - m - 0.29*inch, 'MOM RESCUE PACK')

        canv.setFont('Helvetica', 9)
        canv.drawRightString(w - m - 4, h - m - 0.29*inch, title)

        # Gold footer rule
        canv.setStrokeColor(Brand.GOLD)
        canv.setLineWidth(0.75)
        canv.line(m, m + 0.3*inch, w - m, m + 0.3*inch)

        canv.setFont('Helvetica-Oblique', 7)
        canv.setFillColor(Brand.ROSE_GOLD)
        canv.drawCentredString(w / 2, m + 0.12*inch, Brand.URL)

        canv.setFont('Helvetica', 7)
        canv.setFillColor(Brand.CHARCOAL)
        canv.drawRightString(w - m, m + 0.12*inch, 'p. %d' % doc.page)
        canv.restoreState()

    def create_cover_page(self, title, subtitle, price, tagline):
        s = self.styles
        return [
            Spacer(1, 1.6 * inch),
            HRFlowable(width='80%', thickness=2, color=Brand.GOLD,
                       spaceAfter=18, lineCap='round'),
            Paragraph(title,    s['cover_title']),
            Paragraph(subtitle, s['cover_sub']),
            Spacer(1, 0.2 * inch),
            HRFlowable(width='40%', thickness=0.75, color=Brand.ROSE_GOLD, spaceAfter=10),
            Paragraph(price,   s['cover_price']),
            Spacer(1, 0.15 * inch),
            Paragraph(tagline, s['cover_tag']),
            HRFlowable(width='80%', thickness=2, color=Brand.GOLD, spaceBefore=20),
        ]

    # ── SKU 1: Last-Minute Dad's Gift Kit — Coupon Book ($17) ──────────────────
    def build_coupon_book(self):
        path = os.path.join(Brand.OUT, 'sku1_coupon_book.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, "Last-Minute Dad's Gift Kit")

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=m, rightMargin=m,
                  topMargin=m + 0.6*inch, bottomMargin=m + 0.55*inch)

        story = self.create_cover_page(
            "Last-Minute Dad's Gift Kit",
            '8 Heartfelt Coupons for Mom',
            '$17',
            'Because she deserves every single one.')
        story.append(PageBreak())

        coupons = [
            ('One Day of Total Silence',       'Good for one blissful day of peace and quiet.'),
            ('Breakfast in Bed',               'Pancakes, coffee, and zero interruptions.'),
            ('Uninterrupted Bath Time',        '60 glorious minutes — no knocking allowed.'),
            ('Full TV Remote Control',         'Mom picks everything. No negotiations.'),
            ('A Genuine Heartfelt Apology',    'Redeemable anytime. No questions asked.'),
            ('One Full Day Off from Cooking',  'Takeout night officially approved.'),
            ('Kids to Bed On Time — No Drama', 'All kids, on schedule, guaranteed.'),
            ('30-Minute Foot Massage',         'From the person who loves you most.'),
        ]

        story.append(Paragraph(
            '<b>Your Gift Coupon Collection</b> — Cut along the dashed lines.',
            self.styles['section_hdr']))
        story.append(Spacer(1, 0.15 * inch))

        for i, (title, desc) in enumerate(coupons):
            story.append(CouponCard(title, desc, i + 1))
            story.append(Spacer(1, 0.22 * inch))
            if (i + 1) % 3 == 0 and i + 1 < len(coupons):
                story.append(PageBreak())

        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        print('  OK  SKU 1 ->', path)

    # ── SKU 2: Daily Sanity Planner — Self-Care Bundle ($27) ───────────────────
    def build_daily_planner(self):
        path = os.path.join(Brand.OUT, 'sku2_daily_planner.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, 'Daily Sanity Planner')

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=m, rightMargin=m,
                  topMargin=m + 0.6*inch, bottomMargin=m + 0.55*inch)

        s     = self.styles
        story = self.create_cover_page(
            'Daily Sanity Planner',
            'Your Weekly Self-Care System',
            '$27',
            '7 days. One calm, intentional week.')
        story.append(PageBreak())

        # Weekly overview grid
        story.append(Paragraph('Weekly Overview', s['section_hdr']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(make_week_grid(s))
        story.append(PageBreak())

        # Daily schedule pages (one per day)
        days_full  = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                      'Friday', 'Saturday', 'Sunday']
        time_slots = ['6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
                      '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM',
                      '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM']

        for day in days_full:
            story.append(Paragraph(day, s['section_hdr']))
            story.append(HRFlowable(width='100%', thickness=0.5,
                                    color=Brand.ROSE_GOLD, spaceAfter=6))

            rows = [[Paragraph('<b>' + t + '</b>', s['body']),
                     Paragraph('', s['body'])] for t in time_slots]
            tbl = Table(rows, colWidths=[0.9 * inch, 6.6 * inch],
                        rowHeights=[0.28 * inch] * len(rows))
            tbl.setStyle(TableStyle([
                ('FONTSIZE',     (0, 0), (-1, -1), 9),
                ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
                ('TEXTCOLOR',    (0, 0), (0,  -1), Brand.PLUM),
                ('LINEBELOW',    (1, 0), (1,  -1), 0.4, Brand.GOLD),
                ('BACKGROUND',   (0, 0), (-1, -1), Brand.CREAM),
                ('LEFTPADDING',  (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 0.15 * inch))

            # Self-care intention box
            ibox = Table([[
                Paragraph("<b>Today's Self-Care Intention:</b>", s['habit_label']),
                Paragraph('', s['body'])
            ]], colWidths=[2.2 * inch, 5.3 * inch], rowHeights=[0.35 * inch])
            ibox.setStyle(TableStyle([
                ('BACKGROUND',   (0, 0), (-1, -1), HexColor('#FAF0F4')),
                ('BOX',          (0, 0), (-1, -1), 0.75, Brand.ROSE_GOLD),
                ('LEFTPADDING',  (0, 0), (-1, -1), 8),
                ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(ibox)
            story.append(PageBreak())

        # Habit Tracker (31-day grid)
        story.append(Paragraph('Monthly Habit Tracker', s['section_hdr']))
        story.append(Spacer(1, 0.1 * inch))
        habits = [
            'Drink 8 glasses of water',
            'Move my body for 20 min',
            'Read for 15 minutes',
            'Journalled / reflected',
            'Said no to something',
            'Did one thing just for me',
        ]
        hdata = [['Habit'] + [str(i) for i in range(1, 32)]]
        hdata += [[h] + [''] * 31 for h in habits]
        htbl = Table(hdata,
                     colWidths=[1.8 * inch] + [0.18 * inch] * 31,
                     rowHeights=[0.3 * inch] * (len(habits) + 1))
        htbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0),  Brand.PLUM),
            ('TEXTCOLOR',  (0, 0), (-1, 0),  white),
            ('FONTNAME',   (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',   (0, 0), (-1, -1), 7),
            ('ALIGN',      (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID',       (0, 0), (-1, -1), 0.3, Brand.GOLD),
            ('BACKGROUND', (0, 1), (-1, -1), Brand.CREAM),
            ('LEFTPADDING',(0, 1), (0,  -1), 4),
        ]))
        story.append(htbl)
        story.append(PageBreak())

        # Notes page
        story.append(Paragraph('Notes & Reflections', s['section_hdr']))
        for _ in range(18):
            story.append(HRFlowable(width='100%', thickness=0.4,
                                    color=Brand.GOLD, spaceAfter=18))

        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        print('  OK  SKU 2 ->', path)


if __name__ == '__main__':
    os.makedirs(Brand.OUT, exist_ok=True)
    b = MomRescueBuilder()
    print('Building SKU 1 ...')
    b.build_coupon_book()
    print('Building SKU 2 ...')
    b.build_daily_planner()
    print('\\nAll done! Check the products/ folder.')
"""

with open('launch_build.py', 'w', encoding='utf-8') as f:
    f.write(LAUNCH)

size  = os.path.getsize('launch_build.py')
lines = LAUNCH.count('\n')
print(f'launch_build.py written — {size:,} bytes, {lines} lines')
