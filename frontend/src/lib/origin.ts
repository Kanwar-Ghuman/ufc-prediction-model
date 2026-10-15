const EXPLICIT_API = process.env.NEXT_PUBLIC_API_BASE;
const ON_VERCEL = process.env.VERCEL === "1";

/** Live Python API, or null to read the frozen snapshot shipped with the UI. */
export const liveBase = (): string | null => {
  if (EXPLICIT_API) return EXPLICIT_API;
  if (ON_VERCEL) return null;
  return "http://127.0.0.1:8000";
};

/**
 * Portrait paths in the API are `/api/portraits/<file>`. In dev that file is
 * served by the model API. The deployed site has no API, so `npm run snapshot`
 * copies the same file to `public/portraits` and the page loads it from there.
 */
export const portraitUrl = (path: string | null) => {
  if (!path) return null;
  const base = liveBase();
  if (base) return `${base}${path}`;
  const file = path.split("/").pop();
  if (!file || file === "." || file === ".." || file.includes("..")) return null;
  return `/portraits/${file}`;
};
