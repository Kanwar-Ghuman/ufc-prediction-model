import Link from "next/link";

import { api, eventDate } from "@/lib/api";
import type { CardSummary } from "@/lib/api";
import { ApiNotice, Panel } from "@/components/ui";

export const dynamic = "force-dynamic";

export default async function CardsPage() {
  const cards = await api<CardSummary[]>("/api/cards");
  const today = new Date().toISOString().slice(0, 10);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="display display-hero text-4xl sm:text-5xl">All cards</h1>
        <p className="mt-3 max-w-lg text-sm text-ash">
          Every card, frozen before it happened and graded against those exact
          numbers once results land.
        </p>
      </div>

      {!cards.ok ? (
        <ApiNotice result={cards} />
      ) : cards.data.length === 0 ? (
        <Panel>
          <p className="text-sm text-ash">
            No cards predicted yet. Run{" "}
            <code className="num text-ink">octagon fetch-card</code>, then{" "}
            <code className="num text-ink">octagon predict</code>.
          </p>
        </Panel>
      ) : (
        <ul className="space-y-2.5">
          {cards.data.map((card) => (
            <li key={card.slug}>
              <Link
                href={`/cards/${card.slug}`}
                className="pressable block rounded-2xl border border-line bg-paper px-5 py-4 hover:border-rail hover:bg-raise"
              >
                <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
                  <span className="display display-title text-lg">
                    {card.event}
                  </span>
                  <span className="text-xs text-ash">
                    {eventDate(card.date, { year: "numeric" })}
                  </span>
                </div>
                <p className="mt-1 text-xs text-mist">
                  {card.n_bouts} bouts ·{" "}
                  {card.date >= today ? "upcoming" : "graded"}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
