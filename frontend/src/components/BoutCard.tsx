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
    <div className="flex h-[3px] w-full overflow-hidden bg-line">
      <div
        className={leftLeads ? lead : trail}
        style={{ width: `${left * 100}%` }}
      />
      <div
        className={leftLeads ? trail : lead}
        style={{ width: `${(1 - left) * 100}%` }}
      />
    </div>
  );
}

function BoutHeader({ bout, role }: { bout: Bout; role?: string }) {
  const shortNotice = [bout.context?.f1?.circumstances, bout.context?.f2?.circumstances].some(c => c?.short_notice || c?.late_replacement);
  return <div className="bout-heading">
    <span className={role ? "bout-role" : ""}>{role ?? bout.weight_class ?? "Catchweight"}</span>
    <span>{role ? `${bout.weight_class ?? "Catchweight"} · ` : ""}{bout.scheduled_rounds} rounds</span>
    {shortNotice && <span>Short notice</span>}
    {[bout.f1_ufc_fights, bout.f2_ufc_fights].some(n => n === 0) && <span>UFC debut</span>}
  </div>;
}

function ModelStrip({ bout }: { bout: Bout }) {
  const p1 = bout.p_f1_wins;
  return <div>
    <div className="probability-row">
      <strong className={bout.called && p1 >= .5 ? "favored" : ""}>{pct(p1)}</strong>
      <span>Win probability</span>
      <strong className={bout.called && p1 < .5 ? "favored" : ""}>{pct(1 - p1)}</strong>
    </div>
    <ProbabilityBar left={p1} muted={!bout.called} />
    <div className="pick-line">
      <span className="label text-[9px] text-mist">{bout.called ? "The pick" : "Model lean · no call"}</span>
      <p>{bout.statement ?? `${bout.pick} ${bout.top_outcome?.label ?? "to win"}`}</p>
    </div>
  </div>;
}

/** The selected method first, then the conditional round and exact joint P. */
function OutcomeBreakdown({ bout }: { bout: Bout }) {
  const outcome = bout.top_outcome;
  const method =
    outcome.method === "DEC"
      ? "Decision"
      : outcome.method === "SUB"
        ? "Submission"
        : "KO/TKO";
  const valueTone = bout.called ? "text-blood" : "text-ash";
  const cell = "border-b border-line py-2";

  return (
    <div
      className={`mx-auto mt-3 grid max-w-xl gap-1 text-left ${
        outcome.round == null ? "grid-cols-2" : "grid-cols-2"
      }`}
    >
      <div className={cell}>
        <p className="label text-[9px] text-mist">Method</p>
        <p className={`display mt-0.5 text-sm ${valueTone}`}>{method}</p>
      </div>
      <div className={cell}>
        <p className="label text-[9px] text-mist">Winner + method</p>
        <p className={`font-mono text-sm font-semibold ${valueTone}`}>
          {pct(outcome.method_probability)}
        </p>
      </div>
      {outcome.round != null && outcome.round_probability != null && (
        <>
          <div className={cell}>
            <p className="label text-[9px] text-mist">Exact round</p>
            <p className={`display mt-0.5 text-sm ${valueTone}`}>
              Round {outcome.round}
            </p>
            <p className="text-[9px] text-mist">
              {pct(outcome.round_probability)} within method
            </p>
          </div>
          <div className={cell}>
            <p className="label text-[9px] text-mist">Full outcome</p>
            <p className={`font-mono text-sm font-semibold ${valueTone}`}>
              {pct(outcome.probability)}
            </p>
            <p className="text-[9px] text-mist">winner + method + round</p>
          </div>
        </>
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
    <div className="flex flex-wrap items-center justify-center gap-x-2 border-t border-line bg-ink px-4 py-1.5 text-center">
      <span className="label text-[10px] text-paper/80">Result · {result.called ? (result.correct ? "Correct pick" : "Missed pick") : "No call"}</span>
      <span className="display text-sm text-paper">{result.winner}</span>
      <span className="text-xs text-paper/80">{finish}</span>
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
          <tr className="border-b border-line text-left">
            <th className="label py-1 pr-3 text-[10px] font-medium text-mist">
              Ending
            </th>
            {bout.by_round.map((r) => (
              <th
                key={r.round}
                className="label py-1 pr-3 text-[10px] font-medium text-mist"
              >
                R{r.round}
              </th>
            ))}
            <th className="label py-1 text-[10px] font-medium text-mist">Any</th>
          </tr>
        </thead>
        <tbody className="font-mono tabular-nums">
          {rows.map(([label, key, total]) => (
            <tr key={key} className="border-b border-line/60 last:border-0">
              <td className="py-1 pr-3 font-sans text-ash">{label}</td>
              {bout.by_round.map((r) => (
                <td key={r.round} className="py-1 pr-3 text-ash">
                  {pct(r[key], 1)}
                </td>
              ))}
              <td className="py-1 font-semibold text-ink">{pct(total, 1)}</td>
            </tr>
          ))}
          <tr>
            <td className="py-1 pr-3 font-sans text-ash">
              decision (either fighter)
            </td>
            {bout.by_round.map((r) => (
              <td key={r.round} className="py-1 pr-3 text-mist">
                —
              </td>
            ))}
            <td className="py-1 font-semibold text-ink">
              {pct(bout.p_decision, 1)}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

function FightResearch({ bout }: { bout: Bout }) {
  const research = bout.context?.research ?? [];
  const skill = bout.p_skill;
  const market = bout.p_market;
  if (research.length === 0 && skill == null && market == null) return null;
  return (
    <div>
      <h4 className="label text-[10px] text-mist">Fight research</h4>
      {skill != null && market != null && Number.isFinite(market) && (
        <p className="mt-1 text-xs text-ash">
          Research model {pct(skill)} vs. market {pct(market)} for{" "}
          <span className="text-ink">{bout.f1}</span>
          {Math.abs(skill - market) >= 0.03
            ? ` — ${skill > market ? "research likes them more" : "market likes them more"}`
            : " — they agree"}
          .
        </p>
      )}
      {research.length > 0 && (
        <ul className="mt-1 list-disc space-y-0.5 pl-4 text-xs text-ash">
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
      <h4 className="label text-[10px] text-mist">Day-before context</h4>
      {styles.length > 0 && (
        <p className="mt-1 text-xs text-ash">Style: {styles.join(" · ")}</p>
      )}
      {adjustments.length > 0 && (
        <ul className="mt-1 list-disc space-y-0.5 pl-4 text-xs text-ash">
          {adjustments.map((a) => (
            <li key={a}>{a}</li>
          ))}
        </ul>
      )}
      {notes.length > 0 && (
        <ul className="mt-1 list-disc space-y-0.5 pl-4 text-xs text-mist">
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
      <h4 className="label text-[10px] text-mist">Why</h4>
      <p className="mt-1 text-xs text-ash">
        Log-odds pull on the pick. Bars to the right favour{" "}
        <span className="text-ink">{bout.f1}</span>, to the left{" "}
        <span className="text-ink">{bout.f2}</span>.
      </p>
      <ul className="mt-2 space-y-1">
        {bout.drivers.map((driver) => (
          <li key={driver.feature} className="flex items-center gap-2 text-xs">
            <span className="w-40 shrink-0 truncate text-ash" title={driver.feature}>
              {driver.feature.replace(/_/g, " ")}
            </span>
            <span className="relative flex h-3 flex-1 items-center">
              <span className="absolute inset-y-0 left-1/2 w-px bg-line" />
              <span
                className={`absolute h-2 ${
                  driver.value >= 0 ? "left-1/2 bg-blood" : "right-1/2 bg-rail"
                }`}
                style={{ width: `${(Math.abs(driver.value) / widest) * 48}%` }}
              />
            </span>
            <span className="w-12 shrink-0 text-right font-mono text-mist">
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
  role,
}: {
  bout: Bout;
  role?: string;
  /** Present once the card has been graded against real results. */
  result?: GradedFight;
}) {
  const p1 = bout.p_f1_wins;
  return (
    <article className="bout-card">
      <BoutHeader bout={bout} role={role} />
      <div className="faceoff">
        <div className="fighter-side">
          <Portrait media={bout.f1_media} name={bout.f1} side="left" />
          <Nameplate media={bout.f1_media} name={bout.f1} side="left" winner={bout.called && p1 >= .5} />
        </div>
        <span className="versus">vs</span>
        <div className="fighter-side">
          <Portrait media={bout.f2_media} name={bout.f2} side="right" />
          <Nameplate media={bout.f2_media} name={bout.f2} side="right" winner={bout.called && p1 < .5} />
        </div>
      </div>
      <ModelStrip bout={bout} />
      {result && <ResultLine result={result} />}

      <details className="bout-details group">
        <summary aria-label={`Prediction details for ${bout.f1} versus ${bout.f2}`}>
          <span className="group-open:hidden">Explore prediction</span>
          <span className="hidden group-open:inline">Close prediction</span>
        </summary>
        <div className="space-y-5 border-t border-line pt-4">
          <div className="flex justify-between gap-4 text-xs text-ash">
            <span>{bout.f1_media.country ?? "Country unavailable"}</span>
            <span className="text-right">{bout.f2_media.country ?? "Country unavailable"}</span>
          </div>
          {bout.top_outcome && <OutcomeBreakdown bout={bout} />}
          <EndingGrid bout={bout} />
          <FightResearch bout={bout} />
          <ContextNotes bout={bout} />
          <Drivers bout={bout} />
        </div>
      </details>
    </article>
  );
}
