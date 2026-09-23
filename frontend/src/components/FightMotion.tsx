"use client";

import { useEffect, useRef, useState } from "react";

const CLIPS = {
  "van-pantoja": {
    video: "/motion/van-pantoja.mp4",
    poster: "/motion/van-pantoja-poster.jpg",
    caption: "Van vs. Pantoja / 3D illustration",
    description:
      "Photo-textured 3D interpretations of Joshua Van and Alexandre Pantoja exchanging punches and defensive slips. An illustrative sequence, not actual footage or an outcome prediction.",
  },
  study: {
    video: "/motion/sparring-study.mp4",
    poster: "/motion/sparring-poster.jpg",
    caption: "Movement study 01 / Stand-up",
    description: "Stylized boxing study: two figures exchange jabs and slip punches",
  },
} as const;

export function FightMotion({ matchup = "study" }: {
  matchup?: keyof typeof CLIPS;
}) {
  const video = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  const [failed, setFailed] = useState(false);
  const clip = CLIPS[matchup];

  useEffect(() => {
    const player = video.current;
    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    const sync = () => {
      if (preference.matches) player?.pause();
      else void player?.play().catch(() => setPlaying(false));
    };
    sync();
    preference.addEventListener("change", sync);
    return () => {
      preference.removeEventListener("change", sync);
      player?.pause();
    };
  }, [matchup]);

  const reportFailure = () => {
    setFailed(true);
    setPlaying(false);
  };

  return <div className="event-art">
    <video
      ref={video}
      key={clip.video}
      muted loop playsInline preload="none"
      poster={clip.poster}
      aria-label={clip.description}
      onPlay={() => setPlaying(true)}
      onPause={() => setPlaying(false)}
      onError={reportFailure}
    >
      <source src={clip.video} type="video/mp4" onError={reportFailure} />
    </video>
    <span className="motion-caption">{clip.caption}</span>
    {failed ? <span className="motion-control" role="status">Preview only</span> :
      <button
        className="motion-control"
        type="button"
        aria-label={playing ? "Pause fight animation" : "Play fight animation"}
        onClick={() => {
          if (playing) video.current?.pause();
          else void video.current?.play().catch(() => setPlaying(false));
        }}
      >{playing ? "Pause Ⅱ" : "Play ▷"}</button>
    }
  </div>;
}
