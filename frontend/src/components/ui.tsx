import type { ApiResult } from "@/lib/api";

export function Panel({
  title,
  subtitle,
  children,
}: {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="border border-line bg-paper p-5">
      {title && <h2 className="display text-xl">{title}</h2>}
      {subtitle && <p className="mt-1 max-w-2xl text-sm text-ash">{subtitle}</p>}
      <div className={title || subtitle ? "mt-4" : ""}>{children}</div>
    </section>
  );
}

export function Stat({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <div>
      <dt className="label text-[10px] text-mist">{label}</dt>
      <dd className="display mt-1 text-2xl tabular-nums">{value}</dd>
      {hint && <p className="mt-1 text-xs text-ash">{hint}</p>}
    </div>
  );
}

/** Renders the failure states of `api()` without pretending they're data. */
export function ApiNotice({
  result,
}: {
  result: Extract<ApiResult<unknown>, { ok: false }>;
}) {
  const offline = result.kind === "offline";
  return (
    <div
      className={`border-l-4 bg-paper p-4 text-sm ${
        offline ? "border-blood" : "border-rail"
      }`}
    >
      <p className="label text-xs">
        {offline
          ? "API not running"
          : result.kind === "missing"
            ? "Nothing to show yet"
            : "Something went wrong"}
      </p>
      <p className="mt-1 text-ash">{result.message}</p>
    </div>
  );
}

export function Table({
  head,
  children,
}: {
  head: string[];
  children: React.ReactNode;
}) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b-2 border-ink text-left">
            {head.map((h) => (
              <th key={h} className="label py-2 pr-4 text-[10px] text-ash">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  );
}

export function Row({ children }: { children: React.ReactNode }) {
  return <tr className="border-b border-line last:border-0">{children}</tr>;
}

export function Cell({
  children,
  mono,
  muted,
}: {
  children: React.ReactNode;
  mono?: boolean;
  muted?: boolean;
}) {
  return (
    <td
      className={`py-2 pr-4 ${mono ? "font-mono tabular-nums" : ""} ${
        muted ? "text-ash" : "text-ink"
      }`}
    >
      {children}
    </td>
  );
}

export function Badge({
  children,
  tone = "neutral",
}: {
  children: React.ReactNode;
  tone?: "neutral" | "good" | "bad" | "muted";
}) {
  const tones = {
    neutral: "border-rail text-ash",
    good: "border-hit/40 text-hit",
    bad: "border-miss/40 text-miss",
    muted: "border-line text-mist",
  };
  return (
    <span
      className={`label inline-block border px-1.5 py-0.5 text-[10px] whitespace-nowrap ${tones[tone]}`}
    >
      {children}
    </span>
  );
}
