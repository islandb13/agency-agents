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
KNOWN_PARENT_ID = '34a2d0b7-e3d8-80ec-bb9c-e31edab221d6'


def notion_request(method, endpoint, payload=None):
    url = f'{BASE_URL}{endpoint}'
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': f'Bearer {TOKEN}',
            'Notion-Version': NOTION_VERSION,
            'Content-Type': 'application/json',
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return None, f'HTTP {e.code}: {body}'
    except Exception as e:
        return None, str(e)


def sel(name, color):
    return {'name': name, 'color': color}


# ── STEP 1: Verify parent page ────────────────────────────────────────────────
print('=' * 60)
print('STEP 1: Verifying parent page')
print('=' * 60)

data, err = notion_request('POST', '/search', {
    'query': 'Mom Rescue Pack',
    'filter': {'property': 'object', 'value': 'page'},
    'page_size': 5,
})

parent_id = None
if not err:
    for result in data.get('results', []):
        props = result.get('properties', {})
        for v in props.values():
            if isinstance(v, dict) and v.get('type') == 'title':
                title = ''.join(t.get('plain_text', '') for t in v.get('title', []))
                if 'Mom Rescue Pack' in title:
                    parent_id = result['id']
                    print(f'  Confirmed: "{title}"')
                    print(f'  Parent ID: {parent_id}')
                    break

if not parent_id:
    parent_id = KNOWN_PARENT_ID
    print(f'  Fallback to known Parent ID: {parent_id}')

results_store = {}


# ── DATABASE 1: Master Project Board ─────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 1: Master Project Board')
print('=' * 60)

db1, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '📋'},
    'title': [{'type': 'text', 'text': {'content': '📋 Master Project Board'}}],
    'properties': {
        'Task':     {'title': {}},
        'Status':   {'select': {'options': [
            sel('Not Started', 'gray'),
            sel('In Progress', 'blue'),
            sel('Blocked',     'red'),
            sel('Done',        'green'),
        ]}},
        'Priority': {'select': {'options': [
            sel('P0-Critical', 'red'),
            sel('P1-High',     'orange'),
            sel('P2-Medium',   'yellow'),
            sel('P3-Low',      'gray'),
        ]}},
        'Owner':    {'select': {'options': [
            sel('Claude',     'purple'),
            sel('Human',      'blue'),
            sel('Automation', 'green'),
        ]}},
        'Phase':    {'select': {'options': [
            sel('Research', 'yellow'),
            sel('Build',    'blue'),
            sel('Launch',   'orange'),
            sel('Scale',    'green'),
        ]}},
        'Due Date':   {'date': {}},
        'Blocked By': {'rich_text': {}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db1'] = ('FAILED', '')
else:
    url1 = db1.get('url', '')
    id1  = db1.get('id', '')
    print(f'  ID:  {id1}')
    print(f'  URL: {url1}')
    results_store['db1'] = (id1, url1)

time.sleep(0.5)


# ── DATABASE 2: Product Catalog ───────────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 2: Product Catalog')
print('=' * 60)

db2, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '🛍️'},
    'title': [{'type': 'text', 'text': {'content': '🛍️ Product Catalog'}}],
    'properties': {
        'Product Name':   {'title': {}},
        'Type':           {'select': {'options': [
            sel('Printable',      'blue'),
            sel('Digital Bundle', 'purple'),
            sel('Template',       'green'),
            sel('Upsell',         'orange'),
        ]}},
        'Status':         {'select': {'options': [
            sel('Idea',          'gray'),
            sel('In Production', 'yellow'),
            sel('Live',          'green'),
            sel('Retired',       'red'),
        ]}},
        'Price':          {'number': {'format': 'dollar'}},
        'COGS':           {'number': {'format': 'dollar'}},
        'Margin %':       {'formula': {
            'expression': '(prop("Price") - prop("COGS")) / prop("Price") * 100',
        }},
        'Shopify URL':    {'url': {}},
        'Launch Date':    {'date': {}},
        'Target Persona': {'select': {'options': [
            sel('Last-Minute Dad',      'blue'),
            sel('Sentimental Daughter', 'pink'),
            sel('Budget Shopper',       'orange'),
        ]}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db2'] = ('FAILED', '')
else:
    url2 = db2.get('url', '')
    id2  = db2.get('id', '')
    print(f'  ID:  {id2}')
    print(f'  URL: {url2}')
    results_store['db2'] = (id2, url2)

time.sleep(0.5)


# ── DATABASE 3: Creative Bank ─────────────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 3: Creative Bank')
print('=' * 60)

db3, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '🎨'},
    'title': [{'type': 'text', 'text': {'content': '🎨 Creative Bank'}}],
    'properties': {
        'Asset Name':  {'title': {}},
        'Asset Type':  {'select': {'options': [
            sel('Hero Image',      'blue'),
            sel('Ad Creative',     'orange'),
            sel('Product Mockup',  'green'),
            sel('Video Clip',      'purple'),
            sel('Story',           'pink'),
        ]}},
        'Generator':   {'select': {'options': [
            sel('DALL-E 3',      'blue'),
            sel('Ideogram',      'green'),
            sel('Stability AI',  'purple'),
            sel('Runway ML',     'orange'),
            sel('Pictory',       'pink'),
        ]}},
        'Status':      {'select': {'options': [
            sel('Prompt Draft', 'gray'),
            sel('Generated',    'yellow'),
            sel('Reviewed',     'blue'),
            sel('Approved',     'green'),
            sel('Live',         'orange'),
        ]}},
        'File URL':    {'url': {}},
        'Prompt Used': {'rich_text': {}},
        'Product':     {'rich_text': {}},
        'Dimensions':  {'select': {'options': [
            sel('1080x1080',  'blue'),
            sel('1080x1920',  'purple'),
            sel('1200x628',   'green'),
            sel('4x6',        'orange'),
            sel('8.5x11',     'gray'),
        ]}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db3'] = ('FAILED', '')
else:
    url3 = db3.get('url', '')
    id3  = db3.get('id', '')
    print(f'  ID:  {id3}')
    print(f'  URL: {url3}')
    results_store['db3'] = (id3, url3)


# ── BATCH 1 SUMMARY ───────────────────────────────────────────────────────────
print('\n' + '=' * 60)
print('BATCH 1 COMPLETE')
print('=' * 60)
labels = {
    'db1': '📋 Master Project Board',
    'db2': '🛍️  Product Catalog',
    'db3': '🎨 Creative Bank',
}
all_ok = True
for key, label in labels.items():
    id_, url = results_store.get(key, ('FAILED', ''))
    status = '✅' if id_ != 'FAILED' else '❌'
    print(f'{status} {label}')
    if url:
        print(f'     {url}')
    else:
        all_ok = False

print()
print('All databases created successfully.' if all_ok else 'One or more databases failed — check errors above.')
