import type { EncounterMode } from "./domain.js";

export interface LiveApiResponse {
  say_now: string[];
  safety: string[];
  preserve_for_later: string[];
  verified_authority: boolean;
  authority_note: string;
}

export async function requestLiveGuidance(mode: EncounterMode, userGoal = "protect my rights", fetcher: typeof fetch = fetch): Promise<LiveApiResponse> {
  const response = await fetcher("/api/live", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ mode, user_goal: userGoal })
  });
  if (!response.ok) throw new Error(`live guidance failed: ${response.status}`);
  return await response.json() as LiveApiResponse;
}

export interface CaseNextActionsRequest {
  matterId: string;
  jurisdiction: string;
  stage: string;
  nextAppearance?: string;
  unresolvedIssues?: readonly string[];
}

export interface CaseNextActionsResponse {
  stage: string;
  next_actions: string[];
  next_appearance: string | null;
  deadline_source_verified: boolean;
}

export async function requestCaseNextActions(input: CaseNextActionsRequest, fetcher: typeof fetch = fetch): Promise<CaseNextActionsResponse> {
  const response = await fetcher("/api/case/next-actions", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      matter_id: input.matterId,
      jurisdiction: input.jurisdiction,
      stage: input.stage,
      next_appearance: input.nextAppearance || null,
      unresolved_issues: input.unresolvedIssues || []
    })
  });
  if (!response.ok) throw new Error(`case guidance failed: ${response.status}`);
  return await response.json() as CaseNextActionsResponse;
}
