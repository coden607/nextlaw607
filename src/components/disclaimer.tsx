export function Disclaimer({ compact = false }: { compact?: boolean }) {
  if (compact) {
    return (
      <p className="text-[11px] leading-snug text-subtle">
        Not legal advice. Not a substitute for a licensed New York attorney. A
        human lawyer must review before execution or filing.
      </p>
    );
  }
  return (
    <aside className="rounded-lg border border-border bg-surface px-4 py-3 text-xs leading-normal text-muted">
      <p className="font-medium text-fg">Unauthorized practice notice</p>
      <p className="mt-1">
        NextLaw607 is a drafting and research terminal. It is not a law firm, does
        not form an attorney-client relationship, and does not appear in any
        court. Work product is a starting point. Binding effect depends on
        capacity, consideration, statutory formalities, and a human attorney's
        review under New York law. Citations are limited to the verified bank and
        live CourtListener hits — anything else is marked unverified.
      </p>
    </aside>
  );
}
