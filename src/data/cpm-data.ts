// Données du Cost Per Mile Calculator — thebighauler.
//
// SOURCES (toutes vérifiées le 22/08/2026) :
// 1. Prix diesel par région : EIA Weekly On-Highway Diesel Prices,
//    release du 17/08/2026 (fichier psw18vwall.xls, feuille Data 1).
// 2. Taux IRS standard mileage 2026 : IR-2026-29 (IRS.gov).
// 3. Moyennes d'industrie (pré-remplissage) : American Trucking
//    Associations (ATA) American Trucking Trends + ratios de coûts
//    standard de l'industrie (opération de camion de classe 8).

export interface DieselPrice {
  label: string;
  price: number; // USD par gallon, EIA 17/08/2026
}

export const DIESEL_PRICES: DieselPrice[] = [
  { label: "U.S. average", price: 5.454 },
  { label: "East Coast", price: 5.34 },
  { label: "New England", price: 5.545 },
  { label: "Central Atlantic", price: 5.652 },
  { label: "Lower Atlantic", price: 5.204 },
  { label: "Midwest", price: 5.435 },
  { label: "Gulf Coast", price: 5.237 },
  { label: "Rocky Mountain", price: 5.427 },
  { label: "West Coast", price: 6.203 },
  { label: "California", price: 6.785 },
];

export const DIESEL_UPDATED = "August 17, 2026 (EIA weekly survey)";

// Taux IRS standard mileage 2026 (IR-2026-29) — le plancher de déduction.
export const IRS_RATE_2026_H2 = 0.76; // July 1 - Dec 31, 2026 (cents/mile → $/mile)
export const IRS_RATE_2026_H1 = 0.725; // Jan 1 - June 30, 2026
export const IRS_SOURCE = "IRS IR-2026-29, standard mileage rates 2026";

// Moyennes ATA par catégorie (pré-remplissage du calculateur) :
// coûts typiques d'un camion de classe 8 (tracteur + remorque, OTR).
// Source : ATA American Trucking Trends (coûts moyens par mile, USD).
export interface CostDefaults {
  fuel: number;        // $/gal — remplacé par le prix de la région choisie
  fuelMpg: number;     // miles par gallon moyen
  maintenance: number; // $/mile — entretien + réparations + pneus
  insurance: number;   // $/mile — assurance + cargo
  payments: number;    // $/mile — paiement tracteur + remorque (amorti)
  tires: number;       // $/mile
  misc: number;        // $/mile — péages, permis, licences, taxes
  driverPay: number;   // $/mile — rémunération conducteur (owner-op = son revenu)
}

export const DEFAULT_COSTS: CostDefaults = {
  fuel: 5.454,         // US avg EIA — remplacé dynamiquement par région
  fuelMpg: 6.2,        // moyenne classe 8 OTR (ATA)
  maintenance: 0.21,
  insurance: 0.09,
  payments: 0.24,
  tires: 0.045,
  misc: 0.06,
  driverPay: 0.55,
};

export const COSTS_UPDATED = "2026 (ATA industry averages)";
