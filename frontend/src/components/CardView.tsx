import { eventDate, pct, stamp } from "@/lib/api";
import type { Bout, CardDetail, GradedFight, Headline, Scorecard } from "@/lib/api";
import { BoutCard } from "@/components/BoutCard";

function segments(bouts: Bout[]): { title: string; bouts: Bout[] }[] {
  const out: { title: string; bouts: Bout[] }[] = [];
  for (const bout of bouts) {
    const title = bout.section ?? "Full card";
    const last = out.at(-1);
    if (last && last.title === title) last.bouts.push(bout);
    else out.push({ title, bouts: [bout] });
  }
  return out;
}

function resultIndex(scorecard: Scorecard | null): Map<string, GradedFight> {
  const index = new Map<string, GradedFight>();
  for (const fight of scorecard?.fights ?? []) {
    index.set(`${fight.f1}|${fight.f2}`, fight);
    index.set(`${fight.f2}|${fight.f1}`, fight);
  }
  return index;
}

export function EventHero({
  card,
  eyebrow,
}: {
  card: CardDetail;
  eyebrow?: string;
}) {
  return (
    <header className="border border-line bg-paper">
      <div className="border-b-4 border-blood px-5 py-5 sm:px-8 sm:py-7">
        <p className="label text-[11px] text-blood">
          {eyebrow ?? (card.upcoming ? "Next card" : "Latest card")}
        </p>
        <h1 className="display mt-2 text-3xl sm:text-5xl">{card.event}</h1>
        <p className="label mt-2 text-xs text-ash sm:text-sm">
          {eventDate(card.date, { year: "numeric" })} · {card.bouts.length} bouts
        </p>
      </div>
      {card.headline && <HeadlineCall headline={card.headline} />}
      <p className="px-5 py-2 text-xs text-mist sm:px-8">
        Probabilities frozen {stamp(card.predicted_at)} by{" "}
        <code className="font-mono">octagon predict</code> — every rerun of the
        model republishes this page.
      </p>
    </header>
  );
}

/**
 * The model's most confident prediction on the card, said in words —
 * word-for-word from the API statement — not just a percentage.
 * The percentages ride along underneath, but the sentence leads.
 */
function HeadlineCall({ headline }: { headline: Headline }) {
  return (
    <div className="border-b border-line px-5 py-5 sm:px-8 sm:py-6">
      <p className="label text-[11px] text-mist">
        The model&apos;s most confident call
        {headline.weight_class ? ` · ${headline.weight_class}` : ""}
      </p>
      <p className="display mt-3 text-2xl leading-tight text-ink sm:text-4xl">
        {headline.statement}
      </p>
      <p className="mt-3 text-xs text-ash">
        <span className="font-mono text-blood">{pct(headline.confidence)}</span>{" "}
        to win · this exact ending{" "}
        <span className="font-mono">{pct(headline.outcome_probability)}</span>
      </p>
    </div>
  );
}

/** The band that separates MAIN CARD from PRELIMS. */
function SegmentBand({ title, bouts }: { title: string; bouts: Bout[] }) {
  const called = bouts.filter((b) => b.called);
  const lean =
    called.length > 0
      ? called.reduce((sum, b) => sum + b.confidence, 0) / called.length
      : null;
  return (
    <div className="flex flex-wrap items-baseline justify-between gap-2 border-b-2 border-ink pb-2">
      <h2 className="display text-2xl sm:text-3xl">{title}</h2>
      <p className="min-w-0 text-xs text-ash">
        {bouts.length} bouts
        {lean !== null && (
          <>
            {" · "}
            <span className="font-mono">{pct(lean)}</span> mean confidence on{" "}
            {called.length} calls
          </>
        )}
      </p>
    </div>
  );
}

export function CardView({
  card,
  scorecard,
}: {
  card: CardDetail;
  scorecard?: Scorecard | null;
}) {
  const results = resultIndex(scorecard ?? null);
  return (
    <div className="space-y-8">
      {segments(card.bouts).map((segment) => (
        <section key={segment.title} className="space-y-3">
          <SegmentBand title={segment.title} bouts={segment.bouts} />
          {segment.bouts.map((bout) => (
            <BoutCard
              key={`${bout.f1}-${bout.f2}`}
              bout={bout}
              result={results.get(`${bout.f1}|${bout.f2}`)}
            />
          ))}
        </section>
      ))}
    </div>
  );
}
