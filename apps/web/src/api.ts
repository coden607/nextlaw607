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
