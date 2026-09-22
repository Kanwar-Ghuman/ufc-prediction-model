import Link from "next/link";

import { api, num, pct, stamp } from "@/lib/api";
import type { NextCard, Overview, SplitMetrics } from "@/lib/api";
import { ApiNotice } from "@/components/ui";
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
        <div>
          <h1 className="display display-hero text-4xl sm:text-5xl">Octagon</h1>
          <p className="mt-3 max-w-lg text-sm text-ash">
            Calibrated win, method and round probabilities for upcoming UFC
            cards.
          </p>
        </div>
        <ApiNotice result={card} />
      </div>
    );
  }

  return (
    <div className="space-y-10">
      <EventHero card={card.data} />

      <HeldOutStats
        test={test.ok ? test.data : null}
        updatedAt={overview.ok ? overview.data.updated_at : null}
      />

      {card.data.scorecard && (
        <ScorecardPanel scorecard={card.data.scorecard} />
      )}

      <CardView card={card.data} scorecard={card.data.scorecard} />
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
  const shipped =
    test?.models.find((m) => m.key === "p_shipped") ??
    test?.models.find((m) => m.key === "p_blend");
  return (
    <div className="rounded-2xl border border-line bg-paper px-5 py-4 sm:px-6">
      <div className="flex flex-wrap items-start gap-x-10 gap-y-4">
        <div>
          <p className="text-xs text-mist">Held-out test</p>
          <p className="mt-1 text-sm text-ash">
            {test
              ? `${test.n_fights.toLocaleString()} fights since ${test.date_range[0].slice(0, 4)}`
              : "Not evaluated yet"}
          </p>
        </div>
        {shipped && (
          <>
            <Figure label="Accuracy" value={pct(shipped.accuracy, 1)} />
            <Figure
              label="Log loss"
              value={num(shipped.log_loss)}
              hint="coin flip 0.6931"
            />
            <Figure
              label="Calibration"
              value={num(shipped.ece, 3)}
              hint="lower is better"
            />
          </>
        )}
        <div className="ml-auto text-right">
          {updatedAt && (
            <p className="text-xs text-mist">Run {stamp(updatedAt)}</p>
          )}
          <Link
            href="/results"
            className="pressable text-sm text-blood hover:underline"
          >
            Full results
          </Link>
        </div>
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
      <p className="text-xs text-mist">{label}</p>
      <p className="display display-title mt-0.5 text-lg tabular-nums">
        {value}
      </p>
      {hint && <p className="text-xs text-mist">{hint}</p>}
    </div>
  );
}
