#!/usr/bin/env python3
"""PRODUCTEUR D'ARTICLES practiceownerpro — articles factuels pro.
Pattern site2 : JSON contraint (json_object), température 0.5, re-prompt sur vide,
preflight (mots, H2, em dash, description). VOIX : factuelle, pro, sans tics IA.
Articles = guides pratiques pour practice owners (débutants).

Usage : python3 produce_pop.py --limit 10 [--vertical legal] [--slug xxx]
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path("/root/thebighauler")
CONTENT = ROOT / "src" / "content" / "articles"
OUTPUTS = ROOT / "outputs"
STATE = OUTPUTS / "produce_state.json"
TITLES = OUTPUTS / "titles_all.jsonl"

# Mapping vertical -> nom propre (généré depuis config.ts)
sys.path.insert(0, str(OUTPUTS))
from vertical_names import VERTICAL_NAMES

# DeepSeek
sys.path.insert(0, "/root/niche-finder/scripts")
def load_key():
    for p in ["/root/.hermes/.env", "/root/niche-finder/.env"]:
        if os.path.exists(p):
            for line in open(p):
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return None

KEY = load_key()
API = "https://api.deepseek.com/chat/completions"

EMDASH_RULE = "NEVER use em dashes (—). Use colons or commas instead."

SYSTEM = """You write for The Big Hauler, an EN-US editorial site for truck drivers, owner-operators, and small fleet owners. Topics: ELD compliance, hours of service, DOT rules, IFTA, dispatch and TMS software, load boards, freight factoring, truck maintenance, diesel engines, tires, air brakes, trailers, fuel management, insurance, CDL licensing, driving skills, and the business side of trucking. The reader is a driver or someone starting in trucking, often new to the business side. Voice: practical, concrete, fact-first, like an experienced driver giving straight answers. No fluff, no AI filler, no fake enthusiasm. Specificity is mandatory: real numbers, real ranges, real steps. Regulations change: state the check date and avoid inventing precise legal citations. """ + EMDASH_RULE + """

Output STRICT JSON with exactly these keys:
- "title": the article title (must match the requested title)
- "description": one sentence, 120-160 chars, SEO meta description
- "body": the full article in Markdown. Structure: intro paragraph (2-3 sentences answering the question directly), then H2 sections with concrete information, tables where useful, a FAQ section with 3-4 questions, and a final "The bottom line" section. 700-1100 words. Use H2 (##) headings, not H1. Bullet lists where natural. NEVER use em dashes. Include dollar figures as realistic ranges (e.g. $40-$60/month)."""

def call_llm(system, user, temperature=0.5):
    req = urllib.request.Request(API, data=json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "max_tokens": 3500,
    }).encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
    for a in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read())
                return d["choices"][0]["message"]["content"]
        except Exception as e:
            if a == 3:
                raise
            time.sleep(2 * (a + 1))

def parse_llm_out(raw):
    try:
        return json.loads(raw)
    except Exception:
        pass
    # fallback : extraire le JSON du texte
    m = re.search(r"\{[\s\S]*\}", raw)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return None

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def preflight(slug, title, desc, body, n_words_min=600):
    """Gates : mots, H2, em dash, description, titre."""
    probs = []
    words = len(body.split())
    if words < n_words_min:
        probs.append(f"court ({words} mots < {n_words_min})")
    h2 = body.count("\n## ")
    if h2 < 4:
        probs.append(f"H2 insuffisants ({h2} < 4)")
    if "—" in body:
        probs.append("em dash présent")
    if not desc or len(desc) < 100:
        probs.append("description trop courte")
    return probs

def build_prompt(item):
    return f"""Write the article for this title:

TITLE: {item['title']}

Context: this guide is for {item['sub']}s in the {item['vertical']} vertical, topic: {item['angle']}. Format: {item['format']}.

Requirements:
- Answer the question the title asks, directly and concretely
- Realistic current figures (2026) with ranges where exact numbers vary
- Practical steps the reader can take this week
- If the format is "compare": include a comparison table of 4-6 options with price ranges
- If the format is "list": structure around the N items as H2 sections
- If the format is "checklist": structure as a checklist with explanations
- FAQ section at the end (3-4 questions)
- "The bottom line" final section
- 700-1100 words, H2 sections only (no H1)
- NEVER use em dashes (—)"""

def load_state():
    if STATE.exists():
        try:
            return json.load(open(STATE))
        except Exception:
            pass
    return {"done": []}

def vertical_name(vid):
    """Nom propre du vertical depuis config.ts (mapping généré)."""
    return VERTICAL_NAMES.get(vid, vid.replace("-", " ").title())

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--vertical", default=None)
    ap.add_argument("--slug", default=None)
    args = ap.parse_args()

    if not KEY:
        print("DEEPSEEK_API_KEY introuvable", file=sys.stderr)
        return 2

    titles = [json.loads(l) for l in open(TITLES)]
    if args.vertical:
        titles = [t for t in titles if t["vertical"] == args.vertical]
    if args.slug:
        titles = [t for t in titles if t["slug"] == args.slug]

    st = load_state()
    done = set(st["done"])
    todo = [t for t in titles if t["slug"] not in done]
    print(f"{len(todo)} à produire ({len(done)} déjà faits)", flush=True)

    if args.slug:
        todo = [t for t in todo if t["slug"] == args.slug]

    produced = 0
    for item in todo[:args.limit]:
        slug = item["slug"]
        print(f"  [{produced+1}/{min(args.limit, len(todo))}] {item['title']}", flush=True)
        # retry loop (réponses vides possibles)
        ok = False
        for attempt in range(3):
            try:
                raw = call_llm(SYSTEM, build_prompt(item))
                d = parse_llm_out(raw)
                if not d or not d.get("body"):
                    print(f"    réponse vide (tentative {attempt+1})", flush=True)
                    continue
                body = d["body"]
                title = d.get("title", item["title"])
                desc = d.get("description", "")
                probs = preflight(slug, title, desc, body)
                if probs:
                    print(f"    preflight: {', '.join(probs)}", flush=True)
                    # re-prompt avec correction
                    fix = call_llm(SYSTEM, build_prompt(item) + f"\n\nYour previous draft was rejected: {', '.join(probs)}. Fix these issues. Keep the same title. Also ensure at least 700 words and 4 H2 sections. NO em dashes.")
                    d2 = parse_llm_out(fix)
                    if d2 and d2.get("body"):
                        body = d2["body"]
                        desc = d2.get("description", desc)
                        title = d2.get("title", title)
                # écriture du fichier
                frontmatter = (
                    "---\n"
                    f"title: \"{title.replace(chr(34), chr(39))}\"\n"
                    f"description: \"{desc.replace(chr(34), chr(39))}\"\n"
                    f"vertical: \"{item['vertical']}\"\n"
                    f"verticalName: \"{vertical_name(item['vertical'])}\"\n"
                    f"slug: \"{slug}\"\n"
                    "status: \"published\"\n"
                    "pubDate: 2026-08-21\n"
                    "affiliate_ready: false\n"
                    "---\n\n"
                )
                path = CONTENT / f"{item['vertical']}-{slug}.md"
                path.write_text(frontmatter + body.strip() + "\n")
                done.add(slug)
                st["done"] = list(done)
                STATE.write_text(json.dumps(st, indent=1))
                produced += 1
                ok = True
                print(f"    ✓ {path.name} ({len(body.split())} mots)", flush=True)
                break
            except Exception as e:
                print(f"    erreur: {e}", flush=True)
                time.sleep(3)
        if not ok:
            print(f"    ✗ ÉCHEC {slug}", flush=True)
        time.sleep(1)

    print(f"TERMINÉ: {produced} articles produits", flush=True)

if __name__ == "__main__":
    main()
