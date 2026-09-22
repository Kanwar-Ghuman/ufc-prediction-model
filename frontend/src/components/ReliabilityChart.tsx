import type { Calibration } from "@/lib/api";

const SIZE = 260;
const PAD = 34;

/* Colour by role, not by position: the shipped model is the line the reader
   is here for, the market is the bar it is measured against, and the rest are
   working models that should recede. */
const SERIES_COLORS: Record<string, string> = {
  p_shipped: "#ef3b3e",
  p_market: "#f5f5f7",
  p_blend: "#d9a13d",
  p_lr: "#4da3e8",
  p_gbm_cal: "#32c26f",
};
const FALLBACK = "#a4a4ad";

const colorFor = (key: string) => SERIES_COLORS[key] ?? FALLBACK;

export function ReliabilityChart({ series }: { series: Calibration["series"] }) {
  const x = (v: number) => PAD + v * (SIZE - PAD * 2);
  const y = (v: number) => SIZE - PAD - v * (SIZE - PAD * 2);

  return (
    <div className="flex flex-wrap items-start gap-6">
      <svg
        viewBox={`0 0 ${SIZE} ${SIZE}`}
        className="h-72 w-72 shrink-0"
        role="img"
        aria-label="Reliability diagram: predicted probability against observed win rate"
      >
        <rect
          x={PAD}
          y={PAD}
          width={SIZE - PAD * 2}
          height={SIZE - PAD * 2}
          rx={6}
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
        {series.map((s) => (
          <polyline
            key={s.key}
            points={s.bins
              .map((b) => `${x(b.predicted)},${y(b.observed)}`)
              .join(" ")}
            fill="none"
            stroke={colorFor(s.key)}
            strokeWidth={s.key === "p_shipped" ? 2.25 : 1.5}
            strokeLinecap="round"
            strokeLinejoin="round"
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

      <ul className="space-y-2.5 text-sm">
        {series.map((s) => (
          <li key={s.key} className="flex items-center gap-2.5">
            <span
              className="inline-block h-0.5 w-5 rounded-full"
              style={{ background: colorFor(s.key) }}
            />
            <span className="text-ink">{s.model}</span>
            <span className="num text-xs text-ash">ECE {s.ece.toFixed(3)}</span>
          </li>
        ))}
        <li className="pt-1 text-xs text-mist">
          Dashed line is perfect calibration. Lower ECE is better.
        </li>
      </ul>
    </div>
  );
}
