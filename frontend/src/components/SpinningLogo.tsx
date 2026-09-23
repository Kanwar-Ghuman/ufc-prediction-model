"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";

export function SpinningLogo() {
  const video = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  const [failed, setFailed] = useState(false);

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
  }, []);

  return <div className="octagon-brand">
    <Link href="/" className="octagon-mark">
      <span className="octagon-logo">
        <video
          ref={video}
          muted loop playsInline preload="none"
          poster="/motion/octagon-logo.jpg"
          aria-hidden="true"
          onPlay={() => setPlaying(true)}
          onPause={() => setPlaying(false)}
          onError={() => setFailed(true)}
        >
          <source src="/motion/octagon-logo.mp4" type="video/mp4" onError={() => setFailed(true)} />
        </video>
      </span>
      <span className="brand-name">Ictus<span aria-hidden="true">.</span></span>
    </Link>
    {!failed && <button
      type="button"
      className="logo-motion-toggle"
      aria-label={playing ? "Pause logo rotation" : "Play logo rotation"}
      title={playing ? "Pause logo rotation" : "Play logo rotation"}
      onClick={() => {
        if (playing) video.current?.pause();
        else void video.current?.play().catch(() => setPlaying(false));
      }}
    ><span aria-hidden="true">{playing ? "Ⅱ" : "▷"}</span></button>}
  </div>;
}
