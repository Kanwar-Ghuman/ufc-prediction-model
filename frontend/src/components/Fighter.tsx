"use client";

import { useState } from "react";
import { portraitUrl } from "@/lib/api";
import type { FighterMedia } from "@/lib/api";

type Side = "left" | "right";

export function Portrait({ media, name }: { media: FighterMedia; name: string; side: Side }) {
  const src = portraitUrl(media.portrait);
  const [failedSource, setFailedSource] = useState<string | null>(null);
  const initials = name.split(/\s+/).map(part => part[0]).slice(0, 2).join("");
  return <div className="portrait-frame">
    {src && failedSource !== src ? (
      // Cached photographs already have the required resolution.
      // eslint-disable-next-line @next/next/no-img-element
      <img src={src} alt={name} className="portrait" loading="lazy" onError={() => setFailedSource(src)} />
    ) : <div className="flex h-full items-center justify-center" role="img" aria-label={`${name}, portrait unavailable`}><span className="text-3xl font-light tracking-tight text-mist">{initials}</span></div>}
  </div>;
}

export function Nameplate({ media, name }: { media: FighterMedia; name: string; side: Side; winner: boolean }) {
  return <div>
    <h3 className="fighter-name">{name}</h3>
    <p className="fighter-nickname">{media.nickname ? `“${media.nickname}”` : "\u00a0"}</p>
    <p className="fighter-record">{media.record ?? "Record unavailable"}{media.rank ? ` · #${media.rank}` : ""}</p>
  </div>;
}
