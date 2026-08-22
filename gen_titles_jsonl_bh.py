#!/usr/bin/env python3
"""Construit titles_all.jsonl pour le producteur thebighauler.
Source : outputs/titles_final/<vertical>.txt (titres FINAUX nettoyés cross-vertical).
Champs par item : title, slug, vertical, sub, angle, format.
Usage : python3 gen_titles_jsonl_bh.py [--max-per-vertical N] [--limit M]
"""
import json, re, sys
from pathlib import Path

ROOT = Path("/root/thebighauler")
FILTERED = ROOT / "outputs" / "titles_final"
OUT = ROOT / "outputs" / "titles_all.jsonl"

# verticals prioritaires pour le premier lot (ceux avec le meilleur potentiel
# d'intention commerciale + volume de recherche) — l'ordre détermine qui passe en premier
PRIORITY = [
    "eld-compliance", "hours-of-service", "dot-compliance", "ifta", "hazmat",
    "tms-dispatch", "load-boards", "freight-broker", "factoring", "quick-pay",
    "owner-operators", "lease-purchase", "finding-loads", "trucking-taxes",
    "maintenance", "diesel-engines", "truck-tires", "air-brakes", "trailers",
    "fuel", "fuel-cards", "diesel-prices", "insurance", "cargo-insurance",
    "bobtail", "truck-financing", "cdl-licensing", "cdl-endorsements",
    "driving-school", "truck-driver-jobs", "pre-trip", "safety",
    "logistics", "fleet-management", "fleet-tracking", "fleet-maintenance",
    "telematics", "route-planning", "warehouse", "3pl", "last-mile",
    "flatbed", "tanker", "hotshot", "box-truck", "dump-truck",
    "freight-rates", "spot-rates", "ltl-vs-ftl", "buying-a-truck",
    "new-vs-used", "truck-auctions",
]

# titres à exclure (résidus homonymes détectés manuellement)
BLACKLIST = [
    "tms treatment", "automobile fuel", "a time to plant", "atlanta ga home",
    "50 year old business", "barclays invoice", "bambi dispatch",
    "after hours phone", "america's best hours", "ascend tms",
    "amazon free load boards", "123 load board login",
]

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80].rstrip("-")

def detect_format(title):
    tl = title.lower()
    if " vs " in tl or " vs." in tl or tl.startswith("vs "):
        return "compare"
    if "checklist" in tl or "check list" in tl:
        return "checklist"
    if re.match(r"^(top |best |7 |10 |5 |8 |9 |6 |12 |15 |25 |20 )", tl) or tl.startswith(("best ", "top ")):
        return "list"
    return "guide"

def detect_angle(title):
    tl = title.lower()
    if tl.startswith(("how ", "how to")):
        return "how-to"
    if tl.startswith(("what ", "which ")):
        return "definition"
    if tl.startswith(("best ", "top ", "greatest ")) or re.match(r"^\d+ ", tl):
        return "best-of"
    if tl.startswith(("why ", "when ", "where ", "can ", "do ", "does ", "is ", "are ")):
        return "question"
    if "cost" in tl or "price" in tl or "how much" in tl or "rate" in tl:
        return "cost"
    return "general"

def main():
    max_per = None
    limit = None
    for i, a in enumerate(sys.argv):
        if a == "--max-per-vertical" and i + 1 < len(sys.argv):
            max_per = int(sys.argv[i + 1])
        if a == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    # ordre : verticals prioritaires d'abord, puis les autres (pour que la prod
    # traite les meilleurs en premier, sans plafond arbitraire par vertical)
    ordered_vids = [v for v in PRIORITY if (FILTERED / f"{v}.txt").exists()]
    ordered_vids += sorted(v for f in FILTERED.glob("*.txt") if (v := f.stem) not in PRIORITY)

    items = []
    for vid in ordered_vids:
        f = FILTERED / f"{vid}.txt"
        titles = [l.strip() for l in f.read_text().splitlines() if l.strip()]
        # retire les blacklistés
        titles = [t for t in titles if not any(b in t.lower() for b in BLACKLIST)]
        if max_per:
            titles = titles[:max_per]
        for t in titles:
            items.append({
                "title": t,
                "slug": slugify(t),
                "vertical": vid,
                "sub": vid.replace("-", " "),
                "angle": detect_angle(t),
                "format": detect_format(t),
            })

    # dédup par slug
    seen = set()
    uniq = []
    for it in items:
        if it["slug"] in seen:
            continue
        seen.add(it["slug"])
        uniq.append(it)

    # PRIORITÉ PAR INTENTION COMMERCIALE (modèle info-first) :
    # les articles qui convertissent sortent en premier.
    # compare (comparatifs) > list/best-of (guides d'achat) > cost (coûts) > guide info
    PRIO = {"compare": 0, "list": 1, "checklist": 1, "cost": 2, "best-of": 2, "how-to": 3, "guide": 4}
    # angle cost détecté dans le titre (cost/price/rate/how much)
    def prio_key(it):
        f = it["format"]
        base = PRIO.get(f, 4)
        tl = it["title"].lower()
        if base == 4 and any(w in tl for w in ["cost", "price", "rate", "how much", "worth", "value"]):
            base = 2
        return base
    uniq.sort(key=prio_key)

    if limit:
        uniq = uniq[:limit]

    with open(OUT, "w") as f:
        for it in uniq:
            f.write(json.dumps(it) + "\n")

    from collections import Counter
    vc = Counter(i["vertical"] for i in uniq)
    print(f"{len(uniq)} titres dans titles_all.jsonl ({len(vc)} verticals)")
    print("top verticals:", vc.most_common(10))
    fmts = Counter(i["format"] for i in uniq)
    print("formats:", dict(fmts))
    # premiers titres (ceux qui seront produits en premier)
    print("PREMIERS 10 (intention commerciale):")
    for it in uniq[:10]:
        print(f"  [{it['vertical']}|{it['format']}] {it['title'][:60]}")

if __name__ == "__main__":
    main()
