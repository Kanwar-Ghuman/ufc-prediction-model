import { eventDate, pct, stamp } from "@/lib/api";
import type { Bout, CardDetail, GradedFight, Headline, Scorecard } from "@/lib/api";
import { BoutCard } from "@/components/BoutCard";
import { FightMotion } from "@/components/FightMotion";

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
      <div className="event-hero">
        <div>
          <p className="label text-[10px] text-ash">Fight by fight <span className="mx-2">/</span> {eyebrow ?? (card.upcoming ? "Up next" : "Latest event")}</p>
          <h1 className="display event-title">{card.event}</h1>
          <p className="event-meta">{eventDate(card.date, { year: "numeric" })} <span className="mx-2">/</span> {card.bouts.length} bouts</p>
          <p className="mt-3 text-xs text-mist">Independent predictions. Every pick on the record.</p>
        </div>
        <FightMotion />
      </div>
      {card.headline && <HeadlineCall headline={card.headline} />}
      <p className="mt-2 text-[10px] text-mist">Predictions recorded {stamp(card.predicted_at)}</p>
    </header>
  );
}

/**
 * The model's most confident prediction on the card, said in words —
 * word-for-word from the API statement — not just a percentage.
 * The percentages ride along underneath, but the sentence leads.
 */
function HeadlineCall({ headline }: { headline: Headline }) {
  return <div className="headline-note">
    <span className="label text-[9px] text-mist">Strongest pick</span>
    <strong>{headline.statement}</strong>
    <span className="text-ash">{pct(headline.confidence)} to win · {pct(headline.outcome_probability)} exact outcome</span>
  </div>;
}

/** The band that separates MAIN CARD from PRELIMS. */
function SegmentBand({ title, bouts }: { title: string; bouts: Bout[] }) {
  const called = bouts.filter((b) => b.called);
  const lean =
    called.length > 0
      ? called.reduce((sum, b) => sum + b.confidence, 0) / called.length
      : null;
  return (
    <div className="section-heading">
      <h2 className="display">{title}</h2>
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
    <div>
      <nav className="card-navigation" aria-label="Fight card sections">
        {segments(card.bouts).map((segment, index) => <a key={segment.title} href={`#segment-${index}`}>{segment.title}<span>{segment.bouts.length}</span></a>)}
      </nav>
      {segments(card.bouts).map((segment, segmentIndex) => (
        <section key={segment.title} id={`segment-${segmentIndex}`}>
          <SegmentBand title={segment.title} bouts={segment.bouts} />
          <div className="bout-grid">{segment.bouts.map((bout, boutIndex) => (
            <BoutCard
              key={`${bout.f1}-${bout.f2}`}
              bout={bout}
              role={segmentIndex === 0 && boutIndex === 0 ? "Main event" : segmentIndex === 0 && boutIndex === 1 ? "Co-main event" : undefined}
              result={results.get(`${bout.f1}|${bout.f2}`)}
            />
          ))}</div>
        </section>
      ))}
    </div>
  );
}
