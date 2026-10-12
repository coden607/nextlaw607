import { cn } from "@/lib/cn";

export function Badge({
  className,
  tone = "muted",
  ...props
}: React.ComponentProps<"span"> & {
  tone?: "muted" | "accent" | "partner" | "associate" | "critic" | "ok" | "warn" | "danger" | "holo";
}) {
  const tones: Record<string, string> = {
    muted: "border-border text-muted",
    accent: "border-accent text-accent",
    partner: "border-partner text-partner",
    associate: "border-associate text-associate",
    critic: "border-critic text-critic",
    ok: "border-ok text-ok",
    warn: "border-warn text-warn",
    danger: "border-danger text-danger",
    holo: "border-cyan-400/50 bg-cyan-950/30 text-cyan-300 shadow-[0_0_12px_rgba(0,240,255,0.25)]",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2 py-0.5 font-mono text-[10px] uppercase tracking-[0.14em]",
        tones[tone],
        className,
      )}
      {...props}
    />
  );
}
