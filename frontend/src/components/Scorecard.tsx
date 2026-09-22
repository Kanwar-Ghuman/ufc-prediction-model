import { num, pct } from "@/lib/api";
import type { Scorecard } from "@/lib/api";
import { Badge, Cell, Panel, Row, Stat, Table } from "@/components/ui";

export function ScorecardPanel({ scorecard }: { scorecard: Scorecard }) {
  const a = scorecard.aggregates;
  return (
    <Panel
      title="How it went"
      subtitle="Graded against the probabilities published before the card."
    >
      <dl className="grid grid-cols-2 gap-6 sm:grid-cols-4">
        <Stat
          label="Winners"
          value={`${a.winners_correct}/${a.n}`}
          hint={`${pct(a.accuracy)} · coin flip ${(a.n / 2).toFixed(1)}`}
        />
        <Stat
          label="Log loss"
          value={num(a.log_loss)}
          hint="coin flip 0.6931"
        />
        <Stat
          label="Method"
          value={`${a.method_correct}/${a.n}`}
          hint="KO, submission, decision"
        />
        <Stat
          label="Round"
          value={`${a.round_correct}/${a.n_finishes}`}
          hint="of finishes"
        />
      </dl>

      <div className="mt-8">
        <Table head={["Fight", "Pick", "Result", "Winner", "Method", "Round"]}>
          {scorecard.fights.map((f) => (
            <Row key={`${f.f1}-${f.f2}`}>
              <Cell>
                {f.f1} vs. {f.f2}
              </Cell>
              <Cell>
                {f.pick}{" "}
                <span className="num text-xs text-ash">
                  {pct(f.confidence)}
                </span>
                {!f.called && (
                  <span className="ml-1">
                    <Badge tone="muted">no call</Badge>
                  </span>
                )}
              </Cell>
              <Cell muted>
                {f.winner}
                {f.method && !f.method.endsWith("DEC")
                  ? `, ${f.method} R${f.end_round}`
                  : `, ${f.method}`}
              </Cell>
              <Cell>
                <Badge tone={f.correct ? "good" : "bad"}>
                  {f.correct ? "hit" : "miss"}
                </Badge>
              </Cell>
              <Cell>
                <Badge tone={f.method_correct ? "good" : "neutral"}>
                  {f.method_correct ? "hit" : `said ${f.method_called}`}
                </Badge>
              </Cell>
              <Cell>
                {f.modal_round === null ? (
                  <span className="text-mist">—</span>
                ) : (
                  <Badge tone={f.round_correct ? "good" : "neutral"}>
                    {f.round_correct ? "hit" : `said R${f.modal_round}`}
                  </Badge>
                )}
              </Cell>
            </Row>
          ))}
          {scorecard.skipped.map((s) => (
            <Row key={`${s.f1}-${s.f2}`}>
              <Cell muted>
                {s.f1} vs. {s.f2}
              </Cell>
              <Cell muted>—</Cell>
              <Cell muted>{s.status}</Cell>
              <Cell muted>—</Cell>
              <Cell muted>—</Cell>
              <Cell muted>—</Cell>
            </Row>
          ))}
        </Table>
      </div>

      {a.mean_p_actual !== null && a.mean_p_actual_base !== null && (
        <p className="mt-5 text-sm text-ash">
          On the exact way each fight ended, the model averaged{" "}
          <span className="num text-ink">{num(a.mean_p_actual, 3)}</span> against
          a base rate of{" "}
          <span className="num">{num(a.mean_p_actual_base, 3)}</span>.
        </p>
      )}
    </Panel>
  );
}
