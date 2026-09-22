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
    <header>
      <p className="label text-[11px] text-blood">
        {eyebrow ?? (card.upcoming ? "Next card" : "Latest card")}
      </p>
      <h1 className="display display-hero mt-3 text-4xl sm:text-6xl">
        {card.event}
      </h1>
      <p className="mt-3 text-sm text-ash">
        {eventDate(card.date, { year: "numeric" })} · {card.bouts.length} bouts
      </p>
      <p className="mt-1 text-xs text-mist">
        Frozen {stamp(card.predicted_at)}
      </p>
      {card.headline && <HeadlineCall headline={card.headline} />}
    </header>
  );
}

/**
 * The model's most confident prediction on the card, said in words —
 * word-for-word from the API statement — not just a percentage.
 */
function HeadlineCall({ headline }: { headline: Headline }) {
  return (
    <div className="mt-6 rounded-2xl border border-line bg-paper p-5 sm:p-6">
      <p className="text-xs text-mist">Most confident call</p>
      <p className="display display-title mt-2 text-2xl text-ink sm:text-3xl">
        {headline.statement}
      </p>
      <p className="mt-2.5 text-sm text-ash">
        <span className="num text-blood">{pct(headline.confidence)}</span> to win
        · <span className="num">{pct(headline.outcome_probability)}</span> this
        exact ending
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
    <div className="flex flex-wrap items-baseline justify-between gap-2 px-1">
      <h2 className="display display-title text-xl sm:text-2xl">{title}</h2>
      <p className="text-xs text-mist">
        {bouts.length} bouts
        {lean !== null && (
          <>
            {" · "}
            <span className="num">{pct(lean)}</span> average confidence
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
    <div className="space-y-10">
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
