import Link from "next/link";

import { api, num, pct, stamp } from "@/lib/api";
import type { NextCard, Overview, SplitMetrics } from "@/lib/api";
import { ApiNotice, Panel } from "@/components/ui";
import { CardView, EventHero } from "@/components/CardView";
import { ScorecardPanel } from "@/components/Scorecard";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [card, overview, test] = await Promise.all([
    api<NextCard>("/api/next-card"),
    api<Overview>("/api/overview"),
    api<SplitMetrics>("/api/metrics/test"),
  ]);

  if (!card.ok) {
    return (
      <div className="space-y-6">
        <div className="border-b-4 border-blood pb-4">
          <h1 className="display text-4xl">Octagon</h1>
          <p className="mt-2 max-w-2xl text-sm text-ash">
            Calibrated win, method and round probabilities for upcoming UFC
            cards.
          </p>
        </div>
        <ApiNotice result={card} />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <EventHero card={card.data} />

      <HeldOutStats
        test={test.ok ? test.data : null}
        updatedAt={overview.ok ? overview.data.updated_at : null}
      />

      {card.data.scorecard && (
        <ScorecardPanel scorecard={card.data.scorecard} />
      )}

      <CardView card={card.data} scorecard={card.data.scorecard} />

      <Panel>
        <p className="text-sm text-ash">
          {overview.ok
            ? overview.data.disclaimer
            : "Educational project. Not betting advice."}
        </p>
      </Panel>
    </div>
  );
}

function HeldOutStats({
  test,
  updatedAt,
}: {
  test: SplitMetrics | null;
  updatedAt: string | null;
}) {
  const shipped = test?.models.find((m) => m.key === "p_blend");
  return (
    <div className="flex flex-wrap items-center gap-x-8 gap-y-3 border border-line bg-paper px-5 py-3">
      <div>
        <p className="label text-[10px] text-mist">Held-out test</p>
        <p className="text-xs text-ash">
          {test
            ? `${test.n_fights.toLocaleString()} fights, ${test.date_range[0]} to ${test.date_range[1]}`
            : "not evaluated yet"}
        </p>
      </div>
      {shipped && (
        <>
          <Figure label="Accuracy" value={pct(shipped.accuracy, 1)} />
          <Figure
            label="Log loss"
            value={num(shipped.log_loss)}
            hint="0.6931 = coin flip"
          />
          <Figure
            label="Calibration"
            value={num(shipped.ece, 3)}
            hint="mean gap, lower is better"
          />
        </>
      )}
      <div className="ml-auto text-right">
        {updatedAt && (
          <p className="text-[11px] text-mist">Model run {stamp(updatedAt)}</p>
        )}
        <Link
          href="/results"
          className="label text-[11px] text-blood hover:underline"
        >
          Full results →
        </Link>
      </div>
    </div>
  );
}

function Figure({
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
      <p className="label text-[10px] text-mist">{label}</p>
      <p className="display text-lg tabular-nums">{value}</p>
      {hint && <p className="text-[10px] text-mist">{hint}</p>}
    </div>
  );
}
