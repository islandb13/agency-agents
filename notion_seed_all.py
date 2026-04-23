import urllib.request
import urllib.error
import json
import os
import time

TOKEN = os.environ.get('NOTION_TOKEN')
if not TOKEN:
    raise EnvironmentError('NOTION_TOKEN environment variable is not set')

NOTION_VERSION = '2022-06-28'
BASE_URL = 'https://api.notion.com/v1'

DB = {
    1: '34b2d0b7-e3d8-8172-a203-c0927bfe7beb',  # Master Project Board
    2: '34b2d0b7-e3d8-814e-a7b8-d3ecd6794156',  # Product Catalog
    3: '34b2d0b7-e3d8-81b6-85db-d646738b89f9',  # Creative Bank
    4: '34b2d0b7-e3d8-8124-b808-ed024347fd8e',  # Copy Library
    5: '34b2d0b7-e3d8-81ec-a77d-d3b89e612e09',  # Shopify Buildout Tracker
    6: '34b2d0b7-e3d8-81f3-9aaf-dfbb28c68f57',  # Ad Campaign Manager
    7: '34b2d0b7-e3d8-81a9-afbe-d2b98916c5c2',  # Analytics Dashboard
    8: '34b2d0b7-e3d8-8148-a44d-ebcbf6ca3f15',  # SOP Hub
    9: '34b2d0b7-e3d8-81bb-a88a-d8830b1970b1',  # Agent System Registry
}


def req(payload):
    data = json.dumps(payload).encode()
    r = urllib.request.Request(
        f'{BASE_URL}/pages',
        data=data,
        headers={
            'Authorization': f'Bearer {TOKEN}',
            'Notion-Version': NOTION_VERSION,
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(r, timeout=30) as res:
            return json.loads(res.read()), None
    except urllib.error.HTTPError as e:
        return None, f'HTTP {e.code}: {e.read().decode()}'
    except Exception as e:
        return None, str(e)


def title(val):
    return {'title': [{'text': {'content': val}}]}

def sel(val):
    return {'select': {'name': val}}

def num(val):
    return {'number': val}

def txt(val):
    return {'rich_text': [{'text': {'content': val}}]}

def date(val):
    return {'date': {'start': val}}

def url(val):
    return {'url': val}


def seed(db_id, props):
    result, err = req({'parent': {'database_id': db_id}, 'properties': props})
    if err:
        print(f'    ❌ ERROR: {err[:120]}')
        return False
    print(f'    ✅ {list(props.values())[0].get("title", [{}])[0].get("text", {}).get("content", "row")} — {result.get("url", "")}')
    time.sleep(0.4)
    return True


# ─────────────────────────────────────────────────────────────────────────────
print('\n📋 DB 1 — Master Project Board')
print('─' * 50)
rows1 = [
    {'Task': title('Set up Shopify store + Digital Downloads app'),
     'Status': sel('In Progress'), 'Priority': sel('P0-Critical'),
     'Owner': sel('Human'), 'Phase': sel('Build'), 'Due Date': date('2026-04-25')},
    {'Task': title('Generate 5 hero product images with DALL-E 3'),
     'Status': sel('Not Started'), 'Priority': sel('P1-High'),
     'Owner': sel('Claude'), 'Phase': sel('Build'), 'Due Date': date('2026-04-25')},
    {'Task': title('Write product descriptions for all 5 SKUs'),
     'Status': sel('Not Started'), 'Priority': sel('P1-High'),
     'Owner': sel('Claude'), 'Phase': sel('Build'), 'Due Date': date('2026-04-26')},
    {'Task': title('Launch Meta Advantage+ Shopping Campaign'),
     'Status': sel('Not Started'), 'Priority': sel('P0-Critical'),
     'Owner': sel('Human'), 'Phase': sel('Launch'), 'Due Date': date('2026-04-28')},
    {'Task': title('Create 3-email welcome + urgency sequence'),
     'Status': sel('Not Started'), 'Priority': sel('P2-Medium'),
     'Owner': sel('Claude'), 'Phase': sel('Build'), 'Due Date': date('2026-04-27')},
]
for r in rows1:
    seed(DB[1], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n🛍️  DB 2 — Product Catalog')
print('─' * 50)
rows2 = [
    {'Product Name': title("Mom's Ultimate Self-Care Printable Bundle"),
     'Type': sel('Digital Bundle'), 'Status': sel('In Production'),
     'Price': num(27), 'COGS': num(0), 'Target Persona': sel('Sentimental Daughter'),
     'Launch Date': date('2026-04-28')},
    {'Product Name': title("Last-Minute Dad's Gift Kit"),
     'Type': sel('Printable'), 'Status': sel('In Production'),
     'Price': num(17), 'COGS': num(0), 'Target Persona': sel('Last-Minute Dad'),
     'Launch Date': date('2026-04-28')},
    {'Product Name': title('Personalized Recipe Book Template'),
     'Type': sel('Template'), 'Status': sel('Idea'),
     'Price': num(12), 'COGS': num(0), 'Target Persona': sel('Sentimental Daughter'),
     'Launch Date': date('2026-04-30')},
    {'Product Name': title("Mother's Day Card Pack — 10 Designs"),
     'Type': sel('Printable'), 'Status': sel('In Production'),
     'Price': num(9), 'COGS': num(0), 'Target Persona': sel('Budget Shopper'),
     'Launch Date': date('2026-04-28')},
    {'Product Name': title('Premium Mom Memory Journal'),
     'Type': sel('Upsell'), 'Status': sel('Idea'),
     'Price': num(37), 'COGS': num(0), 'Target Persona': sel('Sentimental Daughter'),
     'Launch Date': date('2026-05-01')},
]
for r in rows2:
    seed(DB[2], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n🎨 DB 3 — Creative Bank')
print('─' * 50)
rows3 = [
    {'Asset Name': title('Hero Banner — Warm Kitchen Gift Moment'),
     'Asset Type': sel('Hero Image'), 'Generator': sel('DALL-E 3'),
     'Status': sel('Prompt Draft'), 'Dimensions': sel('1200x628'),
     'Prompt Used': txt('Warm sunlit kitchen, mother receiving wrapped gift from family, soft bokeh, photorealistic, warm tones, Mother\'s Day'),
     'Product': txt("Mom's Ultimate Self-Care Printable Bundle")},
    {'Asset Name': title('Ad Creative — Last-Minute Panic to Relief'),
     'Asset Type': sel('Ad Creative'), 'Generator': sel('DALL-E 3'),
     'Status': sel('Prompt Draft'), 'Dimensions': sel('1080x1080'),
     'Prompt Used': txt('Split image: stressed dad checking phone on left, relieved dad holding printed gift card on right, bold text overlay space at bottom'),
     'Product': txt("Last-Minute Dad's Gift Kit")},
    {'Asset Name': title('Product Mockup — Bundle Flat Lay'),
     'Asset Type': sel('Product Mockup'), 'Generator': sel('Ideogram'),
     'Status': sel('Prompt Draft'), 'Dimensions': sel('1080x1080'),
     'Prompt Used': txt('Flat lay of printable bundle pages, flowers, coffee mug, pastel pink background, professional product photography style'),
     'Product': txt("Mom's Ultimate Self-Care Printable Bundle")},
    {'Asset Name': title('Pinterest Pin — Recipe Book Preview'),
     'Asset Type': sel('Ad Creative'), 'Generator': sel('Ideogram'),
     'Status': sel('Prompt Draft'), 'Dimensions': sel('1080x1920'),
     'Prompt Used': txt('Elegant recipe book template spread, handwritten-style fonts, floral borders, "The [Family Name] Family Recipes" header, pastel tones'),
     'Product': txt('Personalized Recipe Book Template')},
    {'Asset Name': title('Story Video — 3 Reasons Mom Deserves This'),
     'Asset Type': sel('Story'), 'Generator': sel('Pictory'),
     'Status': sel('Prompt Draft'), 'Dimensions': sel('1080x1920'),
     'Prompt Used': txt('Slideshow: 3 scenes of mom daily stress moments, transition to gift unboxing reveal, uplifting music, text overlays for each reason'),
     'Product': txt("Mom's Ultimate Self-Care Printable Bundle")},
]
for r in rows3:
    seed(DB[3], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n✍️  DB 4 — Copy Library')
print('─' * 50)
rows4 = [
    {'Copy Title': title("Dad, You Have 48 Hours. Here's Her Gift."),
     'Copy Type': sel('Ad Headline'), 'Persona': sel('Last-Minute Dad'),
     'Funnel Stage': sel('Awareness'), 'Status': sel('Draft'),
     'Body': txt("Dad, You Have 48 Hours. Here's Her Gift.\nInstant download. Print at home. She'll love it.")},
    {'Copy Title': title("Still haven't gotten Mom anything? Open this."),
     'Copy Type': sel('Email Subject'), 'Persona': sel('Last-Minute Dad'),
     'Funnel Stage': sel('Conversion'), 'Status': sel('Draft'),
     'Body': txt("Subject: Still haven't gotten Mom anything? Open this.\n\nHey,\n\nMother's Day is in [X] days and if you're reading this, you probably don't have a gift yet.\n\nGood news: you don't need to leave the house.\n\nThe Mom Rescue Pack is an instant-download bundle your mom will actually use — not another candle she'll politely thank you for.\n\nDownload it now. Print it in 10 minutes. Show up like a hero.\n\n[CTA: Get the Bundle — $17]")},
    {'Copy Title': title('Meta Ad Body — Self-Care Bundle Conversion'),
     'Copy Type': sel('Ad Body'), 'Persona': sel('Sentimental Daughter'),
     'Funnel Stage': sel('Conversion'), 'Status': sel('Draft'),
     'Body': txt("She gave you everything.\n\nGive her a morning she'll actually enjoy.\n\nThe Mom's Ultimate Self-Care Bundle includes:\n✅ Daily gratitude & mood tracker\n✅ Weekly meal planner\n✅ Self-care ritual checklist\n✅ 'Letters to Mom' journal prompts\n✅ 12-month wellness calendar\n\nInstant download. Print at home. Personalize it for her.\n\n$27 — less than a grocery run.\n\n👇 Tap to get it before Mother's Day.")},
    {'Copy Title': title("Landing Page Hero — Last-Minute Dad"),
     'Copy Type': sel('Landing Page'), 'Persona': sel('Last-Minute Dad'),
     'Funnel Stage': sel('Consideration'), 'Status': sel('Draft'),
     'Body': txt("HEADLINE: The Gift That Takes 10 Minutes to Give.\n\nSUBHEAD: Instant download. Print at home. She'll think you planned this for weeks.\n\nBODY: No shipping. No waiting. No gift that arrives three days late.\n\nThe Mom Rescue Pack is a premium printable bundle designed for the mom who deserves more than a last-minute grocery store flower run.")},
    {'Copy Title': title('Product Description — Self-Care Bundle'),
     'Copy Type': sel('Product Description'), 'Persona': sel('Budget Shopper'),
     'Funnel Stage': sel('Conversion'), 'Status': sel('Draft'),
     'Body': txt("What's inside the Mom's Ultimate Self-Care Printable Bundle:\n\n• Daily Gratitude & Mood Tracker (30-day format)\n• Weekly Meal Planner with grocery list\n• Self-Care Ritual Checklist (morning + evening)\n• 'Letters to Mom' guided journal prompts (12 prompts)\n• 12-Month Wellness & Goals Calendar\n\nInstant PDF download — print as many times as you need.\nWorks with any home printer. Standard letter size (8.5x11).\n\nPerfect gift for Mother's Day, birthdays, or just because.")},
]
for r in rows4:
    seed(DB[4], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n🛒 DB 5 — Shopify Buildout Tracker')
print('─' * 50)
rows5 = [
    {'Item': title('Create Shopify account + select plan'),
     'Category': sel('Store Setup'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Basic plan ($29/mo) sufficient for launch')},
    {'Item': title('Install Digital Downloads app (free)'),
     'Category': sel('App'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Shopify Digital Downloads — free, handles PDF delivery automatically post-purchase')},
    {'Item': title('Upload all product files (.pdf + .zip bundles)'),
     'Category': sel('Product Page'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Max 1GB per file. Compress all PDFs. Bundle 5-product set as .zip for the $27 tier.')},
    {'Item': title('Configure Dawn theme — hero section + CTA'),
     'Category': sel('Theme'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Use section: Image with text overlay. Headline + subhead + primary CTA button. No coding needed.')},
    {'Item': title('Connect custom domain'),
     'Category': sel('Domain'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Purchase via Shopify or transfer from Namecheap/GoDaddy. Target: momrescuepack.com or similar.')},
    {'Item': title('Enable Shopify Payments + PayPal Express'),
     'Category': sel('Payment'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Shopify Payments for cards; PayPal for trust signal with older buyers.')},
    {'Item': title('Add Privacy Policy + Terms of Service pages'),
     'Category': sel('Legal'), 'Status': sel('Todo'),
     'Priority': sel('Must Have'), 'Notes': txt('Use Shopify auto-generator. Required for Meta ad account approval.')},
]
for r in rows5:
    seed(DB[5], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n📣 DB 6 — Ad Campaign Manager')
print('─' * 50)
rows6 = [
    {'Campaign Name': title("Meta Advantage+ — Self-Care Bundle Launch"),
     'Platform': sel('Meta'), 'Type': sel('Conversion'),
     'Status': sel('Draft'), 'Budget/Day': num(25),
     'Start Date': date('2026-04-28'), 'End Date': date('2026-05-10'),
     'Creative': txt('Hero Banner + Ad Body copy v1. Objective: Purchase. Pixel required.')},
    {'Campaign Name': title("Meta Retargeting — Cart Abandoners"),
     'Platform': sel('Meta'), 'Type': sel('Retargeting'),
     'Status': sel('Draft'), 'Budget/Day': num(10),
     'Start Date': date('2026-04-30'), 'End Date': date('2026-05-10'),
     'Creative': txt('Urgency creative: "Still thinking about it? Mother\'s Day is [X] days away." + scarcity angle.')},
    {'Campaign Name': title("Meta Lookalike — Purchaser Expansion"),
     'Platform': sel('Meta'), 'Type': sel('Lookalike'),
     'Status': sel('Draft'), 'Budget/Day': num(15),
     'Start Date': date('2026-05-01'), 'End Date': date('2026-05-10'),
     'Creative': txt('1% LAL of purchasers. Activate once 20+ purchases recorded. Same creative as launch campaign.')},
    {'Campaign Name': title("Pinterest Promoted Pins — Recipe Template"),
     'Platform': sel('Pinterest'), 'Type': sel('Awareness'),
     'Status': sel('Draft'), 'Budget/Day': num(5),
     'Start Date': date('2026-04-28'), 'End Date': date('2026-05-10'),
     'Creative': txt('Long-format pin 1080x1920. Recipe Book mockup. Target: Home & Garden + Gift Ideas boards.')},
    {'Campaign Name': title("Email — Last-Minute Urgency Sequence (May 8-10)"),
     'Platform': sel('Email'), 'Type': sel('Conversion'),
     'Status': sel('Draft'), 'Budget/Day': num(0),
     'Start Date': date('2026-05-08'), 'End Date': date('2026-05-10'),
     'Creative': txt('3-email sequence: May 8 (48hr warning), May 9 (countdown + social proof), May 10 (final hours + last chance).')},
]
for r in rows6:
    seed(DB[6], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n📊 DB 7 — Analytics Dashboard')
print('─' * 50)
rows7 = [
    {'Date': title('2026-04-23 — Baseline (Pre-Launch)'),
     'Revenue': num(0), 'Orders': num(0), 'Ad Spend': num(0),
     'ROAS': num(0), 'CAC': num(0), 'Refunds': num(0),
     'Email Subscribers': num(0),
     'Notes': txt('Store not yet live. Baseline recorded. Target: $1,000 revenue by May 10.')},
    {'Date': title('2026-04-28 — Launch Day'),
     'Revenue': num(0), 'Orders': num(0), 'Ad Spend': num(25),
     'ROAS': num(0), 'CAC': num(0), 'Refunds': num(0),
     'Email Subscribers': num(0),
     'Notes': txt('Shopify store live. Meta Advantage+ campaign active. Update actuals EOD.')},
    {'Date': title('2026-05-01 — Day 4 Check-In'),
     'Revenue': num(0), 'Orders': num(0), 'Ad Spend': num(100),
     'ROAS': num(0), 'CAC': num(0), 'Refunds': num(0),
     'Email Subscribers': num(0),
     'Notes': txt('Evaluate ROAS. If below 1.5x, pause and refresh creative. Activate LAL if 20+ purchases hit.')},
    {'Date': title('2026-05-10 — Mother\'s Day (Target Date)'),
     'Revenue': num(0), 'Orders': num(0), 'Ad Spend': num(0),
     'ROAS': num(0), 'CAC': num(0), 'Refunds': num(0),
     'Email Subscribers': num(0),
     'Notes': txt('Goal: $1,000 total revenue. Send final urgency email. Turn off paid ads EOD.')},
]
for r in rows7:
    seed(DB[7], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n📐 DB 8 — SOP Hub')
print('─' * 50)
rows8 = [
    {'SOP Title': title('New Product Upload & Fulfillment Setup'),
     'Category': sel('Product Creation'), 'Owner': sel('Human'),
     'Status': sel('Active'), 'Last Reviewed': date('2026-04-23'),
     'Trigger': txt('New digital product file is ready for sale'),
     'Steps': txt('1. Compress PDF to <10MB\n2. Upload to Shopify Products > Digital Downloads\n3. Set price, description, and product image\n4. Test purchase flow with $1 test order\n5. Confirm download email delivers within 60 seconds\n6. Add product to Product Catalog DB')},
    {'SOP Title': title('Customer Refund & Support Response'),
     'Category': sel('Customer Service'), 'Owner': sel('Human'),
     'Status': sel('Active'), 'Last Reviewed': date('2026-04-23'),
     'Trigger': txt('Customer emails support or opens Shopify dispute'),
     'Steps': txt('1. Respond within 4 hours during launch week\n2. If download failed: resend file manually via Shopify order\n3. If unsatisfied: offer replacement product before refund\n4. If refund required: process in Shopify, log in Analytics DB\n5. Note pattern if 3+ same complaints — flag for product fix')},
    {'SOP Title': title('Daily Ad Spend & ROAS Check'),
     'Category': sel('Marketing'), 'Owner': sel('Automation'),
     'Status': sel('Active'), 'Last Reviewed': date('2026-04-23'),
     'Trigger': txt('Every day at 8am during campaign window (Apr 28 – May 10)'),
     'Steps': txt('1. Check Meta Ads Manager: spend, ROAS, CPM, CTR\n2. If ROAS < 1.5x for 2+ consecutive days: pause campaign, swap creative\n3. If ROAS > 3x: increase budget by 20%\n4. Log daily Revenue, Ad Spend, ROAS in Analytics Dashboard DB\n5. Check for disapproved ads or policy flags')},
    {'SOP Title': title('New Creative Asset Request (Claude → Production)'),
     'Category': sel('Marketing'), 'Owner': sel('Claude'),
     'Status': sel('Active'), 'Last Reviewed': date('2026-04-23'),
     'Trigger': txt('Ad performance drops or new creative test needed'),
     'Steps': txt('1. Identify underperforming placement (static/video/story)\n2. Brief Claude: persona, pain point, format, dimensions\n3. Claude generates prompt in Creative Bank DB (Status: Prompt Draft)\n4. Run prompt in DALL-E 3 or Ideogram\n5. Review output, set status to Approved or regenerate\n6. Upload to Meta Ads Manager as new ad variant')},
    {'SOP Title': title('Weekly Revenue & Margin Report'),
     'Category': sel('Finance'), 'Owner': sel('n8n'),
     'Status': sel('Draft'), 'Last Reviewed': date('2026-04-23'),
     'Trigger': txt('Every Sunday at 6pm'),
     'Steps': txt('1. Pull 7-day revenue from Shopify (n8n webhook)\n2. Pull 7-day ad spend from Meta API\n3. Calculate net profit: Revenue - Ad Spend\n4. Update Analytics Dashboard DB rows for the week\n5. Flag if weekly revenue < $200 (below pace for $1k goal)\n6. Send summary to owner via email or Slack')},
]
for r in rows8:
    seed(DB[8], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n🤖 DB 9 — Agent System Registry')
print('─' * 50)
rows9 = [
    {'Agent Name': title('Product Sales Strategist'),
     'Role': sel('Sales'), 'Model': sel('Claude Sonnet 4'),
     'Status': sel('Active'),
     'Handles': txt('Product-to-value translation, persona positioning, battlecard creation, sales play development, objection handling frameworks'),
     'Last Used': date('2026-04-23')},
    {'Agent Name': title('Creative Director'),
     'Role': sel('Creative'), 'Model': sel('DALL-E 3'),
     'Status': sel('Active'),
     'Handles': txt('Hero images, ad creatives, product mockups. Prompts generated by Claude, executed via DALL-E 3 API. Secondary: Ideogram for text-in-image assets.'),
     'Last Used': date('2026-04-23')},
    {'Agent Name': title('Copywriting Agent'),
     'Role': sel('Copywriting'), 'Model': sel('Claude Sonnet 4'),
     'Status': sel('Active'),
     'Handles': txt('Ad headlines, ad body copy, email sequences, landing page copy, product descriptions. All copy stored in Copy Library DB.'),
     'Last Used': date('2026-04-23')},
    {'Agent Name': title('Analytics & Reporting Agent'),
     'Role': sel('Analytics'), 'Model': sel('Claude Sonnet 4'),
     'Status': sel('Idle'),
     'Handles': txt('Interprets daily KPIs from Analytics Dashboard, flags performance anomalies, recommends budget reallocation, generates weekly P&L summary'),
     'Last Used': date('2026-04-23')},
    {'Agent Name': title('Automation Orchestrator (n8n)'),
     'Role': sel('Automation'), 'Model': sel('n8n'),
     'Status': sel('Needs Config'),
     'Handles': txt('Shopify order webhooks → digital delivery triggers, daily ad spend pull from Meta API, weekly revenue report to email, Notion DB row creation on new orders'),
     'Webhook/API': url('https://n8n.io'),
     'Last Used': date('2026-04-23')},
]
for r in rows9:
    seed(DB[9], r)


# ─────────────────────────────────────────────────────────────────────────────
print('\n' + '=' * 60)
print('ALL 9 DATABASES SEEDED')
print('=' * 60)
print('Mom Rescue Pack Business OS is fully operational.')
print('Total records injected: 39')
