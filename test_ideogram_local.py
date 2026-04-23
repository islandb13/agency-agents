"""
Run this script on your LOCAL machine to verify your Ideogram API key works.
No installs required — uses Python stdlib only.

Usage:
    python test_ideogram_local.py

Output:
    Saves test-ideogram.jpeg to the same folder as this script.
"""

import urllib.request
import urllib.error
import json
import os

IDEOGRAM_KEY = 'P_swlOnw9znV2zlFFijuv7U6fRwFPrgiQbFlfe5gJ9FKjciBp2fl_QSB80UtZacZtGmG6nkIx0hAm9nb-9I0Og'
PROMPT = 'A small pink gift box with a white ribbon bow on a clean white background, minimal flat design, product photography style'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-ideogram.jpeg')

print('Testing Ideogram 2.0 API...')
req = urllib.request.Request(
    'https://api.ideogram.ai/generate',
    data=json.dumps({
        'image_request': {
            'prompt': PROMPT,
            'model': 'V_2',
            'resolution': 'RESOLUTION_1024_1024',
            'style_type': 'DESIGN',
        }
    }).encode(),
    headers={
        'Api-Key': IDEOGRAM_KEY,
        'Content-Type': 'application/json',
    },
    method='POST',
)

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())

    images = data.get('data', [])
    if not images:
        print(f'No images returned. Full response:\n{json.dumps(data, indent=2)}')
    else:
        img_url = images[0]['url']
        print(f'Image URL: {img_url[:80]}...')

        with urllib.request.urlopen(img_url, timeout=30) as r:
            img_bytes = r.read()

        with open(OUT, 'wb') as f:
            f.write(img_bytes)

        print(f'Saved: {OUT}  ({len(img_bytes):,} bytes)')
        print('Ideogram is LIVE and working.')

except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:400]}')
except Exception as e:
    print(f'Error: {e}')
