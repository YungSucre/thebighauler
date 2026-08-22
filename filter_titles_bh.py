#!/usr/bin/env python3
"""Filtre les titres collectés Bing pour thebighauler.

Standard 22/08 (leçons practiceownerpro/thefieldandfarm) :
1. NOISE : mots-clés hors-sujet / trop génériques / spammy
2. DEDUP : variantes quasi identiques fusionnées (Jaccard >= 0.62, même vertical)
3. TITRES : transformation en vrais titres éditoriaux (capitalisation, forme)

Usage : python3 filter_titles_bh.py [--top N]
Sortie : outputs/titles_filtered/<vertical>.txt + rapport console
"""
import re, sys, json
from pathlib import Path
from collections import Counter

ROOT = Path("/root/thebighauler")
RAW = ROOT / "outputs/titles_raw"
OUT = ROOT / "outputs/titles_filtered"

# --- 1. NOISE (mots / patterns qui disqualifient un titre) ---
NOISE = [
    "how to make money", "make money", "earn money", "money online",
    "passive income", "side hustle", "rich", "millionaire", "billionaire",
    "get rich", "cash app", "bitcoin", "crypto", "investing in crypto",
    "lottery", "gambling", "casino", "betting", "poker",
    "job interview questions", "resume", "cover letter",
    "gift ideas", "birthday", "wedding", "christmas gifts",
    "recipe", "recipes", "cooking", "bake", "baking", "meal prep",
    "best way to cook", "how to grow", "planting", "garden", "harvest",
    "clothes", "fashion", "outfit", "style guide",
    "porn", "sex", "dating", "girlfriend", "boyfriend", "wife", "husband",
    "fortnite", "minecraft", "gta", "video game", "xbox", "playstation",
    "conspiracy", "aliens", "ufo", "ghost", "haunted", "paranormal",
    "weight loss", "diet plan", "keto", "paleo",
    "politics", "president", "election", "trump", "biden",
    "nfl", "nba", "super bowl", "world cup",
    "tiktok", "instagram", "facebook", "youtube video", "influencer",
]
NOISE_RE = [re.compile(r"\b" + re.escape(n) + r"\b", re.I) for n in NOISE]

# Patterns de titres trop vagues / génériques (pas une vraie question)
VAGUE_RE = [
    re.compile(r"^(what|which|how) (is|are|was|were) (a |an |the )?[a-z]+ (called|named|known as)\b"),
    re.compile(r"^(what|how) .*(mean|means|definition|define)\b"),
    re.compile(r"^(a |an |the )?[a-z]+ (is|are) (a |an )?[a-z]+$"),  # "x is y" nu
    re.compile(r"^(what|which) (is|are) better\b"),
]

# --- 1b. PERTINENCE TRUCKING : le titre doit contenir un terme fort du métier
# (élimine les homonymes : "TMS Treatment" = médecine, "Automobile Fuel" = voiture)
TRUCK_TERMS = [
    "truck", "trucking", "trucker", "semi", "rig", "hauler", "hauling",
    "cdl", "eld", "logbook", "log book", "hours of service", "hos",
    "dot", "fmcsa", "ifta", "irp", "hazmat", "endorsement", "pre-trip",
    "pretrip", "inspection", "weigh station", "weight station",
    "freight", "load", "loads", "shipper", "shipping", "broker", "dispatch",
    "dispatcher", "tms", "factoring", "invoice", "quick pay", "carrier",
    "trailer", "reefer", "flatbed", "dry van", "tanker", "gooseneck",
    "fifth wheel", "5th wheel", "landing gear", "kingpin", "mud flap",
    "diesel", "dpf", "def ", "urea", "scr", "egr", "turbo", "injector",
    "air brake", "air brakes", "slack adjuster", "gladhand", "brake",
    "tire", "tires", "lug nut", "axle", "driveshaft", "drive shaft",
    "transmission", "18 speed", "10 speed", "shifting", "gear",
    "engine", "oil change", "coolant", "alternator", "battery",
    "fuel", "mpg", "miles per gallon", "per mile", "cpm", "idling",
    "truck stop", "truckstop", "truck parking", "rest area", "parking",
    "fuel card", "pilot flying j", "loves", "ta travel", "petro",
    "insurance", "bobtail", "cargo", "liability", "physical damage",
    "non trucking", "owner operator", "lease purchase", "lease-purchase",
    "per diem", "detention", "deadhead", "backhaul", "drayage",
    "dock", "pallet", "tarpaulin", "tarp", "strapping", "chains",
    "mountain driving", "winter driving", "night driving", "backing",
    "lane departure", "blind spot", "backup camera", "dash cam",
    "gps", "toll", "ez pass", "prepass", "scale",
    "peterbilt", "kenworth", "freightliner", "mack", "volvo", "cascadia",
    "w900", "day cab", "sleeper cab", "tractor", "trailer",
    "miles", "odometer", "log", "logs", "elog",
    "overweight", "oversize", "permit", "permits", "escort",
    "temperature", "reefer unit", "cold chain", "produce",
    "dry van", "box truck", "box trucks", "hotshot", "tow truck",
    "dump truck", "dump trucks", "concrete", "aggregate", "gravel",
    "car hauler", "auto transport", "flatbed", "step deck", "lowboy",
    "tanker", "livestock", "cattle", "logging truck", "log truck",
    "heavy haul", "oversize load", "superload", "escort vehicle",
    "ltl", "ftl", "less than truckload", "full truckload",
    "freight forwarding", "freight forwarder", "customs broker", "customs clearance",
    "truck auction", "auction", "trade in", "resale", "depreciation",
    "truck dealership", "used truck", "new truck",
    "driver health", "driver wellness", "trucker diet", "trucker sleep",
    "women in trucking", "female driver", "female truck",
    "spot rate", "spot market", "contract rate", "rate per mile",
    "load rate", "freight rate",
    # logistique + flotte (ajoutés après l'extension superniche)
    "fleet", "logistics", "warehouse", "supply chain", "intermodal",
    "drayage", "3pl", "last mile", "cold chain", "freight forwarding",
    "route planning", "route optimization", "telematics", "container",
    "forklift", "inventory", "pick and pack", "distribution",
]

def is_noise(title):
    for r in NOISE_RE:
        if r.search(title):
            return True
    for r in VAGUE_RE:
        if r.search(title):
            return True
    # trop court
    if len(title.split()) < 3:
        return True
    # trop long (pas un titre d'article)
    if len(title.split()) > 12:
        return True
    return False

def is_ontopic(title):
    tl = title.lower()
    return any(t in tl for t in TRUCK_TERMS)
STOP = set("the a an of to for and in on with your you best how what is are do does it s this week uk us can i my should need guide complete ways way about from per new vs or not".split())

def tokens(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2]

def jaccard(a, b):
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb:
        return 0
    return len(ta & tb) / len(ta | tb)

# Mots à capitaliser dans les titres
CAP_KEEP = {"cdl", "eld", "dot", "fmcsa", "ifta", "irs", "def", "tms", "gps", "dpf", "oem", "us", "uk", "usa", "epa", "osha", "apu", "tarp", "ata", "nat", "pass"}
LOWER_ALWAYS = {"a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "of", "in", "with", "vs", "per", "as"}

def editorial_title(raw):
    """Transforme une suggestion brute en titre éditorial propre."""
    t = raw.strip()
    # enlève les préfixes "how to" redondants si le titre est déjà une question
    t = re.sub(r"^(how do i|how can i|how to) ", "", t, flags=re.I) if len(t) > 45 else t
    # première lettre majuscule
    t = t[0].upper() + t[1:] if t else t
    # capitalisation des mots significatifs (title case doux)
    words = t.split()
    out = []
    for i, w in enumerate(words):
        core = re.sub(r"[^a-zA-Z0-9]", "", w)
        if i == 0 or core in CAP_KEEP or core.lower() not in LOWER_ALWAYS:
            # capitalise sauf acronymes
            if core.lower() in CAP_KEEP:
                out.append(w.upper() if w.isupper() else core.upper() + w[len(core):])
            else:
                out.append(w[0].upper() + w[1:] if w else w)
        else:
            out.append(w.lower())
    t = " ".join(out)
    # nettoie espaces avant ponctuation
    t = re.sub(r"\s+([,.:;?!])", r"\1", t)
    return t

def main():
    top_n = None
    if "--top" in sys.argv:
        top_n = int(sys.argv[sys.argv.index("--top") + 1])
    OUT.mkdir(parents=True, exist_ok=True)

    report = {}
    total_in = total_out = 0
    for rawfile in sorted(RAW.glob("*.txt")):
        if rawfile.name == "ALL.txt":
            continue
        vid = rawfile.stem
        lines = [l.strip().lower() for l in rawfile.read_text().splitlines() if l.strip()]
        total_in += len(lines)

        # 1. filtre noise + pertinence trucking
        kept = [l for l in lines if not is_noise(l) and is_ontopic(l)]

        # 2. dedup par similarité (greedy : garde le premier, élimine les >= 0.62)
        unique = []
        for l in kept:
            dup = False
            for u in unique:
                if jaccard(l, u) >= 0.62:
                    dup = True
                    break
            if not dup:
                unique.append(l)

        # 3. titres éditoriaux
        titles = [editorial_title(l) for l in unique]
        # dedup après normalisation (cas "vs" / "or")
        seen = set()
        final = []
        for t in titles:
            key = t.lower()
            if key in seen:
                continue
            seen.add(key)
            final.append(t)

        if top_n:
            final = final[:top_n]
        total_out += len(final)
        OUT.joinpath(vid + ".txt").write_text("\n".join(final))
        report[vid] = {"in": len(lines), "kept": len(kept), "final": len(final)}

    print(f"{'vertical':<22} {'bruts':>6} {'après filtre':>12} {'finaux':>7}")
    print("-" * 50)
    for vid, r in sorted(report.items()):
        print(f"{vid:<22} {r['in']:>6} {r['kept']:>12} {r['final']:>7}")
    print("-" * 50)
    print(f"TOTAL {total_in} bruts -> {total_out} titres éditoriaux uniques")

if __name__ == "__main__":
    main()
