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
    <section className="rounded-2xl border border-line bg-paper p-5 sm:p-6">
      {title && <h2 className="display display-title text-xl">{title}</h2>}
      {subtitle && <p className="mt-1.5 max-w-xl text-sm text-ash">{subtitle}</p>}
      <div className={title || subtitle ? "mt-5" : ""}>{children}</div>
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
      <dt className="text-xs text-mist">{label}</dt>
      <dd className="display display-title mt-1 text-2xl tabular-nums">{value}</dd>
      {hint && <p className="mt-0.5 text-xs text-mist">{hint}</p>}
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
    <div className="rounded-2xl border border-line bg-paper p-5">
      <p
        className={`display display-title text-base ${
          offline ? "text-blood" : "text-ink"
        }`}
      >
        {offline
          ? "API not running"
          : result.kind === "missing"
            ? "Nothing here yet"
            : "Something went wrong"}
      </p>
      <p className="mt-1.5 text-sm text-ash">{result.message}</p>
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
          <tr className="border-b border-line text-left">
            {head.map((h) => (
              <th key={h} className="py-2 pr-4 text-xs font-medium text-mist">
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
  return <tr className="border-b border-line/60 last:border-0">{children}</tr>;
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
      className={`py-2.5 pr-4 ${mono ? "num" : ""} ${
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
    neutral: "bg-raise text-ash",
    good: "bg-hit/15 text-hit",
    bad: "bg-miss/15 text-miss",
    muted: "bg-raise text-mist",
  };
  return (
    <span
      className={`inline-block rounded-full px-2 py-0.5 text-xs whitespace-nowrap ${tones[tone]}`}
    >
      {children}
    </span>
  );
}
