import type { Metadata } from "next";
import { Navigation } from "@/components/Navigation";
import { SpinningLogo } from "@/components/SpinningLogo";
import "./globals.css";

export const metadata: Metadata = {
  title: "Octagon — Fight by fight",
  description: "Independent UFC analysis. Fighter matchups, calibrated predictions, and the record behind them.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" className="h-full">
    <body className="flex min-h-full flex-col">
      <a href="#main" className="sr-only focus:not-sr-only focus:p-3">Skip to content</a>
      <header className="sticky top-0 z-10 border-b border-line bg-paper">
        <div className="site-width flex items-center justify-between gap-4">
          <SpinningLogo />
          <Navigation />
        </div>
      </header>
      <main id="main" className="site-width flex-1 py-8 sm:py-12">{children}</main>
      <footer className="mt-10 border-t border-line">
        <div className="site-width flex flex-wrap justify-between gap-5 py-7 text-[11px] leading-relaxed text-mist">
          <div><p className="mb-2 font-semibold text-ink">Octagon / Independent fight analysis</p><p>Educational project. Not betting advice. The model does not beat the market.</p></div>
          <p>Fighter imagery &amp; records: <a className="underline underline-offset-2" href="https://www.ufc.com/athletes" target="_blank" rel="noreferrer noopener">UFC</a>.<br />Additional biographies: Wikipedia &amp; Wikidata.</p>
        </div>
      </footer>
    </body>
  </html>;
}
