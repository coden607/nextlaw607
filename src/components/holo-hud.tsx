import { Cpu, Sparkles } from "lucide-react";
import { cn } from "@/lib/cn";
import { useCounsel } from "@/lib/store";

export function HoloOverlay() {
  const holoMode = useCounsel((s) => s.holoMode);

  if (!holoMode) return null;

  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 z-40 overflow-hidden select-none"
    >
      {/* Ambient Top Hologram Emitter Cone */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[720px] h-[320px] bg-[radial-gradient(ellipse_60%_40%_at_50%_0%,rgba(0,240,255,0.12),rgba(168,85,247,0.04)_60%,transparent_100%)] opacity-80" />

      {/* Holographic Fine Scanline Grid Overlay */}
      <div className="absolute inset-0 holo-scanlines opacity-50" />

      {/* Holographic Laser Sweep Bar */}
      <div className="holo-sweep-bar opacity-75" />

      {/* Subtle Corner HUD Telemetry Indicators */}
      <div className="absolute top-2 right-4 hidden md:flex items-center gap-3 font-mono text-[9px] uppercase tracking-[0.2em] text-cyan-400/60">
        <span className="flex items-center gap-1.5">
          <span className="size-1.5 rounded-full bg-cyan-400 shadow-[0_0_8px_#00f0ff] animate-pulse" />
          HOLO·HUD 480nm
        </span>
        <span className="text-cyan-400/30">|</span>
        <span className="text-cyan-400/40">FL-RECAP LINKED</span>
      </div>
    </div>
  );
}

export function HoloToggle({ className }: { className?: string }) {
  const holoMode = useCounsel((s) => s.holoMode);
  const setHoloMode = useCounsel((s) => s.setHoloMode);

  return (
    <button
      type="button"
      onClick={() => setHoloMode(!holoMode)}
      title="Toggle Hologram Special Effects HUD"
      className={cn(
        "flex items-center gap-2 rounded-md px-2.5 py-1.5 font-mono text-xs uppercase tracking-wider transition-all duration-200 border",
        holoMode
          ? "border-cyan-400/50 bg-cyan-950/30 text-cyan-300 shadow-[0_0_12px_rgba(0,240,255,0.25)] hover:border-cyan-300 hover:bg-cyan-950/50"
          : "border-border text-muted hover:border-border/80 hover:text-fg",
        className,
      )}
    >
      <Sparkles
        className={cn(
          "size-3.5 transition-transform duration-300",
          holoMode ? "text-cyan-300 scale-110 drop-shadow-[0_0_6px_#00f0ff]" : "text-muted",
        )}
      />
      <span>HOLO {holoMode ? "ON" : "OFF"}</span>
      <span
        className={cn(
          "size-1.5 rounded-full transition-colors",
          holoMode
            ? "bg-cyan-400 shadow-[0_0_6px_#00f0ff] animate-ping"
            : "bg-muted/40",
        )}
      />
    </button>
  );
}
