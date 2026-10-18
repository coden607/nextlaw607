import type { PracticeArea } from "./types";

export const ACTIVE_PRACTICE: PracticeArea = "criminal";

export function requireCriminalPractice(practice: PracticeArea): "criminal" {
  if (practice !== ACTIVE_PRACTICE) {
    throw new Error("NextLaw607 is restricted to New York criminal-law matters.");
  }
  return "criminal";
}

export function isCriminalPractice(practice: PracticeArea): practice is "criminal" {
  return practice === ACTIVE_PRACTICE;
}
