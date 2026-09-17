const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; kind: "offline" | "missing" | "error"; message: string };

export async function api<T>(path: string): Promise<ApiResult<T>> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  } catch {
    return {
      ok: false,
      kind: "offline",
      message: `Cannot reach the API at ${API_BASE}. Start it with \`cd model && uv run python -m octagon serve\`.`,
    };
  }

  if (!response.ok) {
    const detail = await response
      .json()
      .then((body: { detail?: string }) => body.detail)
      .catch(() => null);
    return {
      ok: false,
      kind: response.status === 404 ? "missing" : "error",
      message: detail ?? `API returned ${response.status}.`,
    };
  }

  return { ok: true, data: (await response.json()) as T };
}

export type Overview = {
  name: string;
  summary: string;
  disclaimer: string;
  updated_at: string | null;
  dataset:
    | { available: false }
    | {
        available: true;
        n_fights: number;
        first_fight: string;
        last_fight: string;
        n_weight_classes: number;
      };
  splits: { train: string; validation: string; test: string };
  abstain_band: [number, number];
  trained: boolean;
  model: {
    n_seeds: number;
    include_raw: boolean;
    weight_lr: number;
    weight_round_base: number;
    n_features: number;
    tuning_trials: number;
    cv_log_loss: number;
    seed: number;
  } | null;
};

type ModelMetrics = {
  key: string;
  model: string;
  note: string;
  priced_only: boolean;
  n: number;
  accuracy: number;
  log_loss: number;
  brier: number;
  roc_auc: number;
  ece: number;
};

type AbstainPoint = {
  band: [number, number];
  coverage: number;
  accuracy: number;
  n: number;
};

export type SplitMetrics = {
  available: true;
  split: string;
  n_fights: number;
  date_range: [string, string];
  models: ModelMetrics[];
  abstain: { shipped_band: [number, number]; points: AbstainPoint[] } | null;
};

export type Calibration = {
  available: true;
  split: string;
  series: {
    key: string;
    model: string;
    ece: number;
    bins: { predicted: number; observed: number; n: number }[];
  }[];
};

export type CardSummary = {
  slug: string;
  event: string;
  date: string;
  n_bouts: number;
};

/** What `octagon fetch-media` found for a fighter: ufc.com, then Wikipedia. */
export type FighterMedia = {
  name: string;
  /** API path, not an absolute URL — portraits are served by the model API. */
  portrait: string | null;
  nickname: string | null;
  record: string | null;
  rank: string | null;
  division: string | null;
  country: string | null;
  country_code: string | null;
  profile: string | null;
  wiki_page: string | null;
  description: string | null;
};

/** One SHAP contribution to a pick, in log-odds. */
type Driver = { feature: string; value: number };

/** Day-before context for one corner of a bout. */
type BoutFighterContext = {
  styles?: string[];
  pro_record?: { wins: number; losses: number; draws?: number; win_pct: number } | null;
  circumstances?: {
    short_notice?: boolean;
    late_replacement?: boolean;
    opponent_changed?: boolean;
    notes?: string[];
  };
  sentiment?: number | null;
  summary?: string | null;
  headlines?: { title: string; link: string }[];
};

export type Bout = {
  f1: string;
  f2: string;
  f1_media: FighterMedia;
  f2_media: FighterMedia;
  weight_class: string | null;
  /** Broadcast segment: "Main card", "Preliminary card", or null if unknown. */
  section: string | null;
  scheduled_rounds: number;
  p_f1_wins: number;
  /** Skill/research model only — null on cards frozen before this field. */
  p_skill?: number | null;
  /** Vig-free market P(f1) — null when the bout was unpriced. */
  p_market?: number | null;
  pick: string;
  confidence: number;
  called: boolean;
  /** Method is selected by marginal probability; finish round is conditional on it. */
  top_outcome: {
    label: string;
    /** Joint P(picked fighter wins by this method in this exact round). */
    probability: number;
    method: "KO/TKO" | "SUB" | "DEC";
    round: number | null;
    /** Joint P(picked fighter wins by this method), marginalized over rounds. */
    method_probability: number;
    /** P(round | picked fighter wins by method), null for a decision. */
    round_probability: number | null;
  };
  /** Word-for-word prediction, e.g. "Medic by KO/TKO in round 1". */
  statement: string | null;
  /** UFC fights each man had before this one; 0 is a debut, null unknown. */
  f1_ufc_fights: number | null;
  f2_ufc_fights: number | null;
  /** Day-before scrape: circumstances, debut record, styles, headlines. */
  context?: {
    adjustments?: string[];
    research?: string[];
    f1?: BoutFighterContext;
    f2?: BoutFighterContext;
  };
  drivers: Driver[];
  methods: {
    f1_ko: number;
    f1_sub: number;
    f1_dec: number;
    f2_ko: number;
    f2_sub: number;
    f2_dec: number;
  };
  by_round: {
    round: number;
    f1_ko: number;
    f1_sub: number;
    f2_ko: number;
    f2_sub: number;
  }[];
  p_decision: number;
};

/** The model's most confident call on a card, spelled out word for word. */
export type Headline = {
  pick: string;
  opponent: string;
  weight_class: string | null;
  confidence: number;
  /** "by KO/TKO in round 2" / "by decision" */
  outcome: string;
  outcome_probability: number;
  statement: string;
};

export type CardDetail = {
  slug: string;
  event: string;
  date: string;
  /** The card hasn't happened yet — show predictions, not a grade. */
  upcoming: boolean;
  /** When `octagon predict` froze these numbers. */
  predicted_at: string;
  headline: Headline | null;
  bouts: Bout[];
};

/** `/api/next-card`: the card the homepage leads with, graded if it's over. */
export type NextCard = CardDetail & { scorecard: Scorecard | null };

export type GradedFight = {
  f1: string;
  f2: string;
  pick: string;
  confidence: number;
  called: boolean;
  winner: string;
  method: string | null;
  end_round: number | null;
  correct: boolean;
  method_called: string;
  method_correct: boolean;
  modal_round: number | null;
  round_correct: boolean | null;
};

export type Scorecard = {
  date: string;
  event: string;
  fights: GradedFight[];
  skipped: { f1: string; f2: string; status: string }[];
  aggregates: {
    n: number;
    winners_correct: number;
    accuracy: number;
    n_called: number;
    called_correct: number;
    called_accuracy: number | null;
    log_loss: number;
    brier: number;
    method_correct: number;
    round_correct: number;
    n_finishes: number;
    mean_p_actual: number | null;
    mean_p_actual_base: number | null;
  };
};

export const pct = (value: number, digits = 0) =>
  `${(value * 100).toFixed(digits)}%`;

export const num = (value: number, digits = 4) => value.toFixed(digits);

/** Portraits live on the model API, which is a different origin in dev. */
export const portraitUrl = (path: string | null) =>
  path ? `${API_BASE}${path}` : null;

/**
 * "RS" -> 🇷🇸, "GB-WLS" -> 🏴󠁧󠁢󠁷󠁬󠁳󠁿. Country flags are the two letters offset into
 * the regional-indicator block; subdivision flags (the home nations, which
 * have no alpha-2 of their own and a lot of fighters) are a black flag
 * followed by the code as invisible tag characters. No image set either way.
 */
export const flagEmoji = (code: string | null) => {
  if (!code) return null;
  if (/^[A-Za-z]{2}$/.test(code)) {
    return String.fromCodePoint(
      ...[...code.toUpperCase()].map((c) => 0x1f1a5 + c.charCodeAt(0)),
    );
  }
  if (/^[A-Za-z]{2}-[A-Za-z0-9]{1,3}$/.test(code)) {
    const tags = [...code.toLowerCase().replace("-", "")].map(
      (c) => 0xe0000 + c.charCodeAt(0),
    );
    return String.fromCodePoint(0x1f3f4, ...tags, 0xe007f);
  }
  return null;
};

/**
 * Card dates are plain YYYY-MM-DD. Parsed as a Date they land on UTC
 * midnight, so anything west of Greenwich renders the day before unless the
 * formatting is pinned to UTC too.
 */
export const eventDate = (iso: string, opts?: Intl.DateTimeFormatOptions) =>
  new Date(`${iso}T00:00:00Z`).toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
    ...opts,
  });

/** A timestamp from the API, as "Jul 26, 9:14 PM" in the reader's zone. */
export const stamp = (iso: string | null) =>
  iso
    ? new Date(iso).toLocaleString("en-US", {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      })
    : null;
