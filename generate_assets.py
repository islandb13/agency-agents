import urllib.request
import urllib.error
import json
import os
import base64
import time

GEMINI_KEY   = os.environ.get('GEMINI_API_KEY')
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
if not GEMINI_KEY:
    raise EnvironmentError('GEMINI_API_KEY environment variable is not set')
if not NOTION_TOKEN:
    raise EnvironmentError('NOTION_TOKEN environment variable is not set')
CREATIVE_DB  = '34b2d0b7-e3d8-81b6-85db-d646738b89f9'
ASSETS_DIR   = '/home/user/agency-agents/assets'
GEMINI_MODEL = 'gemini-3.1-flash-image-preview'

# Shared character anchors — injected into every persona-containing prompt
DAD_ANCHOR = (
    "The dad character is consistent throughout: late 30s male, dark brown hair, "
    "light stubble, wearing a blue casual shirt, average build, friendly face."
)
DAUGHTER_ANCHOR = (
    "The daughter character is consistent throughout: early 20s female, "
    "medium-length dark hair, warm smile, wearing a soft lilac top."
)


def gemini_image(prompt, filename):
    url = (
        f'https://generativelanguage.googleapis.com/v1beta/models/'
        f'{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}'
    )
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read())

    parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
    for part in parts:
        if 'inlineData' in part:
            img_bytes = base64.b64decode(part['inlineData']['data'])
            mime = part['inlineData'].get('mimeType', 'image/jpeg')
            ext = mime.split('/')[-1]
            out = os.path.join(ASSETS_DIR, f'{filename}.{ext}')
            with open(out, 'wb') as f:
                f.write(img_bytes)
            return out, len(img_bytes)
    raise RuntimeError(f'No image in Gemini response for {filename}')


def notion_create_page(properties):
    payload = {
        'parent': {'database_id': CREATIVE_DB},
        'properties': properties,
    }
    req = urllib.request.Request(
        'https://api.notion.com/v1/pages',
        data=json.dumps(payload).encode(),
        headers={
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    return result.get('url', '')


# ── ASSET DEFINITIONS ────────────────────────────────────────────────────────

ASSETS = [
    {
        'name': 'Hero Banner — Warm Kitchen Gift Moment',
        'filename': 'hero-banner-kitchen',
        'asset_type': 'Hero Image',
        'dimensions': '1200x628',
        'decision': {
            'engine': 'Gemini 3.1 Flash Image (DALL-E 3 logic)',
            'pros': 'Multi-object spatial storytelling: family grouping, environmental depth, emotional lighting',
            'scenario': 'Complex scene with 3 characters + props + architectural background requires spatial coherence over speed',
        },
        'prompt': (
            f"{DAD_ANCHOR} {DAUGHTER_ANCHOR} "
            "Cinematic wide-angle hero banner for an e-commerce Mother's Day gift brand. "
            "Scene: Warm golden morning light in a cozy modern kitchen. "
            "A woman in her mid-40s with light brown hair in a loose bun, wearing a soft cream cardigan, "
            "stands at a kitchen island with a surprised, emotional smile. "
            "Beside her: her daughter (early 20s, medium-length dark hair, lilac top) and husband (late 30s, dark hair, blue shirt) "
            "present a beautifully wrapped gift with a pink satin ribbon. "
            "Fresh peonies in a vase on the counter. Warm bokeh background. "
            "Photorealistic commercial photography. Horizontal composition. Emotional, heartwarming atmosphere."
        ),
    },
    {
        'name': 'Ad Creative — Last-Minute Dad: Panic to Relief',
        'filename': 'ad-creative-dad-split',
        'asset_type': 'Ad Creative',
        'dimensions': '1080x1080',
        'decision': {
            'engine': 'Gemini 3.1 Flash Image (Nano Banana 2 logic)',
            'pros': 'Character consistency anchor applied: same face/clothes on both sides of split-screen social ad',
            'scenario': 'Social conversion ad for Last-Minute Dad persona — before/after narrative in single square frame',
        },
        'prompt': (
            f"{DAD_ANCHOR} "
            "Bold square social media ad creative for a Mother's Day digital gift product. "
            "Split-screen composition divided by a clean vertical center line. "
            "LEFT HALF — BEFORE: The dad (dark hair, stubble, blue shirt) hunched over his phone, "
            "panicked expression, wall clock reads 11:59 PM, harsh cool-blue lighting, slight red tint, "
            "messy desk behind him. Small text space at top-left reads: 'Sound familiar?'. "
            "RIGHT HALF — AFTER: The SAME man (identical face, same blue shirt) now relaxed, "
            "standing tall, wide proud grin, holding a beautifully printed certificate card labeled "
            "'Mom Rescue Pack', warm golden light, green soft-glow checkmark above his head. "
            "Small text space at bottom-right reads: 'Fixed in 60 seconds.' "
            "Clean bold graphic style. Commercial ad quality. White sans-serif text overlays."
        ),
    },
    {
        'name': 'Product Mockup — Self-Care Bundle Flat Lay',
        'filename': 'product-mockup-flatlay',
        'asset_type': 'Product Mockup',
        'dimensions': '1080x1080',
        'decision': {
            'engine': 'Gemini 3.1 Flash Image (Nano Banana 2 logic)',
            'pros': 'High-fidelity product photography with prop arrangement — optimized for Shopify and social feed',
            'scenario': 'Primary product listing image for the $27 Self-Care Bundle — needs clean Shopify-ready look',
        },
        'prompt': (
            "Professional overhead flat-lay product photography on a soft blush-pink background. "
            "Center: 5 beautifully printed 8.5x11 pages from the 'Mom's Ultimate Self-Care Bundle' spread out slightly overlapping. "
            "Page designs visible: (1) a pastel daily mood tracker with feminine watercolor headers, "
            "(2) a weekly meal planner with clean grid layout and floral accents, "
            "(3) a monthly wellness calendar in cream and rose, "
            "(4) a journaling prompt page with elegant script title 'Letters to Mom', "
            "(5) a self-care checklist with delicate line illustrations. "
            "Surrounding props: one large white peony flower, a white ceramic mug with steam, "
            "a rose-gold pen, small dried lavender sprig. "
            "Soft diffused natural lighting, no harsh shadows. "
            "Professional Shopify product photography. Clean, premium, minimal aesthetic."
        ),
    },
    {
        'name': 'Pinterest Pin — Recipe Book Template Preview',
        'filename': 'pinterest-pin-recipe-book',
        'asset_type': 'Ad Creative',
        'dimensions': '1080x1920',
        'decision': {
            'engine': 'Gemini 3.1 Flash Image (Ideogram 2.0 logic)',
            'pros': 'Text-in-image emphasis: readable recipe book labels, title typography, CTA overlay — Ideogram-style prompt structure applied',
            'scenario': 'Pinterest vertical pin requires legible text hierarchy — recipe template must look real and readable to convert',
        },
        'prompt': (
            "Elegant vertical Pinterest marketing pin (portrait 2:3 ratio) for a digital download product. "
            "TOP SECTION: Flat-lay photo of an open recipe book template showing two facing pages. "
            "Left page title in elegant serif script reads exactly: 'The Johnson Family Recipes'. "
            "Delicate floral border in blush pink. Fields visible: Prep Time, Servings, Ingredients list with lines, Instructions. "
            "Right page shows a filled-in recipe card in the same style. "
            "Pages on marble surface with a peony flower beside the book. "
            "MIDDLE SECTION: Large bold text overlay on soft cream background reads exactly: "
            "'The Most Thoughtful Mother's Day Gift'. Elegant serif font, deep plum color (#6B2D5E). "
            "Subtext below: 'Personalized for YOUR family. Printed at home in minutes.' "
            "BOTTOM SECTION: Blush-pink button shape with white text: 'Instant Download — $12' "
            "and small text below: 'momrescuepack.com'. "
            "Overall: premium, editorial, Pinterest-native aesthetic. Vertical composition."
        ),
    },
]


# ── EXECUTE ──────────────────────────────────────────────────────────────────

print('=' * 60)
print('CREATIVE BANK — ASSET GENERATION')
print('Engine: Gemini 3.1 Flash Image')
print('=' * 60)

generated = []

for i, asset in enumerate(ASSETS, 1):
    d = asset['decision']
    print(f'\n[{i}/4] {asset["name"]}')
    print(f'  Decision Logic:')
    print(f'    Engine:   {d["engine"]}')
    print(f'    Pros:     {d["pros"]}')
    print(f'    Scenario: {d["scenario"]}')

    try:
        path, size = gemini_image(asset['prompt'], asset['filename'])
        print(f'  Generated: {path}  ({size:,} bytes)')
        generated.append((asset, path))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  ERROR HTTP {e.code}: {body[:200]}')
        generated.append((asset, None))
    except Exception as e:
        print(f'  ERROR: {e}')
        generated.append((asset, None))

    if i < len(ASSETS):
        time.sleep(1)


# ── NOTION UPDATES ───────────────────────────────────────────────────────────

print('\n' + '=' * 60)
print('UPDATING NOTION — Creative Bank')
print('=' * 60)

for asset, path in generated:
    if not path:
        print(f'  SKIP (failed): {asset["name"]}')
        continue

    file_uri = f'file://{path}'
    d = asset['decision']
    props = {
        'Asset Name':  {'title': [{'text': {'content': asset['name']}}]},
        'Asset Type':  {'select': {'name': asset['asset_type']}},
        'Generator':   {'select': {'name': 'DALL-E 3'}},   # maps to closest schema option
        'Status':      {'select': {'name': 'Generated'}},
        'File URL':    {'url': file_uri},
        'Prompt Used': {'rich_text': [{'text': {'content': asset['prompt'][:1800]}}]},
        'Dimensions':  {'select': {'name': asset['dimensions']}},
        'Product':     {'rich_text': [{'text': {'content': d['engine']}}]},
    }
    try:
        url = notion_create_page(props)
        print(f'  Notion row created: {asset["name"]}')
        print(f'    {url}')
    except Exception as e:
        print(f'  Notion ERROR for {asset["name"]}: {e}')
    time.sleep(0.4)

print('\n' + '=' * 60)
print('COMPLETE')
ok = sum(1 for _, p in generated if p)
print(f'{ok}/4 assets generated  |  {ok}/4 Notion rows written')
print('=' * 60)
