#!/usr/bin/env python3
"""
Generate base64 data URIs for all SVG images in frontend/assets/images/
and output a Python dict ready to be pasted into routes.py
"""
import os
import base64
import json

IMAGES_DIR = r'C:\Users\Admin\OneDrive\Documents\AuralDine\frontend\assets\images'

if not os.path.isdir(IMAGES_DIR):
    print(f"Error: {IMAGES_DIR} not found")
    exit(1)

# Read all SVG files
svg_files = sorted([f for f in os.listdir(IMAGES_DIR) if f.endswith('.svg')])
print(f"Found {len(svg_files)} SVG files")

image_data_uris = {}

for fname in svg_files:
    fpath = os.path.join(IMAGES_DIR, fname)
    try:
        with open(fpath, 'rb') as f:
            content = f.read()
        b64 = base64.b64encode(content).decode('ascii')
        data_uri = f'data:image/svg+xml;base64,{b64}'
        image_data_uris[fname] = data_uri
        print(f"✓ {fname}")
    except Exception as e:
        print(f"✗ {fname}: {e}")

# Output as Python code
output_code = "# Auto-generated image data URIs (base64)\n"
output_code += "IMAGE_DATA_URIS = {\n"
for fname, uri in image_data_uris.items():
    output_code += f'    "{fname}": "{uri}",\n'
output_code += "}\n"

# Save to a file
output_file = r'C:\Users\Admin\OneDrive\Documents\AuralDine\backend\app\image_data_uris.py'
with open(output_file, 'w') as f:
    f.write(output_code)

print(f"\n✓ Saved {len(image_data_uris)} data URIs to {output_file}")
print(f"Total data URIs generated: {len(image_data_uris)}")
