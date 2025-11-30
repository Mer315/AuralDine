import os
import base64
import json

images_dir = 'frontend/assets/images'
files = sorted([f for f in os.listdir(images_dir) if f.endswith('.svg')])

uris = {}
for fname in files:
    fpath = os.path.join(images_dir, fname)
    with open(fpath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    uris[fname] = f'data:image/svg+xml;base64,{b64}'

# Save as JSON for easy reading
with open('image_uris.json', 'w') as f:
    json.dump(uris, f)

print(f"Generated {len(uris)} image data URIs and saved to image_uris.json")
