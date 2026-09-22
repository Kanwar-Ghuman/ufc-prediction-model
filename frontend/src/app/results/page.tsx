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
      "Used to choose between models. Odds exist here, so it is the only fair model-against-market comparison.",
  },
  {
    split: "test",
    title: "Test (2024 onward)",
    subtitle: "Touched once, at the end. No odds coverage, so no market row.",
  },
];

export default function ResultsPage() {
  return (
    <div className="space-y-10">
      <div>
        <h1 className="display display-hero text-4xl sm:text-5xl">Results</h1>
        <p className="mt-3 max-w-lg text-sm text-ash">
          Every fight is scored by a model trained only on fights before it. A
          coin flip scores 0.6931 log loss — that is the bar.
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
              <div className="mt-8">
                <h3 className="display display-title text-base">
                  Abstain trade-off
                </h3>
                <p className="mt-1.5 mb-4 max-w-xl text-sm text-ash">
                  A wider no-call band answers fewer fights and gets more of
                  them right. Shipped band{" "}
                  <span className="num text-ink">
                    {metrics.data.abstain.shipped_band.join("–")}
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
