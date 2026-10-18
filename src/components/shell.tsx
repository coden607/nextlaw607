import { Link, useRouterState } from "@tanstack/react-router";
import {
  BookOpen,
  Briefcase,
  FileSignature,
  FileText,
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
import { HoloOverlay, HoloToggle } from "@/components/holo-hud";
import { cn } from "@/lib/cn";
import { useCounsel } from "@/lib/store";

const NAV = [
  { to: "/", label: "Deck", icon: LayoutGrid },
  { to: "/draft", label: "Draft", icon: FileSignature },
  { to: "/drafts", label: "Drafts", icon: FileText },
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
  const holoMode = useCounsel((s) => s.holoMode);
  const active = useCounsel((s) => s.matters.find((m) => m.id === s.activeMatterId));
  const [more, setMore] = useState(false);

  useEffect(() => {
    seedIfEmpty();
  }, [seedIfEmpty]);

  useEffect(() => {
    setMore(false);
  }, [pathname]);

  return (
    <div className={cn("min-h-dvh bg-bg text-fg relative", holoMode && "holo-grid-mesh")}>
      <HoloOverlay />
      <Toaster theme="dark" position="bottom-right" />
      <div className="flex min-h-dvh relative z-10">
        <aside
          className={cn(
            "no-print sticky top-0 hidden h-dvh w-56 shrink-0 flex-col border-r border-border bg-surface md:flex relative",
            holoMode && "border-cyan-500/20 shadow-[1px_0_15px_rgba(0,240,255,0.05)]",
          )}
        >
          {holoMode ? <div className="holo-beam-top" /> : null}
          <Link to="/" className="flex items-center gap-3 px-4 py-5 group">
            <span
              className={cn(
                "flex size-9 items-center justify-center rounded-md border border-border bg-elevated transition-all duration-300",
                holoMode && "border-cyan-400/40 bg-cyan-950/20 shadow-[0_0_10px_rgba(0,240,255,0.25)] group-hover:shadow-[0_0_18px_rgba(0,240,255,0.45)]",
              )}
            >
              <Scale className={cn("size-4 text-accent transition-colors", holoMode && "text-cyan-300")} />
            </span>
            <span className="min-w-0">
              <span className={cn("block font-display text-lg leading-tight tracking-tight", holoMode && "holo-text")}>
                NextLaw<span className={holoMode ? "text-cyan-400/60" : "text-muted"}>607</span>
              </span>
              <span
                className={cn(
                  "block font-mono text-[10px] uppercase tracking-[0.18em] text-subtle",
                  holoMode && "text-cyan-400/60",
                )}
              >
                N.Y. Criminal Law
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
                  aria-current={on ? "page" : undefined}
                  className={cn(
                    "flex h-11 items-center gap-3 rounded-md px-3 text-sm transition-all duration-[var(--motion-quick)]",
                    on
                      ? holoMode
                        ? "border-l-2 border-cyan-400 bg-cyan-950/30 text-cyan-200 shadow-[0_0_12px_rgba(0,240,255,0.15)]"
                        : "bg-elevated text-fg"
                      : "text-muted hover:bg-elevated hover:text-fg",
                  )}
                >
                  <Icon className={cn("size-4", on && holoMode && "text-cyan-300 drop-shadow-[0_0_4px_#00f0ff]")} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <div className="border-t border-border px-4 py-4 space-y-2">
            <HoloToggle className="w-full justify-center" />
            <button
              type="button"
              onClick={() => setVoiceOn(!voiceOn)}
              className={cn(
                "flex h-11 w-full items-center justify-center gap-2 rounded-md border text-sm transition-colors",
                voiceOn
                  ? "border-associate bg-elevated text-associate"
                  : "border-border text-muted",
              )}
            >
              <Mic className="size-4" />
              {voiceOn ? "Voice armed" : "Voice idle"}
            </button>
            {active ? (
              <p className="pt-1 truncate font-mono text-[10px] uppercase tracking-wider text-subtle">
                {active.caption}
              </p>
            ) : null}
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <header
            className={cn(
              "no-print flex h-14 items-center justify-between gap-3 border-b border-border px-4 md:px-6 relative",
              holoMode && "border-cyan-500/20 bg-surface/80 backdrop-blur-sm",
            )}
          >
            {holoMode ? <div className="holo-beam-top" /> : null}
            <div className="flex min-w-0 items-center gap-2 md:hidden">
              <Scale className={cn("size-4 shrink-0 text-accent", holoMode && "text-cyan-300")} />
              <span className={cn("truncate font-display text-base", holoMode && "holo-text")}>NextLaw607</span>
            </div>
            <p
              className={cn(
                "hidden truncate font-mono text-[11px] uppercase tracking-[0.16em] text-subtle md:block",
                holoMode && "text-cyan-400/70",
              )}
            >
              NY criminal-law terminal · CPL · Penal Law · suppression · discovery · appeals
            </p>
            <div className="flex items-center gap-3">
              <HoloToggle className="md:hidden" />
              <p
                className={cn(
                  "truncate font-mono text-[11px] text-subtle px-2 py-0.5 rounded border border-transparent",
                  holoMode && "border-cyan-500/30 text-cyan-300/80 bg-cyan-950/20",
                )}
              >
                {active ? active.county + " County" : "No matter"}
              </p>
            </div>
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
                const on =
                  item.to === "/"
                    ? pathname === "/"
                    : pathname === item.to || pathname.startsWith(`${item.to}/`);
                const Icon = item.icon;
                return (
                  <Link
                    key={item.to}
                    to={item.to}
                    aria-current={on ? "page" : undefined}
                    className={cn(
                      "flex h-14 items-center gap-3 rounded-md border border-border bg-elevated px-3 text-sm",
                      on ? "text-fg" : "text-muted",
                    )}
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
              aria-current={on ? "page" : undefined}
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
