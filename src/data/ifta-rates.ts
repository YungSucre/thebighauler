// IFTA fuel tax rates — 3Q2026 (July 1 - September 30, 2026).
// Source : IFTA, Inc. official Tax Rate Matrix (iftach.org/taxmatrix4/), updated 8/21/2026.
// Rates in USD per gallon. "special_diesel" is the IFTA diesel rate used for quarterly reports.
// Oregon (OR) leaves rates blank in the official matrix — see ODOT.
//
export interface IftaRate {
  name: string;
  diesel: number | null;
  gasoline: number | null;
}

export const IFTA_RATES: Record<string, IftaRate> = {
  "AB": { name: "Alberta", diesel: 0.3519, gasoline: 0.3519 },
  "AL": { name: "Alabama", diesel: 0.31, gasoline: 0.3 },
  "AR": { name: "Arkansas", diesel: 0.285, gasoline: 0.247 },
  "AZ": { name: "Arizona", diesel: 0.26, gasoline: 0.18 },
  "BC": { name: "British Columbia", diesel: 0.406, gasoline: 0.3924 },
  "CA": { name: "California", diesel: 0.979, gasoline: null },
  "CO": { name: "Colorado", diesel: 0.335, gasoline: 0.28 },
  "CT": { name: "Connecticut", diesel: 0.499, gasoline: 0.25 },
  "DE": { name: "Delaware", diesel: 0.22, gasoline: 0.23 },
  "FL": { name: "Florida", diesel: 0.4097, gasoline: 0.411 },
  "GA": { name: "Georgia", diesel: 0.373, gasoline: 0.333 },
  "IA": { name: "Iowa", diesel: 0.325, gasoline: 0.3 },
  "ID": { name: "Idaho", diesel: 0.32, gasoline: null },
  "IL": { name: "Illinois", diesel: 0.738, gasoline: 0.653 },
  "IN": { name: "Indiana", diesel: 0.63, gasoline: 0.37 },
  "KS": { name: "Kansas", diesel: 0.26, gasoline: 0.24 },
  "KY": { name: "Kentucky", diesel: 0.105, gasoline: 0.045 },
  "LA": { name: "Louisiana", diesel: 0.2, gasoline: 0.2 },
  "MA": { name: "Massachusetts", diesel: 0.24, gasoline: 0.24 },
  "MB": { name: "Manitoba", diesel: 0.3383, gasoline: 0.3383 },
  "MD": { name: "Maryland", diesel: 0.4675, gasoline: 0.46 },
  "ME": { name: "Maine", diesel: 0.312, gasoline: null },
  "MI": { name: "Michigan", diesel: 0.524, gasoline: 0.524 },
  "MN": { name: "Minnesota", diesel: 0.326, gasoline: 0.326 },
  "MO": { name: "Missouri", diesel: 0.295, gasoline: 0.295 },
  "MS": { name: "Mississippi", diesel: 0.24, gasoline: 0.24 },
  "MT": { name: "Montana", diesel: 0.2975, gasoline: null },
  "NB": { name: "New Brunswick", diesel: 0.4182, gasoline: 0.2942 },
  "NC": { name: "North Carolina", diesel: 0.41, gasoline: 0.41 },
  "ND": { name: "North Dakota", diesel: 0.23, gasoline: 0.23 },
  "NE": { name: "Nebraska", diesel: 0.318, gasoline: 0.318 },
  "NH": { name: "New Hampshire", diesel: 0.222, gasoline: null },
  "NJ": { name: "New Jersey", diesel: 0.561, gasoline: 0.491 },
  "NL": { name: "Newfoundland", diesel: 0.2572, gasoline: 0.203 },
  "NM": { name: "New Mexico", diesel: 0.21, gasoline: 0.12 },
  "NS": { name: "Nova Scotia", diesel: 0.4168, gasoline: 0.4196 },
  "NV": { name: "Nevada", diesel: 0.27, gasoline: 0.23 },
  "NY": { name: "New York", diesel: 0.3805, gasoline: 0.397 },
  "OH": { name: "Ohio", diesel: 0.47, gasoline: 0.385 },
  "OK": { name: "Oklahoma", diesel: 0.19, gasoline: 0.19 },
  "ON": { name: "Ontario", diesel: 0.2436, gasoline: 0.2436 },
  "OR": { name: "Oregon", diesel: null, gasoline: null },
  "PA": { name: "Pennsylvania", diesel: 0.741, gasoline: 0.576 },
  "PE": { name: "Prince Edward Island", diesel: 0.383, gasoline: 0.2293 },
  "QC": { name: "Quebec", diesel: 0.5468, gasoline: 0.5197 },
  "RI": { name: "Rhode Island", diesel: 0.4, gasoline: 0.4 },
  "SC": { name: "South Carolina", diesel: 0.28, gasoline: 0.28 },
  "SD": { name: "South Dakota", diesel: 0.28, gasoline: 0.28 },
  "SK": { name: "Saskatchewan", diesel: 0.406, gasoline: 0.406 },
  "TN": { name: "Tennessee", diesel: 0.27, gasoline: 0.26 },
  "TX": { name: "Texas", diesel: 0.2, gasoline: 0.2 },
  "UT": { name: "Utah", diesel: 0.379, gasoline: 0.319 },
  "VA": { name: "Virginia", diesel: 0.143, gasoline: 0.153 },
  "VT": { name: "Vermont", diesel: 0.31, gasoline: null },
  "WA": { name: "Washington", diesel: 0.595, gasoline: 0.565 },
  "WI": { name: "Wisconsin", diesel: 0.329, gasoline: 0.329 },
  "WV": { name: "West Virginia", diesel: 0.357, gasoline: 0.357 },
  "WY": { name: "Wyoming", diesel: 0.24, gasoline: 0.24 },
};

export const IFTA_QUARTER = "3Q2026";
export const IFTA_UPDATED = "August 22, 2026";
export const IFTA_SOURCE = "IFTA, Inc. official Tax Rate Matrix (iftach.org)";