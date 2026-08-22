// Logique de calcul IFTA — calcul trimestriel standard.
// Formule officielle : taxes dues par juridiction =
//   (miles parcourus ÷ MPG moyen de la flotte) × taux de la juridiction
//   − (gallons achetés dans la juridiction × taux de la juridiction)
// Si le résultat est négatif (plus de crédit que de taxe due), on a un
// crédit reportable. La somme des taxes dues − crédits = montant à payer.

import { IFTA_RATES } from "../data/ifta-rates";

export interface IftaInput {
  milesByState: Record<string, number>; // miles parcourus par état
  gallonsByState: Record<string, number>; // gallons de diesel achetés par état
  totalGallons: number; // total gallons achetés (tous états)
  totalMiles: number; // total miles parcourus
}

export interface IftaLine {
  abbr: string;
  name: string;
  miles: number;
  gallons: number;
  rate: number | null; // taux diesel de l'état (null = non publié)
  taxDue: number;
  credit: number;
  net: number;
}

export interface IftaResult {
  lines: IftaLine[];
  mpg: number; // miles par gallon moyen
  totalTaxDue: number;
  totalCredit: number;
  totalNet: number; // à payer (ou crédit si négatif)
  quarter: string;
  updated: string;
}

export function computeIfta(input: IftaInput): IftaResult {
  const mpg = input.totalGallons > 0 ? input.totalMiles / input.totalGallons : 0;
  const lines: IftaLine[] = [];

  for (const [abbr, miles] of Object.entries(input.milesByState)) {
    if (miles <= 0) continue;
    const rate = IFTA_RATES[abbr]?.diesel ?? null;
    const gallons = input.gallonsByState[abbr] || 0;
    // taxe due = miles ÷ MPG × taux
    const taxDue = rate !== null && mpg > 0 ? (miles / mpg) * rate : 0;
    // crédit = gallons achetés dans cet état × taux de CET état
    const credit = rate !== null ? gallons * rate : 0;
    lines.push({
      abbr,
      name: IFTA_RATES[abbr]?.name || abbr,
      miles,
      gallons,
      rate,
      taxDue,
      credit,
      net: taxDue - credit,
    });
  }

  // tri par net décroissant (ce qu'on doit le plus en premier)
  lines.sort((a, b) => b.net - a.net);

  const totalTaxDue = lines.reduce((s, l) => s + l.taxDue, 0);
  const totalCredit = lines.reduce((s, l) => s + l.credit, 0);

  return {
    lines,
    mpg,
    totalTaxDue,
    totalCredit,
    totalNet: totalTaxDue - totalCredit,
    quarter: "3Q2026",
    updated: "August 22, 2026",
  };
}

// Helpers pour la page : ajouter/retirer des lignes d'état
export const US_STATES = Object.keys(IFTA_RATES).filter(
  (ab) => !["AB", "BC", "MB", "NB", "NL", "NS", "ON", "PE", "QC", "SK"].includes(ab)
).sort();
