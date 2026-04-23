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


# ── DATABASE 7: Analytics Dashboard ──────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 7: Analytics Dashboard')
print('=' * 60)

db7, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '📊'},
    'title': [{'type': 'text', 'text': {'content': '📊 Analytics Dashboard'}}],
    'properties': {
        'Date':                {'title': {}},
        'Revenue':             {'number': {'format': 'dollar'}},
        'Orders':              {'number': {'format': 'number'}},
        'Ad Spend':            {'number': {'format': 'dollar'}},
        'ROAS':                {'number': {'format': 'number'}},
        'CAC':                 {'number': {'format': 'dollar'}},
        'Refunds':             {'number': {'format': 'number'}},
        'Email Subscribers':   {'number': {'format': 'number'}},
        'Top Product':         {'select': {'options': [
            sel('Mom\'s Day Printable Bundle',    'green'),
            sel('Last-Minute Card Pack',          'blue'),
            sel('Personalized Recipe Book',       'pink'),
            sel('Sentimental Photo Template',     'purple'),
            sel('Gift Tag Collection',            'orange'),
        ]}},
        'Notes':               {'rich_text': {}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db7'] = ('FAILED', '')
else:
    url7 = db7.get('url', '')
    id7  = db7.get('id', '')
    print(f'  ID:  {id7}')
    print(f'  URL: {url7}')
    results_store['db7'] = (id7, url7)

time.sleep(0.5)


# ── DATABASE 8: SOP Hub ───────────────────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 8: SOP Hub')
print('=' * 60)

db8, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '📐'},
    'title': [{'type': 'text', 'text': {'content': '📐 SOP Hub'}}],
    'properties': {
        'SOP Title':    {'title': {}},
        'Category':     {'select': {'options': [
            sel('Product Creation', 'blue'),
            sel('Fulfillment',      'green'),
            sel('Marketing',        'orange'),
            sel('Customer Service', 'yellow'),
            sel('Finance',          'purple'),
            sel('Tech',             'gray'),
        ]}},
        'Owner':        {'select': {'options': [
            sel('Claude',     'purple'),
            sel('Human',      'blue'),
            sel('Automation', 'green'),
            sel('n8n',        'orange'),
        ]}},
        'Status':       {'select': {'options': [
            sel('Draft',        'gray'),
            sel('Active',       'green'),
            sel('Needs Update', 'yellow'),
            sel('Archived',     'red'),
        ]}},
        'Trigger':      {'rich_text': {}},
        'Steps':        {'rich_text': {}},
        'Last Reviewed': {'date': {}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db8'] = ('FAILED', '')
else:
    url8 = db8.get('url', '')
    id8  = db8.get('id', '')
    print(f'  ID:  {id8}')
    print(f'  URL: {url8}')
    results_store['db8'] = (id8, url8)

time.sleep(0.5)


# ── DATABASE 9: Agent System Registry ────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 9: Agent System Registry')
print('=' * 60)

db9, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '🤖'},
    'title': [{'type': 'text', 'text': {'content': '🤖 Agent System Registry'}}],
    'properties': {
        'Agent Name': {'title': {}},
        'Role':       {'select': {'options': [
            sel('Research',        'yellow'),
            sel('Creative',        'pink'),
            sel('Copywriting',     'orange'),
            sel('Sales',           'green'),
            sel('Analytics',       'blue'),
            sel('Automation',      'purple'),
            sel('Customer Service', 'gray'),
            sel('Dev',             'red'),
        ]}},
        'Model':      {'select': {'options': [
            sel('Claude Opus 4',    'purple'),
            sel('Claude Sonnet 4',  'blue'),
            sel('GPT-4o',           'green'),
            sel('DALL-E 3',         'orange'),
            sel('Runway ML',        'pink'),
            sel('Pictory',          'yellow'),
            sel('n8n',              'gray'),
        ]}},
        'Status':     {'select': {'options': [
            sel('Active',       'green'),
            sel('Idle',         'yellow'),
            sel('Needs Config', 'orange'),
            sel('Retired',      'red'),
        ]}},
        'Handles':    {'rich_text': {}},
        'Webhook/API': {'url': {}},
        'Last Used':  {'date': {}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db9'] = ('FAILED', '')
else:
    url9 = db9.get('url', '')
    id9  = db9.get('id', '')
    print(f'  ID:  {id9}')
    print(f'  URL: {url9}')
    results_store['db9'] = (id9, url9)


# ── BATCH 3 SUMMARY ───────────────────────────────────────────────────────────
print('\n' + '=' * 60)
print('BATCH 3 COMPLETE — ALL 9 DATABASES LIVE')
print('=' * 60)
labels = {
    'db7': '📊 Analytics Dashboard',
    'db8': '📐 SOP Hub',
    'db9': '🤖 Agent System Registry',
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
print('9-database Business OS complete.' if all_ok else 'One or more databases failed — check errors above.')
