import Link from "next/link";

import { api, eventDate } from "@/lib/api";
import type { CardSummary } from "@/lib/api";
import { ApiNotice, Panel } from "@/components/ui";

export const dynamic = "force-dynamic";

export default async function CardsPage() {
  const cards = await api<CardSummary[]>("/api/cards");
  const today = new Date().toISOString().slice(0, 10);

  return (
    <div className="space-y-6">
      <div className="border-b-4 border-blood pb-4">
        <h1 className="display text-4xl">All cards</h1>
        <p className="mt-2 max-w-2xl text-sm text-ash">
          Predictions frozen at the moment they were made, before the fights
          happened. Once results land in the database each card is graded
          against those exact numbers rather than a refit.
        </p>
      </div>

      {!cards.ok ? (
        <ApiNotice result={cards} />
      ) : cards.data.length === 0 ? (
        <Panel>
          <p className="text-sm text-ash">
            No cards predicted yet. Run{" "}
            <code className="font-mono">octagon fetch-card</code>, then{" "}
            <code className="font-mono">
              octagon predict --card cards/&lt;file&gt;.yaml
            </code>
            .
          </p>
        </Panel>
      ) : (
        <ul className="space-y-3">
          {cards.data.map((card) => (
            <li key={card.slug}>
              <Link
                href={`/cards/${card.slug}`}
                className="block border border-line bg-paper p-5 transition-colors hover:border-blood"
              >
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <span className="display text-xl">{card.event}</span>
                  <span className="label text-[11px] text-ash">
                    {eventDate(card.date, { year: "numeric" })}
                  </span>
                </div>
                <p className="mt-1 text-xs text-mist">
                  {card.n_bouts} bouts predicted ·{" "}
                  {card.date >= today ? "upcoming" : "graded once results land"}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
