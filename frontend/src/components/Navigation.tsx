"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Navigation() {
  const pathname = usePathname();
  return <nav className="site-nav" aria-label="Main navigation">
    {[{ href: "/", label: "Next card" }, { href: "/cards", label: "All cards" }, { href: "/results", label: "Results" }].map(({ href, label }) =>
      <Link key={href} href={href} aria-current={(href === "/" ? pathname === "/" : pathname.startsWith(href)) ? "page" : undefined}>{label}</Link>
    )}
  </nav>;
}
