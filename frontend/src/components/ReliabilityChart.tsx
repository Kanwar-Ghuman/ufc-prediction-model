import type { Calibration } from "@/lib/api";

const SIZE = 260;
const PAD = 34;

const SERIES_COLORS = ["#f4f4f5", "#e62629", "#4da3e8", "#d9a13d"];

export function ReliabilityChart({ series }: { series: Calibration["series"] }) {
  const x = (v: number) => PAD + v * (SIZE - PAD * 2);
  const y = (v: number) => SIZE - PAD - v * (SIZE - PAD * 2);

  return (
    <div className="flex flex-wrap items-start gap-6">
      <svg
        viewBox={`0 0 ${SIZE} ${SIZE}`}
        className="h-64 w-64 shrink-0"
        role="img"
        aria-label="Reliability diagram: predicted probability against observed win rate"
      >
        <rect
          x={PAD}
          y={PAD}
          width={SIZE - PAD * 2}
          height={SIZE - PAD * 2}
          fill="none"
          stroke="var(--color-line)"
        />
        <line
          x1={x(0)}
          y1={y(0)}
          x2={x(1)}
          y2={y(1)}
          strokeDasharray="4 3"
          stroke="var(--color-rail)"
        />
        {series.map((s, i) => (
          <polyline
            key={s.key}
            points={s.bins
              .map((b) => `${x(b.predicted)},${y(b.observed)}`)
              .join(" ")}
            fill="none"
            stroke={SERIES_COLORS[i % SERIES_COLORS.length]}
            strokeWidth={1.75}
          />
        ))}
        {[0, 0.5, 1].map((t) => (
          <text
            key={`x${t}`}
            x={x(t)}
            y={SIZE - PAD + 14}
            textAnchor="middle"
            fill="var(--color-mist)"
            className="text-[9px]"
          >
            {t.toFixed(1)}
          </text>
        ))}
        {[0, 0.5, 1].map((t) => (
          <text
            key={`y${t}`}
            x={PAD - 6}
            y={y(t) + 3}
            textAnchor="end"
            fill="var(--color-mist)"
            className="text-[9px]"
          >
            {t.toFixed(1)}
          </text>
        ))}
        <text
          x={SIZE / 2}
          y={SIZE - 4}
          textAnchor="middle"
          fill="var(--color-mist)"
          className="text-[9px]"
        >
          predicted
        </text>
        <text
          x={10}
          y={SIZE / 2}
          textAnchor="middle"
          transform={`rotate(-90 10 ${SIZE / 2})`}
          fill="var(--color-mist)"
          className="text-[9px]"
        >
          observed
        </text>
      </svg>

      <ul className="space-y-2 text-sm">
        {series.map((s, i) => (
          <li key={s.key} className="flex items-center gap-2">
            <span
              className="inline-block h-0.5 w-5"
              style={{ background: SERIES_COLORS[i % SERIES_COLORS.length] }}
            />
            <span className="text-ink">{s.model}</span>
            <span className="font-mono text-xs text-ash">
              ECE {s.ece.toFixed(3)}
            </span>
          </li>
        ))}
        <li className="pt-1 text-xs text-mist">
          Dashed line is perfect calibration. Lower ECE is better.
        </li>
      </ul>
    </div>
  );
}
