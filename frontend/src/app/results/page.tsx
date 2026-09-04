import { api, num, pct } from "@/lib/api";
import type { Calibration, SplitMetrics } from "@/lib/api";
import { ApiNotice, Cell, Panel, Row, Table } from "@/components/ui";
import { ReliabilityChart } from "@/components/ReliabilityChart";

export const dynamic = "force-dynamic";

const SPLITS = [
  {
    split: "valid",
    title: "Validation (2022–2023)",
    subtitle:
      "Used during development to choose between models. This era has odds coverage, so it is the only place a fair model-vs-market comparison exists.",
  },
  {
    split: "test",
    title: "Test (2024 onward)",
    subtitle:
      "Touched once, at the end. The odds source stops in 2023, so there is no market row here.",
  },
];

export default function ResultsPage() {
  return (
    <div className="space-y-8">
      <div className="border-b-4 border-blood pb-4">
        <h1 className="display text-4xl">Results</h1>
        <p className="mt-2 max-w-2xl text-sm text-ash">
          Walk-forward evaluation: for every fight, the model is trained only on
          fights that happened before it. A coin flip scores 0.6931 log loss and
          0.25 Brier — those are the numbers to beat.
        </p>
      </div>

      {SPLITS.map((s) => (
        <Section key={s.split} {...s} />
      ))}
    </div>
  );
}

async function Section({
  split,
  title,
  subtitle,
}: {
  split: string;
  title: string;
  subtitle: string;
}) {
  const [metrics, calibration] = await Promise.all([
    api<SplitMetrics>(`/api/metrics/${split}`),
    api<Calibration>(`/api/calibration/${split}`),
  ]);

  return (
    <div className="space-y-4">
      <Panel title={title} subtitle={subtitle}>
        {metrics.ok ? (
          <>
            <Table
              head={["Model", "n", "Log loss", "Accuracy", "Brier", "AUC", "ECE"]}
            >
              {metrics.data.models.map((m) => (
                <Row key={m.key}>
                  <Cell>
                    {m.model}
                    <span className="block text-xs text-mist">{m.note}</span>
                  </Cell>
                  <Cell mono muted>
                    {m.n.toLocaleString()}
                  </Cell>
                  <Cell mono>{num(m.log_loss)}</Cell>
                  <Cell mono>{pct(m.accuracy, 1)}</Cell>
                  <Cell mono muted>
                    {num(m.brier)}
                  </Cell>
                  <Cell mono muted>
                    {num(m.roc_auc, 3)}
                  </Cell>
                  <Cell mono muted>
                    {num(m.ece, 3)}
                  </Cell>
                </Row>
              ))}
            </Table>

            {metrics.data.abstain && (
              <div className="mt-6">
                <h3 className="label text-[10px] text-mist">
                  Abstain trade-off
                </h3>
                <p className="mt-1 mb-3 text-sm text-ash">
                  Widening the no-call band raises accuracy on the fights that
                  remain, by answering fewer of them. Shipped band:{" "}
                  <span className="font-mono">
                    {metrics.data.abstain.shipped_band.join(" – ")}
                  </span>
                  .
                </p>
                <Table head={["No-call band", "Coverage", "Accuracy", "Fights"]}>
                  {metrics.data.abstain.points.map((p) => (
                    <Row key={p.band.join()}>
                      <Cell mono>{p.band.join(" – ")}</Cell>
                      <Cell mono muted>
                        {pct(p.coverage)}
                      </Cell>
                      <Cell mono>{pct(p.accuracy, 1)}</Cell>
                      <Cell mono muted>
                        {p.n.toLocaleString()}
                      </Cell>
                    </Row>
                  ))}
                </Table>
              </div>
            )}
          </>
        ) : (
          <ApiNotice result={metrics} />
        )}
      </Panel>

      {calibration.ok && (
        <Panel
          title="Calibration"
          subtitle="When the model says 70%, does it happen 70% of the time?"
        >
          <ReliabilityChart series={calibration.data.series} />
        </Panel>
      )}
    </div>
  );
}
