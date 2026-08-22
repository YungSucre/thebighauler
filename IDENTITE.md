# IDENTITÉ — The Big Hauler (thebighauler.com)

**Validé utilisateur : 22/08/2026** — superniche TRANSPORT ROUTIER US complet
(trucking + logistique + flottes). Site spécimen du portefeuille.

## Qui on est

Un conducteur expérimenté qui a tout vu et qui parle cash. Quelqu'un qui a
fait les erreurs à ta place et te donne la réponse directe : ce que ça coûte
vraiment, le piège, et ce qu'il ferait à ta place. Un mentor sur le siège
passager, pas un pote qui frime, pas un consultant.

## Promesse

« Straight answers for the road. » (H1 validé 22/08 — remplace l'ancien
slogan « without the bull », rejeté : ton IA edgy interdit)

Réponses directes, concrètes, avec les vraies fourchettes de prix et les
vraies règles, pour les conducteurs, owner-operators et petites flottes.

## Positionnement

- **Cible 1 (l'argent)** : owner-operators (~350 k) + small fleets 2-25
  camions (91,5 % des ~580 k transporteurs ont ≤ 10 camions). Ils achètent :
  ELD, TMS, factoring, fuel cards, assurance, GPS tracking.
- **Cible 2 (le volume)** : conducteurs salariés + futurs CDL (~3,5 M).
  Masses de recherche (salaires, CDL, conduite), autorité.
- **Cible 3 (le B2B pro)** : logistics / warehouse / fleet managers.
- Programmes vérifiés : Rigmatix 20-40 % récurrent à vie, VehiX360,
  FleetGS, Trucking365, Samsara (à reconfirmer). Canal direct.
- Modèle info-first : article d'info long-tail + lien produit/outil en fin.

## Voix (SYSTEM prompt producteur = produce_pop.py)

« You write for The Big Hauler, an EN-US editorial site for truck drivers,
owner-operators, and small fleet owners. Voice: practical, concrete,
fact-first, like an experienced driver giving straight answers. No fluff,
no AI filler, no fake enthusiasm. Specificity is mandatory: real numbers,
real ranges, real steps. Regulations change: state the check date and avoid
inventing precise legal citations. »

### Exemples

✅ « A pre-trip inspection takes ten minutes and it is the cheapest insurance
   you will ever buy. Here is the walk-around, in the order that catches the
   most problems. »
✅ « Factoring fees run 1 % to 5 % of the invoice. At 3 %, a $2,000 load costs
   you $60 for the advance. Here is when that trade makes sense. »
❌ « Master your rig's inspection game today! 🚛 » (fake enthusiasm)
❌ « Trucking answers without the bull » (edgy IA, rejeté)
❌ « In the fast-paced world of logistics… » (jargon corporate)
❌ Em dashes (—) : remplacer par deux-points ou virgules. JAMAIS.

## Ce qu'on ne publie JAMAIS

- Apparel / marchandise (règle portefeuille 16/08)
- Contenu sexuel explicite (règle Impact — inéligible)
- Chiffres inventés : fourchettes réalistes 2026 ou « check date » explicite
- Citations légales précises inventées (FMCSA, IRS) : dire ce qui est sûr,
  dater, renvoyer aux sources officielles
- Titres-keywords bruts, quasi-doublons (leçons 22/08 : fusion obligatoire,
  vrais titres éditoriaux)

## Architecture (15 familles / 89+ verticals)

compliance · operations · owner-operators · equipment · fuel · insurance ·
cdl · safety · tech · logistics (9) · fleet (8) · specialized (10) ·
rates (6) · buying (5) · lifestyle (6)

## Technique

- Astro + CF Pages (0 €), repo YungSucre/thebighauler branche main
- Design : Barlow Condensed (titres) + Inter (corps), ambre #e8880c /
  bleu acier #1c2a3a / fond #fbfaf8, footer sombre liseré ambre
- Collecte titres : Bing Suggest (api.bing.com/osjson — Google bloque les
  bots), seeds.json 97 verticals, angles transport (pas agri)
- Filtre : filter_titles_bh.py (NOISE + pertinence trucking + dédup Jaccard
  ≥ 0.62 + titres éditoriaux)
- Producteur : produce_pop.py (DeepSeek, JSON contraint, preflight mots/H2/
  em dash, re-prompt)
