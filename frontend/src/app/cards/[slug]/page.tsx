import Link from "next/link";

import { api } from "@/lib/api";
import type { CardDetail, Scorecard } from "@/lib/api";
import { ApiNotice } from "@/components/ui";
import { CardView, EventHero } from "@/components/CardView";
import { ScorecardPanel } from "@/components/Scorecard";

export const dynamic = "force-dynamic";

export default async function CardPage(props: PageProps<"/cards/[slug]">) {
  const { slug } = await props.params;
  const [card, scorecard] = await Promise.all([
    api<CardDetail>(`/api/cards/${slug}`),
    api<Scorecard>(`/api/cards/${slug}/scorecard`),
  ]);

  if (!card.ok) {
    return <ApiNotice result={card} />;
  }

  return (
    <div className="space-y-8">
      <Link href="/cards" className="label text-[11px] text-ash hover:text-ink">
        ← All cards
      </Link>

      <EventHero card={card.data} eyebrow="Frozen prediction" />

      {scorecard.ok && <ScorecardPanel scorecard={scorecard.data} />}

      <CardView
        card={card.data}
        scorecard={scorecard.ok ? scorecard.data : null}
      />
    </div>
  );
}
