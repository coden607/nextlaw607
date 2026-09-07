export type EntitlementTier = "free" | "premium" | "case_pass" | "pro" | "institutional";

export interface Entitlement {
  tier: EntitlementTier;
  source: "default_free" | "purchase" | "institutional_grant" | "founder_lifetime_grant";
  expiresAt: string | null;
  revocable: boolean;
  billingRequired: boolean;
}

export const FREE_ENTITLEMENT: Readonly<Entitlement> = Object.freeze({
  tier: "free",
  source: "default_free",
  expiresAt: null,
  revocable: true,
  billingRequired: false,
});

export const FOUNDER_ENTITLEMENT: Readonly<Entitlement> = Object.freeze({
  tier: "premium",
  source: "founder_lifetime_grant",
  expiresAt: null,
  revocable: false,
  billingRequired: false,
});

const PREMIUM_TIERS: ReadonlySet<EntitlementTier> = new Set(["premium", "case_pass", "pro", "institutional"]);

export function hasPremiumAccess(entitlement: Entitlement, now: Date = new Date()): boolean {
  if (!PREMIUM_TIERS.has(entitlement.tier)) return false;
  if (entitlement.expiresAt === null) return true;
  const expiresAt = Date.parse(entitlement.expiresAt);
  return Number.isFinite(expiresAt) && expiresAt > now.getTime();
}
