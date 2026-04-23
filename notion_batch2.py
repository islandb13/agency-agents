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


# ── DATABASE 4: Copy Library ──────────────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 4: Copy Library')
print('=' * 60)

db4, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '✍️'},
    'title': [{'type': 'text', 'text': {'content': '✍️ Copy Library'}}],
    'properties': {
        'Copy Title':   {'title': {}},
        'Copy Type':    {'select': {'options': [
            sel('Ad Headline',       'red'),
            sel('Ad Body',           'orange'),
            sel('Email Subject',     'yellow'),
            sel('Email Body',        'blue'),
            sel('Landing Page',      'purple'),
            sel('SMS',               'pink'),
            sel('Product Description', 'green'),
        ]}},
        'Persona':      {'select': {'options': [
            sel('Last-Minute Dad',      'blue'),
            sel('Sentimental Daughter', 'pink'),
            sel('Budget Shopper',       'orange'),
        ]}},
        'Funnel Stage': {'select': {'options': [
            sel('Awareness',     'yellow'),
            sel('Consideration', 'blue'),
            sel('Conversion',    'green'),
            sel('Retention',     'purple'),
        ]}},
        'Status':       {'select': {'options': [
            sel('Draft',   'gray'),
            sel('Tested',  'yellow'),
            sel('Winner',  'green'),
            sel('Retired', 'red'),
        ]}},
        'Body':         {'rich_text': {}},
        'CTR %':        {'number': {'format': 'percent'}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db4'] = ('FAILED', '')
else:
    url4 = db4.get('url', '')
    id4  = db4.get('id', '')
    print(f'  ID:  {id4}')
    print(f'  URL: {url4}')
    results_store['db4'] = (id4, url4)

time.sleep(0.5)


# ── DATABASE 5: Shopify Buildout Tracker ──────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 5: Shopify Buildout Tracker')
print('=' * 60)

db5, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '🛒'},
    'title': [{'type': 'text', 'text': {'content': '🛒 Shopify Buildout Tracker'}}],
    'properties': {
        'Item':           {'title': {}},
        'Category':       {'select': {'options': [
            sel('Store Setup', 'blue'),
            sel('Product Page', 'green'),
            sel('Theme',       'purple'),
            sel('App',         'orange'),
            sel('Domain',      'yellow'),
            sel('Payment',     'pink'),
            sel('Legal',       'gray'),
        ]}},
        'Status':         {'select': {'options': [
            sel('Todo',        'gray'),
            sel('In Progress', 'blue'),
            sel('Done',        'green'),
            sel('Skipped',     'red'),
        ]}},
        'Priority':       {'select': {'options': [
            sel('Must Have',   'red'),
            sel('Nice to Have', 'yellow'),
        ]}},
        'Notes':          {'rich_text': {}},
        'Completed Date': {'date': {}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db5'] = ('FAILED', '')
else:
    url5 = db5.get('url', '')
    id5  = db5.get('id', '')
    print(f'  ID:  {id5}')
    print(f'  URL: {url5}')
    results_store['db5'] = (id5, url5)

time.sleep(0.5)


# ── DATABASE 6: Ad Campaign Manager ──────────────────────────────────────────
print('\n' + '=' * 60)
print('CREATING DB 6: Ad Campaign Manager')
print('=' * 60)

db6, err = notion_request('POST', '/databases', {
    'parent': {'type': 'page_id', 'page_id': parent_id},
    'icon': {'type': 'emoji', 'emoji': '📣'},
    'title': [{'type': 'text', 'text': {'content': '📣 Ad Campaign Manager'}}],
    'properties': {
        'Campaign Name': {'title': {}},
        'Platform':      {'select': {'options': [
            sel('Meta',      'blue'),
            sel('TikTok',    'pink'),
            sel('Pinterest', 'red'),
            sel('Email',     'yellow'),
            sel('Organic',   'green'),
        ]}},
        'Type':          {'select': {'options': [
            sel('Awareness',   'yellow'),
            sel('Conversion',  'green'),
            sel('Retargeting', 'orange'),
            sel('Lookalike',   'purple'),
        ]}},
        'Status':        {'select': {'options': [
            sel('Draft',     'gray'),
            sel('Scheduled', 'yellow'),
            sel('Active',    'green'),
            sel('Paused',    'orange'),
            sel('Ended',     'red'),
        ]}},
        'Budget/Day':    {'number': {'format': 'dollar'}},
        'Start Date':    {'date': {}},
        'End Date':      {'date': {}},
        'ROAS':          {'number': {'format': 'number'}},
        'CPA':           {'number': {'format': 'dollar'}},
        'Creative':      {'rich_text': {}},
    },
})

if err:
    print(f'  ERROR: {err}')
    results_store['db6'] = ('FAILED', '')
else:
    url6 = db6.get('url', '')
    id6  = db6.get('id', '')
    print(f'  ID:  {id6}')
    print(f'  URL: {url6}')
    results_store['db6'] = (id6, url6)


# ── BATCH 2 SUMMARY ───────────────────────────────────────────────────────────
print('\n' + '=' * 60)
print('BATCH 2 COMPLETE')
print('=' * 60)
labels = {
    'db4': '✍️  Copy Library',
    'db5': '🛒 Shopify Buildout Tracker',
    'db6': '📣 Ad Campaign Manager',
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
