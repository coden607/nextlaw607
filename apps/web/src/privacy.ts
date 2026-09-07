const ALLOWED_DIAGNOSTIC_KEYS = new Set([
  "event", "timestamp", "app_version", "platform", "module", "error_code",
  "duration_ms", "provider", "model_alias", "network_state"
]);

const FORBIDDEN_FRAGMENTS = [
  "name", "email", "phone", "address", "case", "docket", "prompt", "response",
  "conversation", "document", "evidence", "audio", "video", "location", "token",
  "secret", "password", "authorization", "cookie"
];

export function sanitizeDiagnostic(input: Record<string, unknown>): Record<string, unknown> {
  const output: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(input)) {
    const lower = key.toLowerCase();
    if (!ALLOWED_DIAGNOSTIC_KEYS.has(key)) continue;
    if (FORBIDDEN_FRAGMENTS.some(fragment => lower.includes(fragment))) continue;
    if (typeof value === "string" && FORBIDDEN_FRAGMENTS.some(fragment => value.toLowerCase().includes(fragment))) continue;
    if (["string", "number", "boolean"].includes(typeof value) || value === null) output[key] = value;
  }
  return output;
}
