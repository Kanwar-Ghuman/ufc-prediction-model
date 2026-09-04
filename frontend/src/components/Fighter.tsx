import { flagEmoji, portraitUrl } from "@/lib/api";
import type { FighterMedia } from "@/lib/api";

type Side = "left" | "right";

function Monogram({ name }: { name: string }) {
  const initials = name
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0] ?? "")
    .join("");
  return (
    <div className="flex h-full w-full items-center justify-center bg-linear-to-b from-line to-shell">
      <span className="display text-3xl text-mist sm:text-4xl">{initials}</span>
    </div>
  );
}

export function Portrait({
  media,
  name,
  side,
}: {
  media: FighterMedia;
  name: string;
  side: Side;
}) {
  const src = portraitUrl(media.portrait);
  return (
    <div className="h-20 w-14 shrink-0 overflow-hidden sm:h-40 sm:w-36">
      {src ? (
        // Mirror the right-hand fighter so the pair face each other, the way
        // a broadcast card frames them. Only the photo flips — a mirrored
        // monogram is just backwards letters.
        //
        // Plain <img>, not next/image: these are served by the model API on
        // another origin, already cropped to the size they render at, and
        // allow-listing a localhost port in next.config would be the only
        // thing the optimizer bought us.
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={src}
          alt={`${name}`}
          className={`portrait h-full w-full ${
            side === "right" ? "-scale-x-100" : ""
          }`}
          loading="lazy"
        />
      ) : (
        <Monogram name={name} />
      )}
    </div>
  );
}

export function Nameplate({
  media,
  name,
  side,
  winner,
}: {
  media: FighterMedia;
  name: string;
  side: Side;
  /** Model's pick — the red rule under the name, as broadcast graphics do. */
  winner: boolean;
}) {
  const flag = flagEmoji(media.country_code);
  const align = side === "left" ? "items-start text-left" : "items-end text-right";
  return (
    <div className={`flex min-w-0 flex-col gap-1 ${align}`}>
      {media.rank && (
        <span className="label text-[11px] text-ash">#{media.rank}</span>
      )}
      <h3
        className={`display w-full min-w-0 text-sm leading-tight wrap-break-word sm:text-2xl ${
          winner ? "text-ink" : "text-ash"
        }`}
      >
        {name}
      </h3>
      {winner && <span className="h-0.5 w-10 bg-blood" />}
      {media.nickname && (
        <span className="truncate text-xs text-mist italic">
          &ldquo;{media.nickname}&rdquo;
        </span>
      )}
      <div
        className={`flex flex-wrap items-center gap-x-2 text-xs text-ash ${
          side === "right" ? "justify-end" : ""
        }`}
      >
        {flag && (
          <span title={media.country ?? undefined} aria-hidden>
            {flag}
          </span>
        )}
        {media.country && <span className="hidden sm:inline">{media.country}</span>}
        {media.record && <span className="font-mono">{media.record}</span>}
      </div>
    </div>
  );
}
