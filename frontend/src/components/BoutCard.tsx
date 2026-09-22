import { num, pct } from "@/lib/api";
import type { Bout, GradedFight } from "@/lib/api";
import { Nameplate, Portrait } from "@/components/Fighter";

function ProbabilityBar({
  left,
  muted,
}: {
  left: number;
  muted?: boolean;
}) {
  const lead = muted ? "bg-rail" : "bg-blood";
  const trail = muted ? "bg-line" : "bg-rail";
  const leftLeads = left >= 0.5;
  return (
    <div className="flex h-1 w-full gap-0.5 overflow-hidden rounded-full">
      <div
        className={`rounded-full ${leftLeads ? lead : trail}`}
        style={{ width: `${left * 100}%` }}
      />
      <div
        className={`rounded-full ${leftLeads ? trail : lead}`}
        style={{ width: `${(1 - left) * 100}%` }}
      />
    </div>
  );
}

function Tag({
  children,
  tone = "plain",
}: {
  children: React.ReactNode;
  tone?: "plain" | "gold" | "solid";
}) {
  const tones = {
    plain: "bg-raise text-ash",
    gold: "bg-gold/15 text-gold",
    solid: "bg-ink text-shell",
  };
  return (
    <span className={`rounded-full px-2 py-0.5 text-[11px] ${tones[tone]}`}>
      {children}
    </span>
  );
}

/** Weight class, rounds, title/no-call flags. */
function BoutHeader({ bout }: { bout: Bout }) {
  const circ = [
    bout.context?.f1?.circumstances,
    bout.context?.f2?.circumstances,
  ];
  const shortNotice = circ.some(
    (c) => c?.short_notice || c?.late_replacement,
  );
  // UFC fights === 0 is a debut. A pro record in the media cache is not.
  const debut = [bout.f1_ufc_fights, bout.f2_ufc_fights].some(
    (n) => n === 0,
  );
  return (
    <div className="flex flex-wrap items-center justify-center gap-2 px-4 pt-4 text-[11px] text-mist">
      <span>
        {bout.weight_class ?? "Catchweight"} · {bout.scheduled_rounds} rounds
      </span>
      {bout.scheduled_rounds === 5 && <Tag tone="solid">Main event</Tag>}
      {!bout.called && <Tag>No call</Tag>}
      {shortNotice && <Tag tone="gold">Short notice</Tag>}
      {debut && <Tag>UFC debut</Tag>}
    </div>
  );
}

/** The model's call — words first, percentages secondary. */
function ModelStrip({ bout, result }: { bout: Bout; result?: GradedFight }) {
  const p1 = bout.p_f1_wins;
  // A no-call has no favourite to colour. Leaving the leading number red
  // would read as a pick the model explicitly declined to make.
  const lead = bout.called ? "text-blood" : "text-ash";
  const selectedOutcome = bout.top_outcome
    ? `${bout.pick} ${bout.top_outcome.label}`
    : `picks ${bout.pick}`;
  const prediction = bout.called
    ? bout.statement ?? selectedOutcome
    : `Lean: ${selectedOutcome}`;

  return (
    <div className="px-4 pb-4">
      <div className="rounded-xl bg-shell/60 px-4 py-4 text-center">
        <p className="text-[11px] text-mist">
          {bout.called ? "Prediction" : "Low confidence"}
        </p>
        {result ? (
          <p
            className={`display display-title mt-1.5 text-lg ${
              !bout.called
                ? "text-mist"
                : result.correct
                  ? "text-hit"
                  : "text-miss"
            }`}
          >
            {!bout.called
              ? "Abstained"
              : result.correct
                ? "Called it"
                : "Missed"}
          </p>
        ) : (
          <p
            className={`display display-title mt-1.5 text-lg sm:text-2xl ${
              bout.called ? "text-ink" : "text-mist"
            }`}
          >
            {prediction}
          </p>
        )}
        {bout.top_outcome && !result && <OutcomeBreakdown bout={bout} />}

        <div className="mt-4 flex items-center justify-between gap-4">
          <span className={`display text-base ${p1 >= 0.5 ? lead : "text-ash"}`}>
            {pct(p1)}
          </span>
          <span className="text-[11px] text-mist">Win probability</span>
          <span className={`display text-base ${p1 < 0.5 ? lead : "text-ash"}`}>
            {pct(1 - p1)}
          </span>
        </div>
        <div className="mt-1.5">
          <ProbabilityBar left={p1} muted={!bout.called} />
        </div>
      </div>
    </div>
  );
}

/** The selected method, and the round it most likely lands in. */
function OutcomeBreakdown({ bout }: { bout: Bout }) {
  const outcome = bout.top_outcome;
  const method =
    outcome.method === "DEC"
      ? "Decision"
      : outcome.method === "SUB"
        ? "Submission"
        : "KO/TKO";
  const tone = bout.called ? "text-blood" : "text-ash";

  return (
    <div className="mt-3 flex flex-wrap items-baseline justify-center gap-x-5 gap-y-1 text-xs text-mist">
      <span>
        {method} <span className={`num ${tone}`}>{pct(outcome.method_probability)}</span>
      </span>
      {outcome.round != null && (
        <span>
          Round {outcome.round}{" "}
          <span className={`num ${tone}`}>{pct(outcome.probability)}</span>
        </span>
      )}
    </div>
  );
}

/** Result line for a card that has already happened. */
function ResultLine({ result }: { result: GradedFight }) {
  const finish =
    result.method && !result.method.endsWith("DEC")
      ? `${result.method}, round ${result.end_round}`
      : result.method ?? "decision";
  return (
    <div className="flex flex-wrap items-center justify-center gap-x-2 border-t border-line px-4 py-2.5 text-center text-xs">
      <span className="text-mist">Result</span>
      <span className="display text-sm text-ink">{result.winner}</span>
      <span className="text-ash">{finish}</span>
    </div>
  );
}

/** The joint distribution over every way the fight can end. */
function EndingGrid({ bout }: { bout: Bout }) {
  const rows = [
    [`${bout.f1} by KO/TKO`, "f1_ko", bout.methods.f1_ko],
    [`${bout.f1} by submission`, "f1_sub", bout.methods.f1_sub],
    [`${bout.f2} by KO/TKO`, "f2_ko", bout.methods.f2_ko],
    [`${bout.f2} by submission`, "f2_sub", bout.methods.f2_sub],
  ] as const;

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-xs whitespace-nowrap">
        <thead>
          <tr className="border-b border-line text-left text-mist">
            <th className="py-1.5 pr-3 font-medium">Ending</th>
            {bout.by_round.map((r) => (
              <th key={r.round} className="py-1.5 pr-3 font-medium">
                R{r.round}
              </th>
            ))}
            <th className="py-1.5 font-medium">Any</th>
          </tr>
        </thead>
        <tbody className="num">
          {rows.map(([label, key, total]) => (
            <tr key={key} className="border-b border-line/50 last:border-0">
              <td className="py-1.5 pr-3 font-sans text-ash">{label}</td>
              {bout.by_round.map((r) => (
                <td key={r.round} className="py-1.5 pr-3 text-mist">
                  {pct(r[key], 1)}
                </td>
              ))}
              <td className="py-1.5 text-ink">{pct(total, 1)}</td>
            </tr>
          ))}
          <tr>
            <td className="py-1.5 pr-3 font-sans text-ash">Decision</td>
            {bout.by_round.map((r) => (
              <td key={r.round} className="py-1.5 pr-3 text-mist">
                —
              </td>
            ))}
            <td className="py-1.5 text-ink">{pct(bout.p_decision, 1)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

function SubHead({ children }: { children: React.ReactNode }) {
  return <h4 className="text-xs text-mist">{children}</h4>;
}

function FightResearch({ bout }: { bout: Bout }) {
  const research = bout.context?.research ?? [];
  const skill = bout.p_skill;
  const market = bout.p_market;
  if (research.length === 0 && skill == null && market == null) return null;
  return (
    <div>
      <SubHead>Research</SubHead>
      {skill != null && market != null && Number.isFinite(market) && (
        <p className="mt-1.5 text-xs text-ash">
          Model <span className="num">{pct(skill)}</span> vs. market{" "}
          <span className="num">{pct(market)}</span> on{" "}
          <span className="text-ink">{bout.f1}</span>
          {Math.abs(skill - market) >= 0.03
            ? ` — ${skill > market ? "the model likes them more" : "the market likes them more"}`
            : " — they agree"}
          .
        </p>
      )}
      {research.length > 0 && (
        <ul className="mt-1.5 list-disc space-y-1 pl-4 text-xs text-ash marker:text-mist">
          {research.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

function ContextNotes({ bout }: { bout: Bout }) {
  const ctx = bout.context;
  if (!ctx) return null;
  const adjustments = ctx.adjustments ?? [];
  const notes = [
    ...(ctx.f1?.circumstances?.notes ?? []).map((n) => `${bout.f1}: ${n}`),
    ...(ctx.f2?.circumstances?.notes ?? []).map((n) => `${bout.f2}: ${n}`),
  ];
  const styles = [
    ctx.f1?.styles?.length
      ? `${bout.f1}: ${ctx.f1.styles.join(", ")}`
      : null,
    ctx.f2?.styles?.length
      ? `${bout.f2}: ${ctx.f2.styles.join(", ")}`
      : null,
  ].filter(Boolean) as string[];
  const headlines = [
    ...(ctx.f1?.headlines ?? []),
    ...(ctx.f2?.headlines ?? []),
  ].slice(0, 4);
  if (
    adjustments.length === 0 &&
    notes.length === 0 &&
    styles.length === 0 &&
    headlines.length === 0
  ) {
    return null;
  }
  return (
    <div>
      <SubHead>Context</SubHead>
      {styles.length > 0 && (
        <p className="mt-1.5 text-xs text-ash">Style: {styles.join(" · ")}</p>
      )}
      {adjustments.length > 0 && (
        <ul className="mt-1.5 list-disc space-y-1 pl-4 text-xs text-ash marker:text-mist">
          {adjustments.map((a) => (
            <li key={a}>{a}</li>
          ))}
        </ul>
      )}
      {notes.length > 0 && (
        <ul className="mt-1.5 list-disc space-y-1 pl-4 text-xs text-mist marker:text-mist">
          {notes.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
      )}
      {headlines.length > 0 && (
        <ul className="mt-2 space-y-1 text-xs text-ash">
          {headlines.map((h) => (
            <li key={h.title} className="truncate" title={h.title}>
              {h.link ? (
                <a
                  className="underline underline-offset-2 hover:text-ink"
                  href={h.link}
                  rel="noreferrer noopener"
                  target="_blank"
                >
                  {h.title}
                </a>
              ) : (
                h.title
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/**
 * The SHAP contributions frozen with the prediction — what actually moved
 * this pick, rather than a general story about what the model likes.
 */
function Drivers({ bout }: { bout: Bout }) {
  if (bout.drivers.length === 0) return null;
  const widest = Math.max(...bout.drivers.map((d) => Math.abs(d.value)));

  return (
    <div>
      <SubHead>Why</SubHead>
      <p className="mt-1.5 text-xs text-ash">
        Bars right favour <span className="text-ink">{bout.f1}</span>, left{" "}
        <span className="text-ink">{bout.f2}</span>.
      </p>
      <ul className="mt-2.5 space-y-1.5">
        {bout.drivers.map((driver) => (
          <li key={driver.feature} className="flex items-center gap-3 text-xs">
            <span className="w-36 shrink-0 truncate text-ash" title={driver.feature}>
              {driver.feature.replace(/_/g, " ")}
            </span>
            <span className="relative flex h-3 flex-1 items-center">
              <span className="absolute inset-y-0 left-1/2 w-px bg-line" />
              <span
                className={`absolute h-1.5 rounded-full ${
                  driver.value >= 0 ? "left-1/2 bg-blood" : "right-1/2 bg-rail"
                }`}
                style={{ width: `${(Math.abs(driver.value) / widest) * 48}%` }}
              />
            </span>
            <span className="num w-12 shrink-0 text-right text-mist">
              {driver.value >= 0 ? "+" : ""}
              {num(driver.value, 2)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function BoutCard({
  bout,
  result,
}: {
  bout: Bout;
  /** Present once the card has been graded against real results. */
  result?: GradedFight;
}) {
  const p1 = bout.p_f1_wins;
  return (
    <article className="overflow-hidden rounded-2xl border border-line bg-paper">
      <BoutHeader bout={bout} />

      {/*
        Grid, not flex: the two name columns are minmax(0, 1fr), which is the
        only reliable way to let a long surname shrink and wrap instead of
        pushing the whole row past a phone's viewport.
      */}
      <div className="grid grid-cols-[auto_minmax(0,1fr)_auto_minmax(0,1fr)_auto] items-center gap-2 px-3 py-4 sm:gap-4 sm:px-5">
        <Portrait media={bout.f1_media} name={bout.f1} side="left" />
        <Nameplate
          media={bout.f1_media}
          name={bout.f1}
          side="left"
          winner={bout.called && p1 >= 0.5}
        />
        <span className="display px-1 text-xs text-mist sm:text-sm">vs</span>
        <Nameplate
          media={bout.f2_media}
          name={bout.f2}
          side="right"
          winner={bout.called && p1 < 0.5}
        />
        <Portrait media={bout.f2_media} name={bout.f2} side="right" />
      </div>

      <ModelStrip bout={bout} result={result} />
      {result && <ResultLine result={result} />}

      <details className="group border-t border-line">
        <summary className="pressable flex cursor-pointer list-none items-center justify-between px-4 py-3 text-xs text-mist select-none hover:text-ink">
          <span>
            <span className="group-open:hidden">How it ends, and why</span>
            <span className="hidden group-open:inline">Hide detail</span>
          </span>
          <span
            aria-hidden
            className="text-[10px] transition-transform duration-200 group-open:rotate-180 motion-reduce:transition-none"
          >
            ▼
          </span>
        </summary>
        <div className="space-y-5 px-4 pb-5">
          <EndingGrid bout={bout} />
          <FightResearch bout={bout} />
          <ContextNotes bout={bout} />
          <Drivers bout={bout} />
        </div>
      </details>
    </article>
  );
}
