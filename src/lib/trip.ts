// Logique du Trip Fuel Cost Calculator — thebighauler.
// Distance réelle via OSRM (open source routing, gratuit, sans clé).
// Coût carburant = (miles ÷ MPG) × prix diesel de la région (EIA).
// + option aller-retour, + marge de sécurité.

export interface TripInput {
  miles: number;
  mpg: number;
  dieselPrice: number;
  roundTrip: boolean;
  safetyBufferPct: number; // marge sur les miles (détours, déviations)
}

export interface TripResult {
  totalMiles: number;
  fuelGallons: number;
  fuelCost: number;
  perMile: number;
}

export function computeTrip(i: TripInput): TripResult {
  const totalMiles = i.miles * (i.roundTrip ? 2 : 1) * (1 + i.safetyBufferPct / 100);
  const fuelGallons = i.mpg > 0 ? totalMiles / i.mpg : 0;
  const fuelCost = fuelGallons * i.dieselPrice;
  return {
    totalMiles,
    fuelGallons,
    fuelCost,
    perMile: totalMiles > 0 ? i.dieselPrice / i.mpg : 0,
  };
}

// Géocodage ville → coordonnées via Nominatim (OSM, gratuit, sans clé).
// Usage policy: UA navigateur + referer requis.
export async function geocode(city: string): Promise<{ lat: number; lon: number; name: string }> {
  const r = await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(city + ", USA")}`,
    {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://thebighauler.com/calculators/trip-fuel-cost/",
        "Accept": "application/json",
      },
    }
  );
  if (!r.ok) throw new Error("geocode");
  const d = await r.json();
  if (!d.length) throw new Error("city");
  return { lat: parseFloat(d[0].lat), lon: parseFloat(d[0].lon), name: d[0].display_name.split(",")[0] };
}

// Distance réelle via OSRM.
export async function routeMiles(a: { lat: number; lon: number }, b: { lat: number; lon: number }): Promise<number> {
  const url = `https://router.project-osrm.org/route/v1/driving/${a.lon},${a.lat};${b.lon},${b.lat}?overview=false`;
  const r = await fetch(url);
  if (!r.ok) throw new Error("route");
  const d = await r.json();
  if (!d.routes?.length) throw new Error("noroute");
  return d.routes[0].distance / 1609.34; // mètres → miles
}
