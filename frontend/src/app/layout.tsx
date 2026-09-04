import type { Metadata } from "next";
import Link from "next/link";
import { Geist_Mono, Inter, Oswald } from "next/font/google";
import "./globals.css";

const oswald = Oswald({ variable: "--font-oswald", subsets: ["latin"] });
const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Octagon",
  description: "Calibrated UFC win, method, and round probabilities.",
};

const NAV = [
  { href: "/", label: "Next card" },
  { href: "/cards", label: "All cards" },
  { href: "/results", label: "Results" },
];

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${oswald.variable} ${inter.variable} ${geistMono.variable} h-full`}
    >
      <body className="flex min-h-full flex-col">
        <header className="sticky top-0 z-10 border-b border-line bg-paper">
          <div className="mx-auto flex max-w-5xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3 sm:px-8">
            <Link href="/" className="flex items-baseline gap-2">
              <span className="display text-xl">Octagon</span>
            </Link>
            <nav className="label flex gap-5 text-[11px] text-ash">
              {NAV.map((item) => (
                <Link key={item.href} href={item.href} className="hover:text-ink">
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>

        <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-6 sm:px-8 sm:py-10">
          {children}
        </main>

        <footer className="mt-8 border-t border-line bg-paper">
          <div className="mx-auto max-w-5xl space-y-1 px-4 py-5 text-xs text-mist sm:px-8">
            <p>
              Educational project. Not betting advice — the backtest shows this
              model does not beat the market.
            </p>
            <p>
              Fighter portraits, records and rankings from{" "}
              <a
                className="underline underline-offset-2 hover:text-ash"
                href="https://www.ufc.com/athletes"
                rel="noreferrer noopener"
                target="_blank"
              >
                ufc.com
              </a>
              ; flags and biographies from Wikipedia and Wikidata. Cached
              locally by <code className="font-mono">octagon fetch-media</code>.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
