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
        <header className="chrome chrome-edge sticky top-0 z-10">
          <div className="mx-auto flex max-w-4xl flex-wrap items-center gap-x-7 gap-y-2 px-5 py-3.5 sm:px-8">
            <Link href="/" className="display display-title text-xl">
              Octagon
            </Link>
            <nav className="flex gap-6 text-sm text-ash">
              {NAV.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="pressable hover:text-ink"
                >
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>

        <main className="mx-auto w-full max-w-4xl flex-1 px-5 py-8 sm:px-8 sm:py-12">
          {children}
        </main>

        <footer className="mt-16 border-t border-line/70">
          <div className="mx-auto flex max-w-4xl flex-wrap justify-between gap-2 px-5 py-6 text-xs text-mist sm:px-8">
            <p>Educational project. Not betting advice.</p>
            <p>
              Portraits and records from{" "}
              <a
                className="underline underline-offset-2 hover:text-ash"
                href="https://www.ufc.com/athletes"
                rel="noreferrer noopener"
                target="_blank"
              >
                ufc.com
              </a>
              .
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
