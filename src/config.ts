export const SITE = {
  url: 'https://thebighauler.com',
  name: 'The Big Hauler',
  description:
    'Straight answers for truck drivers and owner-operators: ELD compliance, dispatch, maintenance, fuel, insurance, factoring, CDL, and the business side of trucking. Written in plain language by people who know the road.',
};

export const CATEGORIES = [
  {
    id: 'compliance',
    name: 'Compliance & Regulations',
    verticals: [
      { id: 'eld-compliance', name: 'ELD Compliance' },
      { id: 'hours-of-service', name: 'Hours of Service' },
      { id: 'dot-compliance', name: 'DOT Compliance' },
      { id: 'ifta', name: 'IFTA & Fuel Tax' },
      { id: 'hazmat', name: 'Hazmat' },
      { id: 'permits-oversize', name: 'Permits & Oversize' },
    ],
  },
  {
    id: 'operations',
    name: 'Operations & Dispatch',
    verticals: [
      { id: 'tms-dispatch', name: 'TMS & Dispatch Software' },
      { id: 'load-boards', name: 'Load Boards' },
      { id: 'freight-broker', name: 'Freight Brokers' },
      { id: 'factoring', name: 'Freight Factoring' },
      { id: 'quick-pay', name: 'Quick Pay' },
      { id: 'dispatch-service', name: 'Dispatch Services' },
    ],
  },
  {
    id: 'owner-operators',
    name: 'Owner-Operators',
    verticals: [
      { id: 'owner-operators', name: 'Owner-Operator Basics' },
      { id: 'lease-purchase', name: 'Lease-Purchase' },
      { id: 'finding-loads', name: 'Finding Loads' },
      { id: 'trucking-accounting', name: 'Trucking Accounting' },
      { id: 'trucking-taxes', name: 'Trucking Taxes' },
    ],
  },
  {
    id: 'equipment',
    name: 'Truck & Equipment',
    verticals: [
      { id: 'maintenance', name: 'Truck Maintenance' },
      { id: 'diesel-engines', name: 'Diesel Engines' },
      { id: 'truck-tires', name: 'Truck Tires' },
      { id: 'air-brakes', name: 'Air Brakes' },
      { id: 'trailers', name: 'Trailers' },
      { id: 'fifth-wheel', name: 'Fifth Wheel' },
    ],
  },
  {
    id: 'fuel',
    name: 'Fuel & Costs',
    verticals: [
      { id: 'fuel', name: 'Fuel Management' },
      { id: 'fuel-cards', name: 'Fuel Cards' },
      { id: 'diesel-prices', name: 'Diesel Prices' },
      { id: 'def', name: 'DEF Fluid' },
      { id: 'fuel-economy', name: 'Fuel Economy' },
    ],
  },
  {
    id: 'insurance',
    name: 'Insurance & Finance',
    verticals: [
      { id: 'insurance', name: 'Truck Insurance' },
      { id: 'commercial-auto', name: 'Commercial Auto' },
      { id: 'cargo-insurance', name: 'Cargo Insurance' },
      { id: 'bobtail', name: 'Bobtail Insurance' },
      { id: 'truck-financing', name: 'Truck Financing' },
    ],
  },
  {
    id: 'cdl',
    name: 'CDL & Careers',
    verticals: [
      { id: 'cdl-licensing', name: 'CDL Licensing' },
      { id: 'cdl-endorsements', name: 'CDL Endorsements' },
      { id: 'cdl-practice-test', name: 'CDL Practice Tests' },
      { id: 'driving-school', name: 'Driving School' },
      { id: 'truck-driver-jobs', name: 'Truck Driver Jobs' },
      { id: 'team-driving', name: 'Team Driving' },
    ],
  },
  {
    id: 'safety',
    name: 'Safety & Driving',
    verticals: [
      { id: 'safety', name: 'Truck Safety' },
      { id: 'pre-trip', name: 'Pre-Trip Inspection' },
      { id: 'backing', name: 'Backing & Maneuvering' },
      { id: 'mountain-driving', name: 'Mountain Driving' },
      { id: 'winter-driving', name: 'Winter Driving' },
      { id: 'night-driving', name: 'Night Driving' },
    ],
  },
  {
    id: 'tech',
    name: 'Tech & Apps',
    verticals: [
      { id: 'tech-apps', name: 'Trucker Apps' },
      { id: 'gps-truck', name: 'GPS for Trucks' },
      { id: 'dash-cams', name: 'Dash Cams' },
      { id: 'eld-apps', name: 'ELD Apps' },
      { id: 'weather-apps', name: 'Weather Apps' },
    ],
  },
  {
    id: 'lifestyle',
    name: 'Truck Stops & Life',
    verticals: [
      { id: 'truck-stops', name: 'Truck Stops' },
      { id: 'truck-parking', name: 'Truck Parking' },
      { id: 'rest-areas', name: 'Rest Areas' },
      { id: 'trucker-lifestyle', name: 'Life on the Road' },
    ],
  },
];

export const VERTICALS = CATEGORIES.flatMap((c) => c.verticals);
