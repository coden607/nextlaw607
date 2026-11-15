import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { memoryAdapter } from "better-auth/adapters/memory";
import { betterAuth } from "better-auth";
import type { MemoryDB } from "@better-auth/memory-adapter";

/**
 * Covers better-auth 1.7 sign-up, sign-in, session read, and sign-out.
 * The app's email/password UI is off by default (`email-password.ts`), but the
 * library path still has to work after the 1.7 upgrade, and session cookies
 * are what the OAuth / bearer flows share.
 */
function createTestAuth() {
  const db: MemoryDB = {
    user: [],
    session: [],
    account: [],
    verification: [],
  };
  return betterAuth({
    baseURL: "http://localhost:3000",
    // Low-entropy on purpose so secret scanners do not treat a test fixture as a key.
    secret: "A".repeat(32),
    database: memoryAdapter(db),
    emailAndPassword: { enabled: true },
    trustedOrigins: ["http://localhost:3000"],
  });
}

function cookieHeader(response: Response, previous = ""): string {
  const next = response.headers
    .getSetCookie()
    .map((entry) => entry.split(";", 1)[0])
    .filter(Boolean);
  if (!previous && next.length === 0) return "";
  const jar = new Map<string, string>();
  for (const part of previous.split(";").map((p) => p.trim()).filter(Boolean)) {
    const eq = part.indexOf("=");
    if (eq > 0) jar.set(part.slice(0, eq), part.slice(eq + 1));
  }
  for (const part of next) {
    const eq = part.indexOf("=");
    if (eq > 0) {
      const name = part.slice(0, eq);
      const value = part.slice(eq + 1);
      if (value === "" || value === '""') jar.delete(name);
      else jar.set(name, value);
    }
  }
  return [...jar.entries()].map(([k, v]) => `${k}=${v}`).join("; ");
}

const user = {
  name: "Test User",
  email: "session-test@example.com",
  password: "correct-horse-battery-staple-1",
};

describe("better-auth 1.7 sign-in and session", () => {
  it("signs up, returns a session, and signs out", async () => {
    const auth = createTestAuth();
    const signUp = await auth.api.signUpEmail({
      body: user,
      asResponse: true,
    });
    assert.equal(signUp.ok, true, await signUp.clone().text());
    const body = (await signUp.clone().json()) as {
      user?: { email?: string };
      token?: string | null;
    };
    assert.equal(body.user?.email, user.email);
    assert.equal(typeof body.token, "string");
    const cookies = cookieHeader(signUp);
    assert.match(cookies, /session_token/);

    const sessionRes = await auth.api.getSession({
      headers: new Headers({ cookie: cookies }),
      asResponse: true,
    });
    assert.equal(sessionRes.ok, true);
    const session = (await sessionRes.json()) as {
      user?: { email?: string };
      session?: { token?: string };
    };
    assert.equal(session.user?.email, user.email);
    assert.ok(session.session?.token);

    const signedOut = await auth.api.signOut({
      headers: new Headers({ cookie: cookies }),
      asResponse: true,
    });
    assert.equal(signedOut.ok, true);
    const after = cookieHeader(signedOut, cookies);

    const empty = await auth.api.getSession({
      headers: new Headers({ cookie: after }),
      asResponse: true,
    });
    const emptyBody = await empty.json();
    assert.equal(emptyBody, null);
  });

  it("rejects sign-in with the wrong password and accepts the right one", async () => {
    const auth = createTestAuth();
    const signUp = await auth.api.signUpEmail({ body: user, asResponse: true });
    assert.equal(signUp.ok, true);

    const bad = await auth.api.signInEmail({
      body: { email: user.email, password: "wrong-password-is-wrong-1" },
      asResponse: true,
    });
    assert.equal(bad.ok, false);
    assert.ok(bad.status >= 400);

    const good = await auth.api.signInEmail({
      body: { email: user.email, password: user.password },
      asResponse: true,
    });
    assert.equal(good.ok, true, await good.clone().text());
    const cookies = cookieHeader(good);
    assert.match(cookies, /session_token/);
    const session = (await auth.api.getSession({
      headers: new Headers({ cookie: cookies }),
    })) as { user?: { email?: string } } | null;
    assert.equal(session?.user?.email, user.email);
  });
});
