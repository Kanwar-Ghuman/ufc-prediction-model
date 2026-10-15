#!/usr/bin/env node
/** Pull the local Octagon API into src/data/snapshot.json for Vercel. */

import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const base = process.env.API_BASE ?? "http://127.0.0.1:8000";
const out = join(dirname(fileURLToPath(import.meta.url)), "../src/data/snapshot.json");

async function get(path) {
  const response = await fetch(`${base}${path}`);
  if (response.status === 404) return null;
  if (!response.ok) {
    throw new Error(`${path} -> ${response.status}`);
  }
  return response.json();
}

const snapshot = {};
for (const path of [
  "/api/overview",
  "/api/next-card",
  "/api/cards",
  "/api/metrics/valid",
  "/api/metrics/test",
  "/api/calibration/valid",
  "/api/calibration/test",
]) {
  snapshot[path] = await get(path);
}

const cards = snapshot["/api/cards"] ?? [];
for (const card of cards) {
  snapshot[`/api/cards/${card.slug}`] = await get(`/api/cards/${card.slug}`);
  snapshot[`/api/cards/${card.slug}/scorecard`] = await get(
    `/api/cards/${card.slug}/scorecard`,
  );
}

await mkdir(dirname(out), { recursive: true });
await writeFile(out, `${JSON.stringify(snapshot)}\n`);
console.log(`Wrote ${out} (${cards.length} cards)`);

const portraits = new Set();
for (const value of Object.values(snapshot)) {
  const bouts = value && typeof value === "object" ? value.bouts : null;
  if (!Array.isArray(bouts)) continue;
  for (const bout of bouts) {
    for (const side of ["f1_media", "f2_media"]) {
      const portrait = bout?.[side]?.portrait;
      if (typeof portrait === "string") portraits.add(portrait);
    }
  }
}

const portraitDir = join(dirname(out), "../../public/portraits");
await mkdir(portraitDir, { recursive: true });
let saved = 0;
for (const path of portraits) {
  const file = path.split("/").pop();
  if (!file || file === "." || file === ".." || file.includes("..")) continue;
  const response = await fetch(`${base}${path}`);
  if (!response.ok) {
    console.warn(`missing portrait ${path} (${response.status})`);
    continue;
  }
  await writeFile(join(portraitDir, file), Buffer.from(await response.arrayBuffer()));
  saved += 1;
}
console.log(`Wrote ${saved}/${portraits.size} portraits to ${portraitDir}`);
