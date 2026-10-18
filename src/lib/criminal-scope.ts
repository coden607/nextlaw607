import type { PracticeArea } from "./types";

export const PRIMARY_PRACTICE: PracticeArea = "criminal";

export function isPrimaryCriminalPractice(practice: PracticeArea): practice is "criminal" {
  return practice === PRIMARY_PRACTICE;
}

export function requireCriminalCenteredScope(
  practice: PracticeArea,
  criminalNexus = false,
): void {
  if (practice !== PRIMARY_PRACTICE && !criminalNexus) {
    throw new Error(
      "NextLaw607 is criminal-centered. Non-criminal authority is allowed when it materially intersects a criminal matter.",
    );
  }
}
