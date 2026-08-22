#!/usr/bin/env python3
"""Télécharge une image Pexels par famille pour la home thebighauler."""
import json, os, re, subprocess, urllib.request

KEY = subprocess.run(["bash", "-c", "grep -oP '^PEXELS_API_KEY=\\K.*' /root/niche-finder/.env | head -1"],
                     capture_output=True, text=True).stdout.strip()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"

FAMILIES = {
    "compliance": "truck driver tablet logbook cab",
    "operations": "truck dispatcher computer office logistics",
    "owner-operators": "truck driver semi truck",
    "equipment": "truck engine mechanic garage diesel",
    "fuel": "diesel fuel pump truck",
    "insurance": "truck highway road",
    "cdl": "truck driver steering wheel hands",
    "safety": "truck brakes inspection wheels",
    "tech": "trucker smartphone gps navigation",
    "logistics": "warehouse forklift logistics",
    "fleet": "fleet trucks parking lot aerial",
    "specialized": "flatbed truck loaded cargo",
    "rates": "highway trucks sunset road",
    "buying": "truck dealership semi truck for sale",
    "lifestyle": "truck stop diner night",
}

def fetch(q):
    url = "https://api.pexels.com/v1/search?query=" + urllib.parse.quote(q) + "&per_page=3&orientation=landscape"
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())
    for p in d.get("photos", [])[:3]:
        # préfère landscape ~1200px
        src = p["src"].get("landscape") or p["src"]["large"]
        return src, p.get("alt", "")
    return None, None

import urllib.parse
os.makedirs("/root/thebighauler/public/images/families", exist_ok=True)
ok = 0
for fam, q in FAMILIES.items():
    src, alt = fetch(q)
    if not src:
        print(f"!! {fam}: pas d'image")
        continue
    out = f"/root/thebighauler/public/images/families/{fam}.jpg"
    req = urllib.request.Request(src, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        open(out, "wb").write(r.read())
    ok += 1
    print(f"✓ {fam}: {q} -> {os.path.getsize(out)//1024} Ko")
print(f"{ok}/15 familles imagées")
