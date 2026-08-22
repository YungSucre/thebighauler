// Logique de calcul du Cost Per Mile (CPM) — thebighauler.
// Formule standard de l'industrie (ATA / owner-operator) :
//   coût carburant = (miles ÷ MPG) × prix diesel de la région
//   coût par mile = (carburant + entretien×miles + assurance×miles +
//                    paiements×miles + pneus×miles + divers×miles +
//                    paye×miles) ÷ miles
// = carburant/mile + somme des coûts fixes par mile.

export interface CpmInput {
  milesPerMonth: number;   // miles mensuels
  mpg: number;             // miles par gallon
  dieselPrice: number;     // $/gal (région choisie, EIA)
  maintenance: number;     // $/mile
  insurance: number;       // $/mile
  payments: number;        // $/mile
  tires: number;           // $/mile
  misc: number;            // $/mile
  driverPay: number;       // $/mile
}

export interface CpmResult {
  fuelCostPerMile: number;
  fixedCostPerMile: number;
  totalCostPerMile: number;
  monthlyFuel: number;
  monthlyTotal: number;
  irsRate: number;         // le taux IRS de déduction (plancher)
  irsDeduction: number;    // ce qu'on peut déduire par mile
}

export function computeCpm(i: CpmInput): CpmResult {
  const fuelCostPerMile = i.mpg > 0 ? i.dieselPrice / i.mpg : 0;
  const fixedCostPerMile =
    i.maintenance + i.insurance + i.payments + i.tires + i.misc + i.driverPay;
  const totalCostPerMile = fuelCostPerMile + fixedCostPerMile;
  const monthlyFuel = fuelCostPerMile * i.milesPerMonth;
  const monthlyTotal = totalCostPerMile * i.milesPerMonth;
  // taux IRS 2026 H2 (juillet-décembre) — le plancher de déduction officiel
  const irsRate = 0.76;
  return {
    fuelCostPerMile,
    fixedCostPerMile,
    totalCostPerMile,
    monthlyFuel,
    monthlyTotal,
    irsRate,
    irsDeduction: irsRate * i.milesPerMonth,
  };
}
