// Logique du Truck Payment Calculator — thebighauler.
// Formule de prêt standard (amortissement) :
//   M = P × r(1+r)^n / ((1+r)^n - 1)
//   où P = montant financé, r = taux mensuel, n = nombre de mois.
// + comparaison avec le CPM moyen d'un owner-operator.

export interface LoanInput {
  price: number;         // prix du camion
  down: number;          // apport
  trade: number;         // reprise
  rate: number;          // taux annuel %
  months: number;        // durée en mois
}

export interface LoanResult {
  financed: number;
  monthly: number;
  totalInterest: number;
  totalCost: number;
}

export function computeLoan(i: LoanInput): LoanResult {
  const financed = Math.max(0, i.price - i.down - i.trade);
  const r = i.rate / 100 / 12;
  if (financed <= 0) return { financed: 0, monthly: 0, totalInterest: 0, totalCost: 0 };
  const monthly = r === 0
    ? financed / i.months
    : (financed * r * Math.pow(1 + r, i.months)) / (Math.pow(1 + r, i.months) - 1);
  const totalCost = monthly * i.months;
  return {
    financed,
    monthly,
    totalInterest: totalCost - financed,
    totalCost,
  };
}
