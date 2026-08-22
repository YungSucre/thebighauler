// Endpoint Astro : /llms.txt: généré depuis la navigation (jamais obsolète)
import type { APIRoute } from "astro";
import { SITE, CATEGORIES } from "../config";

export const GET: APIRoute = () => {
  const lines: string[] = [];
  lines.push(`# ${SITE.name}`);
  lines.push("");
  lines.push(`> ${SITE.description}`);
  lines.push("");
  lines.push("The Big Hauler is an independent publisher of practical guides for truck drivers and owner-operators: ELD compliance, dispatch, maintenance, fuel, insurance, and the business side of trucking, organized by topic.");
  lines.push("");
  lines.push("## Guide hubs (verticals)");
  lines.push("");
  for (const cat of CATEGORIES) {
    lines.push(`### ${cat.name}`);
    for (const v of cat.verticals) {
      lines.push(`- [${v.name}](${SITE.url}/guides/${v.id}/)`);
    }
    lines.push("");
  }
  return new Response(lines.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
