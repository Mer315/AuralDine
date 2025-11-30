import sys
import json
import base64
from pathlib import Path

if len(sys.argv) < 3:
    print('Usage: decode_image.py <image_key> <output_path>')
    sys.exit(1)

key = sys.argv[1]
out = Path(sys.argv[2])

root = Path(__file__).resolve().parents[1]
json_path = root / 'image_uris.json'
if not json_path.exists():
    print('image_uris.json not found at', json_path)
    sys.exit(2)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if key not in data:
    print(f'Key "{key}" not found in image_uris.json')
    print('Available keys (sample):', list(data.keys())[:10])
    sys.exit(3)

val = data[key]
if not val.startswith('data:image/svg+xml;base64,'):
    print('Unexpected format, writing raw value to file')
    out.write_text(val, encoding='utf-8')
    print('Wrote', out)
    sys.exit(0)

b64 = val.split(',',1)[1]
svg_bytes = base64.b64decode(b64)
out.write_bytes(svg_bytes)
print('Wrote', out.resolve())
