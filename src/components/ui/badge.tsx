import { cn } from "@/lib/cn";

export function Badge({
  className,
  tone = "muted",
  ...props
}: React.ComponentProps<"span"> & {
  tone?: "muted" | "accent" | "partner" | "associate" | "critic" | "ok" | "warn" | "danger";
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
