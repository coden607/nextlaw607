import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input, Label, Textarea } from "@/components/ui/input";
import { newMatter, useCounsel } from "@/lib/store";
import { PRACTICE_LABEL, type PracticeArea } from "@/lib/types";

export const Route = createFileRoute("/intake")({ component: Intake });

const AREAS = Object.keys(PRACTICE_LABEL) as PracticeArea[];

function Intake() {
  const navigate = useNavigate();
  const upsert = useCounsel((s) => s.upsertMatter);
  const [caption, setCaption] = useState("");
  const [practice, setPractice] = useState<PracticeArea>("contracts");
  const [county, setCounty] = useState("New York");
  const [partyA, setPartyA] = useState("");
  const [roleA, setRoleA] = useState("Client");
  const [partyB, setPartyB] = useState("");
  const [roleB, setRoleB] = useState("Counterparty");
  const [facts, setFacts] = useState("");
  const [objectives, setObjectives] = useState("");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!caption.trim() || !partyA.trim() || !partyB.trim()) {
      toast.error("Caption and both parties are required.");
      return;
    }
    const m = newMatter({
      caption: caption.trim(),
      practice,
      county: county.trim() || "New York",
      facts: facts.trim(),
      objectives: objectives.trim(),
      parties: [
        { role: roleA.trim() || "Party A", name: partyA.trim() },
        { role: roleB.trim() || "Party B", name: partyB.trim() },
      ],
    });
    upsert(m);
    toast.success("Matter opened.");
    void navigate({ to: "/matters" });
  }

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6 pb-20">
      <header>
        <Badge>Client intake</Badge>
        <h1 className="mt-3 font-display text-3xl tracking-tight">Open a matter</h1>
        <p className="mt-2 text-sm leading-normal text-muted">
          The triad will not draft until a county and two parties exist. Facts
          stay in this browser. This is not a retainer and does not create an
          attorney-client relationship.
        </p>
      </header>

      <form onSubmit={submit} className="flex flex-col gap-4 rounded-xl border border-border bg-surface p-5">
        <div>
          <Label htmlFor="caption">Caption</Label>
          <Input
            id="caption"
            className="mt-1"
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            placeholder="Avery v. Hale, or Northline LLC / contractor"
          />
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <Label htmlFor="practice">Practice</Label>
            <select
              id="practice"
              value={practice}
              onChange={(e) => setPractice(e.target.value as PracticeArea)}
              className="mt-1 h-11 w-full rounded-md border border-border bg-elevated px-3 text-sm text-fg"
            >
              {AREAS.map((a) => (
                <option key={a} value={a}>
                  {PRACTICE_LABEL[a]}
                </option>
              ))}
            </select>
          </div>
          <div>
            <Label htmlFor="county">County</Label>
            <Input
              id="county"
              className="mt-1"
              value={county}
              onChange={(e) => setCounty(e.target.value)}
              placeholder="Kings"
            />
          </div>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <Label htmlFor="roleA">Party A role</Label>
            <Input id="roleA" className="mt-1" value={roleA} onChange={(e) => setRoleA(e.target.value)} />
            <Label htmlFor="partyA" className="mt-3 block">
              Name
            </Label>
            <Input id="partyA" className="mt-1" value={partyA} onChange={(e) => setPartyA(e.target.value)} />
          </div>
          <div>
            <Label htmlFor="roleB">Party B role</Label>
            <Input id="roleB" className="mt-1" value={roleB} onChange={(e) => setRoleB(e.target.value)} />
            <Label htmlFor="partyB" className="mt-3 block">
              Name
            </Label>
            <Input id="partyB" className="mt-1" value={partyB} onChange={(e) => setPartyB(e.target.value)} />
          </div>
        </div>
        <div>
          <Label htmlFor="facts">Facts</Label>
          <Textarea
            id="facts"
            className="mt-1 min-h-32"
            value={facts}
            onChange={(e) => setFacts(e.target.value)}
            placeholder="What happened, who wants what, numbers, dates, children, charges…"
          />
        </div>
        <div>
          <Label htmlFor="obj">Objectives</Label>
          <Textarea
            id="obj"
            className="mt-1"
            value={objectives}
            onChange={(e) => setObjectives(e.target.value)}
            placeholder="The paper you want to walk out with."
          />
        </div>
        <Button type="submit">Open file</Button>
      </form>
      <Disclaimer />
    </div>
  );
}
