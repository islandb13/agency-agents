# launch_build.py — Mom Rescue Pack | Run locally: python3 launch_build.py
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
        c.drawString(pad + 4, h - pad - 10, '\u2702  \u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014')

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
        c.drawCentredString(w / 2, pad + 8, 'MOM RESCUE PACK  \u2022  Gift Certificate')


class CanvaCover(Flowable):
    """Full-page Canva-exported cover. Header/footer is suppressed on this page."""
    def __init__(self, path):
        Flowable.__init__(self)
        self._path = path
    def wrap(self, aW, aH):
        return aW, aH
    def draw(self):
        self.canv.drawImage(
            self._path,
            -(0.75 * inch), -(0.80 * inch),
            width=Brand.W, height=Brand.H,
            preserveAspectRatio=False, mask=None
        )


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
        self._has_cover = False  # set True by create_cover_page
        self._skip_header_p1 = False  # True when full Canva cover PNG is used

    def _make_styles(self):
        def s(name, **kw):
            return ParagraphStyle(name, **kw)
        return {
            'cover_title': s('ct', fontSize=28, leading=35,
                             textColor=HexColor('#6B2D5E'), alignment=TA_CENTER,
                             spaceAfter=30, fontName='Helvetica-Bold', charSpace=1.5),
            'cover_sub':   s('cs', fontSize=16, leading=20,
                             textColor=HexColor('#B76E79'),
                             alignment=TA_CENTER, spaceAfter=10, fontName='Helvetica-Oblique'),
            'cover_price': s('cp', fontSize=22, textColor=HexColor('#D4A574'),
                             alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold'),
            'cover_tag':   s('cg', fontSize=11, textColor=HexColor('#3A3A3A'),
                             alignment=TA_CENTER, fontName='Helvetica'),
            'section_hdr': s('sh', fontSize=14, textColor=HexColor('#6B2D5E'),
                             alignment=TA_CENTER, spaceBefore=10, spaceAfter=6,
                             fontName='Helvetica-Bold'),
            'body':        s('bd', fontSize=10, leading=14,
                             textColor=HexColor('#3A3A3A'),
                             alignment=TA_LEFT, fontName='Helvetica'),
            'day_hdr':     s('dh', fontSize=9, textColor=white,
                             alignment=TA_CENTER, fontName='Helvetica-Bold'),
            'cell':        s('cl', fontSize=8, textColor=HexColor('#3A3A3A'),
                             alignment=TA_CENTER, fontName='Helvetica'),
            'habit_label': s('hl', fontSize=9, textColor=HexColor('#6B2D5E'),
                             alignment=TA_LEFT, fontName='Helvetica-Bold'),
            # Cover-with-background variants (used on page 1 over cover_bg.png)
            'cover_title_dk': s('ctdk', fontSize=28, leading=35,
                                textColor=HexColor('#6B2D5E'), alignment=TA_CENTER,
                                spaceAfter=30, fontName='Helvetica-Bold', charSpace=1.5),
            'cover_sub_dk':   s('csdk', fontSize=16, leading=20,
                                textColor=HexColor('#B76E79'), alignment=TA_CENTER,
                                spaceAfter=10, fontName='Helvetica-Oblique'),
            'cover_price_dk': s('cpdk', fontSize=22, textColor=HexColor('#C4963A'),
                                alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold'),
            'cover_tag_dk':   s('cgdk', fontSize=11, textColor=HexColor('#3A3A3A'),
                                alignment=TA_CENTER, fontName='Helvetica'),
        }

    def _header_footer(self, canv, doc, title='Mom Rescue Pack'):
        canv.saveState()
        m, w, h = Brand.MARGIN, Brand.W, Brand.H
        if self._skip_header_p1 and doc.page == 1:
            canv.restoreState()
            return

        # ── AI Premium Backgrounds (graceful fallback if absent) ─────────
        _cover_bg   = os.path.join('assets', 'backgrounds', 'cover_bg.png')
        _content_bg = os.path.join('assets', 'backgrounds', 'content_bg.png')
        if self._has_cover and doc.page == 1 and os.path.exists(_cover_bg):
            canv.drawImage(_cover_bg, 0, 0, width=w, height=h,
                          preserveAspectRatio=False, mask=None)
        elif os.path.exists(_content_bg) and not (self._has_cover and doc.page == 1):
            canv.drawImage(_content_bg, 0, 0, width=w, height=h,
                          preserveAspectRatio=False, mask=None)

        # Gold double-rule header (Option D — Classic Gold Foil)
        canv.setStrokeColor(Brand.GOLD)
        canv.setLineWidth(1.8)
        canv.line(m, h - m - 0.06*inch, w - m, h - m - 0.06*inch)
        canv.setLineWidth(0.4)
        canv.line(m, h - m - 0.12*inch, w - m, h - m - 0.12*inch)

        # Logo: prefer PNG (transparent bg) over JPEG
        _logo = next((f for f in [
            'mom-rescue-pack-logo.png',
            Brand.LOGO,
        ] if os.path.exists(f)), None)
        if _logo:
            canv.drawImage(_logo, m + 4, h - m - 0.44*inch,
                           width=0.30*inch, height=0.30*inch,
                           preserveAspectRatio=True, mask='auto')

        canv.setFont('Helvetica-Bold', 9)
        canv.setFillColor(Brand.PLUM)
        canv.drawString(m + 0.42*inch, h - m - 0.32*inch, 'MOM RESCUE PACK')

        canv.setFont('Helvetica-Oblique', 9)
        canv.setFillColor(Brand.ROSE_GOLD)
        canv.drawRightString(w - m - 4, h - m - 0.32*inch, title)

        canv.setStrokeColor(Brand.GOLD)
        canv.setLineWidth(0.4)
        canv.line(m, h - m - 0.46*inch, w - m, h - m - 0.46*inch)

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
        self._has_cover = True   # tells _header_footer page 1 is a cover
        s  = self.styles
        dk = os.path.exists(os.path.join('assets', 'backgrounds', 'cover_bg.png'))
        return [
            Spacer(1, 1.6 * inch),
            HRFlowable(width='80%', thickness=1.5, color=Brand.GOLD,
                       spaceAfter=18, lineCap='round'),
            Paragraph(title,    s['cover_title_dk']   if dk else s['cover_title']),
            Paragraph(subtitle, s['cover_sub_dk']     if dk else s['cover_sub']),
            Spacer(1, 0.2 * inch),
            HRFlowable(width='40%', thickness=0.75, color=Brand.GOLD, spaceAfter=10),
            Paragraph(price,   s['cover_price_dk']   if dk else s['cover_price']),
            Spacer(1, 0.15 * inch),
            Paragraph(tagline, s['cover_tag_dk']     if dk else s['cover_tag']),
            HRFlowable(width='80%', thickness=1.5, color=Brand.GOLD, spaceBefore=20),
        ]

    # ── SKU 1: Last-Minute Dad's Gift Kit — Coupon Book ($17) ──────────────────
    def build_coupon_book(self):
        self._has_cover = False
        path = os.path.join(Brand.OUT, 'sku1_coupon_book.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, "Mom's Coupon Book")

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=0.75*inch, rightMargin=0.75*inch,
                  topMargin=0.90*inch, bottomMargin=0.80*inch)

        _canva = os.path.join('assets', 'canva_covers', 'sku1.png')
        if os.path.exists(_canva):
            self._has_cover = True; self._skip_header_p1 = True
            story = [CanvaCover(_canva), PageBreak()]
        else:
            self._skip_header_p1 = False
            story = self.create_cover_page(
                "Mom's Coupon Book",
                '8 Heartfelt Gift Coupons — Just for Her',
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
        self._has_cover = False
        path = os.path.join(Brand.OUT, 'sku2_daily_planner.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, 'Daily Sanity Planner')

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=0.75*inch, rightMargin=0.75*inch,
                  topMargin=0.90*inch, bottomMargin=0.80*inch)

        s     = self.styles
        _canva = os.path.join('assets', 'canva_covers', 'sku2.png')
        if os.path.exists(_canva):
            self._has_cover = True; self._skip_header_p1 = True
            story = [CanvaCover(_canva), PageBreak()]
        else:
            self._skip_header_p1 = False
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



    # ── SKU 3: Mother's Day Card Pack — 5 A2 Foldable Cards ($9) ──────────────
    def build_card_pack(self):
        self._has_cover = False
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
        self._has_cover = False
        path = os.path.join(Brand.OUT, 'sku4_activity_pack.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, 'Mom Activity Pack')

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=0.75*inch, rightMargin=0.75*inch,
                  topMargin=0.90*inch, bottomMargin=0.80*inch)
        s     = self.styles
        _canva = os.path.join('assets', 'canva_covers', 'sku4.png')
        if os.path.exists(_canva):
            self._has_cover = True; self._skip_header_p1 = True
            story = [CanvaCover(_canva), PageBreak()]
        else:
            self._skip_header_p1 = False
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
        story.append(Spacer(1, 1.6*inch))   # vertical centre
        story.append(HRFlowable(width='85%', thickness=2.5, color=Brand.GOLD,
                                spaceAfter=22, lineCap='round'))
        story.append(Paragraph('Certificate of Appreciation', s['cover_title']))
        story.append(Spacer(1, 0.14*inch))
        story.append(Paragraph('This certifies that', s['cover_sub']))
        story.append(Spacer(1, 0.2*inch))
        # Name field: Table + LINEBELOW per project standards (premium, robust)
        _cert_name = Table([['']], colWidths=[3.5*inch], rowHeights=[0.45*inch])
        _cert_name.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 1.5, Brand.ROSE_GOLD),
        ]))
        _cert_name.hAlign = 'CENTER'
        story.append(_cert_name)
        story.append(Paragraph('is officially the', s['cover_sub']))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("World's Greatest Mom", s['cover_title']))
        story.append(Spacer(1, 0.28*inch))
        story.append(Paragraph(
            'Awarded with love, gratitude, and absolutely zero conditions.',
            s['cover_tag']))
        story.append(Spacer(1, 0.38*inch))
        story.append(HRFlowable(width='85%', thickness=2.5, color=Brand.GOLD,
                                lineCap='round'))
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        print('  OK  SKU 4 ->', path)

    # ── SKU 5: Mom Rescue Pack User Manual ($37) ───────────────────────────────
    def build_mom_manual(self):
        self._has_cover = False
        path = os.path.join(Brand.OUT, 'sku5_mom_manual.pdf')
        m    = Brand.MARGIN

        def on_page(c, doc):
            self._header_footer(c, doc, 'Mom Rescue Pack Manual')

        doc = SimpleDocTemplate(path, pagesize=letter,
                  leftMargin=0.75*inch, rightMargin=0.75*inch,
                  topMargin=0.90*inch, bottomMargin=0.80*inch)
        s     = self.styles
        _canva = os.path.join('assets', 'canva_covers', 'sku5.png')
        if os.path.exists(_canva):
            self._has_cover = True; self._skip_header_p1 = True
            story = [CanvaCover(_canva), PageBreak()]
        else:
            self._skip_header_p1 = False
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
            '&bull; SKU 1 — Mom’s Coupon Book (8 Heartfelt Gift Coupons)<br/>'
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
            ('SKU 1: Mom\'s Coupon Book', self.build_coupon_book),
            ('SKU 2: Daily Planner',  self.build_daily_planner),
            ('SKU 3: Card Pack',      self.build_card_pack),
            ('SKU 4: Activity Pack',  self.build_activity_pack),
            ('SKU 5: User Manual',    self.build_mom_manual),
        ]:
            print('Building', label, '...')
            fn()
        print('\nAll 5 SKUs complete! Check the products/ folder.')


if __name__ == '__main__':
    MomRescueBuilder().run_all()
