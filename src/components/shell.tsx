import { Link, useRouterState } from "@tanstack/react-router";
import {
  BookOpen,
  Briefcase,
  FileSignature,
  Gavel,
  LayoutGrid,
  Menu,
  Mic,
  Scale,
  Search,
  Terminal,
  Users,
  X,
} from "lucide-react";
import { useEffect, useState, type ReactNode } from "react";
import { Toaster } from "sonner";
import { cn } from "@/lib/cn";
import { useCounsel } from "@/lib/store";

const NAV = [
  { to: "/", label: "Deck", icon: LayoutGrid },
  { to: "/draft", label: "Draft", icon: FileSignature },
  { to: "/research", label: "Research", icon: Search },
  { to: "/triad", label: "Triad", icon: Users },
  { to: "/matters", label: "Matters", icon: Briefcase },
  { to: "/intake", label: "Intake", icon: Gavel },
  { to: "/playbook", label: "Playbook", icon: BookOpen },
  { to: "/stack", label: "Stack", icon: Terminal },
] as const;

const PRIMARY = NAV.slice(0, 4);

export function Shell({ children }: { children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const seedIfEmpty = useCounsel((s) => s.seedIfEmpty);
  const voiceOn = useCounsel((s) => s.voiceOn);
  const setVoiceOn = useCounsel((s) => s.setVoiceOn);
  const active = useCounsel((s) => s.matters.find((m) => m.id === s.activeMatterId));
  const [more, setMore] = useState(false);

  useEffect(() => {
    seedIfEmpty();
  }, [seedIfEmpty]);

  useEffect(() => {
    setMore(false);
  }, [pathname]);

  return (
    <div className="min-h-dvh bg-bg text-fg">
      <Toaster theme="dark" position="bottom-right" />
      <div className="flex min-h-dvh">
        <aside className="no-print sticky top-0 hidden h-dvh w-56 shrink-0 flex-col border-r border-border bg-surface md:flex">
          <Link to="/" className="flex items-center gap-3 px-4 py-5">
            <span className="flex size-9 items-center justify-center rounded-md border border-border bg-elevated">
              <Scale className="size-4 text-accent" />
            </span>
            <span className="min-w-0">
              <span className="block font-display text-lg leading-tight tracking-tight">
                NextLaw<span className="text-muted">607</span>
              </span>
              <span className="block font-mono text-[10px] uppercase tracking-[0.18em] text-subtle">
                N.Y. General Counsel
              </span>
            </span>
          </Link>
          <nav className="flex flex-1 flex-col gap-0.5 px-2">
            {NAV.map((item) => {
              const on =
                item.to === "/"
                  ? pathname === "/"
                  : pathname === item.to || pathname.startsWith(`${item.to}/`);
              const Icon = item.icon;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={cn(
                    "flex h-11 items-center gap-3 rounded-md px-3 text-sm transition-colors duration-[var(--motion-quick)]",
                    on ? "bg-elevated text-fg" : "text-muted hover:bg-elevated hover:text-fg",
                  )}
                >
                  <Icon className="size-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <div className="border-t border-border px-4 py-4">
            <button
              type="button"
              onClick={() => setVoiceOn(!voiceOn)}
              className={cn(
                "flex h-11 w-full items-center justify-center gap-2 rounded-md border text-sm",
                voiceOn
                  ? "border-associate bg-elevated text-associate"
                  : "border-border text-muted",
              )}
            >
              <Mic className="size-4" />
              {voiceOn ? "Voice armed" : "Voice idle"}
            </button>
            {active ? (
              <p className="mt-3 truncate font-mono text-[10px] uppercase tracking-wider text-subtle">
                {active.caption}
              </p>
            ) : null}
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <header className="no-print flex h-14 items-center justify-between gap-3 border-b border-border px-4 md:px-6">
            <div className="flex min-w-0 items-center gap-2 md:hidden">
              <Scale className="size-4 shrink-0 text-accent" />
              <span className="truncate font-display text-base">NextLaw607</span>
            </div>
            <p className="hidden truncate font-mono text-[11px] uppercase tracking-[0.16em] text-subtle md:block">
              Sovereign counsel terminal · CPL / PL / DRL 70·240 / FCA Art. 6 / GOL
            </p>
            <p className="truncate font-mono text-[11px] text-subtle">
              {active ? active.county + " County" : "No matter"}
            </p>
          </header>
          <main className="flex-1 px-4 py-6 pb-24 md:px-8 md:py-8 md:pb-8">{children}</main>
        </div>
      </div>

      {more ? (
        <div className="no-print fixed inset-0 z-30 md:hidden">
          <button
            type="button"
            aria-label="Close menu"
            className="absolute inset-0 bg-bg/70"
            onClick={() => setMore(false)}
          />
          <div className="absolute inset-x-0 bottom-0 rounded-t-xl border border-border bg-surface p-4 pb-[calc(env(safe-area-inset-bottom)+4.5rem)]">
            <div className="mb-3 flex items-center justify-between">
              <p className="font-display text-lg">More</p>
              <button type="button" className="size-11" onClick={() => setMore(false)} aria-label="Close">
                <X className="size-4" />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {NAV.slice(4).map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.to}
                    to={item.to}
                    className="flex h-14 items-center gap-3 rounded-md border border-border bg-elevated px-3 text-sm"
                  >
                    <Icon className="size-4" />
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>
        </div>
      ) : null}

      <nav className="no-print fixed inset-x-0 bottom-0 z-20 grid grid-cols-5 border-t border-border bg-surface pb-[env(safe-area-inset-bottom)] md:hidden">
        {PRIMARY.map((item) => {
          const on =
            item.to === "/"
              ? pathname === "/"
              : pathname === item.to || pathname.startsWith(`${item.to}/`);
          const Icon = item.icon;
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "flex min-h-14 flex-col items-center justify-center gap-1 text-[10px] uppercase tracking-wider",
                on ? "text-fg" : "text-subtle",
              )}
            >
              <Icon className="size-4" />
              {item.label}
            </Link>
          );
        })}
        <button
          type="button"
          onClick={() => setMore((v) => !v)}
          className={cn(
            "flex min-h-14 flex-col items-center justify-center gap-1 text-[10px] uppercase tracking-wider",
            more ? "text-fg" : "text-subtle",
          )}
        >
          <Menu className="size-4" />
          More
        </button>
      </nav>
    </div>
  );
}
