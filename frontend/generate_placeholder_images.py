#!/usr/bin/env python3
"""
Generate placeholder images for cuisines.
This script creates simple SVG-based placeholder images for all cuisines.
"""

import os
from pathlib import Path

# Define cuisines by state
CUISINES = {
    "telangana": [
        "biryani", "chickencurry", "pesarattu", "gongura", "halim",
        "mirchi", "khichdi", "qubani", "shamikebab", "nihari"
    ],
    "gujarath": [
        "dhokla", "undhiyu", "fafda", "khichiyu", "thepla",
        "khandvi", "jalebi", "pavbhaji", "kadhi", "muthiya"
    ],
    "kerala": [
        "appam", "fishcurry", "puttu", "avial", "dosa",
        "erissery", "rasam", "parippu", "bananachips", "payasam"
    ],
    "karnataka": [
        "bisibele", "dosa", "uttapam", "joladaroti", "hulijavitri",
        "ravaidli", "ragimudde", "mysorepak", "chikhalwali", "bonda"
    ],
    "jharkhand": [
        "thekua", "rugra", "dhuska", "pua", "chikni",
        "alootamatar", "baati", "litti", "dal", "khichdi"
    ],
    "tamilnadu": [
        "idli", "chettinad", "dosa", "vadai", "rasam",
        "pongal", "appalam", "idiyappam", "momo", "payasam"
    ]
}

def create_svg_placeholder(name: str) -> str:
    """Create a simple SVG placeholder for a cuisine image."""
    colors = {
        "telangana": "#FF6B35",
        "gujarath": "#FFA500",
        "kerala": "#FF8C00",
        "karnataka": "#FF7F50",
        "jharkhand": "#FF6347",
        "tamilnadu": "#FF5733"
    }
    
    state = None
    for s in colors:
        if any(c in name for c in CUISINES.get(s, [])):
            state = s
            break
    
    color = colors.get(state, "#FF7F50")
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF1744;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#grad_{name})"/>
  <circle cx="200" cy="120" r="60" fill="rgba(255,255,255,0.2)"/>
  <circle cx="150" cy="150" r="40" fill="rgba(255,255,255,0.15)"/>
  <circle cx="250" cy="180" r="35" fill="rgba(255,255,255,0.1)"/>
  <text x="200" y="260" font-size="24" font-weight="bold" text-anchor="middle" fill="white">{name.replace("_", " ").title()}</text>
</svg>'''
    return svg

def main():
    """Generate placeholder images for all cuisines."""
    base_dir = Path(__file__).parent / "assets" / "images"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for state, dishes in CUISINES.items():
        for dish in dishes:
            filename = f"{state}_{dish}.svg"
            filepath = base_dir / filename
            
            svg_content = create_svg_placeholder(f"{state}_{dish}")
            
            with open(filepath, 'w') as f:
                f.write(svg_content)
            
            count += 1
            print(f"✅ Created {filename}")
    
    print(f"\n✅ Generated {count} placeholder images in {base_dir}")

if __name__ == "__main__":
    main()
