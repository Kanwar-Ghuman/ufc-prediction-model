"use client";

import { useEffect, useRef, useState } from "react";

export function FightMotion() {
  const video = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  useEffect(() => {
    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    const sync = () => {
      if (preference.matches) video.current?.pause();
      else void video.current?.play().catch(() => setPlaying(false));
    };
    sync();
    preference.addEventListener("change", sync);
    return () => preference.removeEventListener("change", sync);
  }, []);
  return <div className="event-art">
    <video ref={video} muted loop playsInline preload="none" poster="/motion/sparring-poster.jpg" aria-label="Stylized boxing study: two figures exchange jabs and slip punches" onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)}>
      <source src="/motion/sparring-study.mp4" type="video/mp4" />
    </video>
    <span className="motion-caption">Movement study 01 / Stand-up</span>
    <button className="motion-control" type="button" aria-label={playing ? "Pause fight animation" : "Play fight animation"} onClick={() => {
      if (playing) video.current?.pause();
      else void video.current?.play().catch(() => setPlaying(false));
    }}>{playing ? "Pause Ⅱ" : "Play ▷"}</button>
  </div>;
}
