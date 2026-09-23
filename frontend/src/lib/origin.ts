const EXPLICIT_API = process.env.NEXT_PUBLIC_API_BASE;
const ON_VERCEL = process.env.VERCEL === "1";

/** Live Python API, or null to read the frozen snapshot shipped with the UI. */
export const liveBase = (): string | null => {
  if (EXPLICIT_API) return EXPLICIT_API;
  if (ON_VERCEL) return null;
  return "http://127.0.0.1:8000";
};

/** Portraits live on the model API, which is a different origin in dev. */
export const portraitUrl = (path: string | null) => {
  const base = liveBase();
  return path && base ? `${base}${path}` : null;
};
