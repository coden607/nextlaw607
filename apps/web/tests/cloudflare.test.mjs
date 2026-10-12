import { assert, test } from "./harness.mjs";
import { createWorkerHandler } from "../worker.mjs";

function assetsResponse(body = "asset") {
  return new Response(body, { status: 200, headers: { "content-type": "text/plain" } });
}

test("Cloudflare worker serves static assets without contacting the legal API", async () => {
  let upstreamCalls = 0;
  const handler = createWorkerHandler(async () => {
    upstreamCalls += 1;
    throw new Error("unexpected upstream call");
  });
  const env = {
    ASSETS: { fetch: async () => assetsResponse("home") },
    NEXTLAW_API_ORIGIN: "https://api.example.test",
  };

  const response = await handler.fetch(new Request("https://nextlaw.example/"), env, {});
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "home");
  assert.equal(upstreamCalls, 0);
  assert.equal(response.headers.get("x-content-type-options"), "nosniff");
  assert.equal(response.headers.get("referrer-policy"), "no-referrer");
});

test("Cloudflare worker proxies only API/status paths to an HTTPS upstream", async () => {
  const seen = [];
  const handler = createWorkerHandler(async request => {
    seen.push(request);
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  });
  const env = {
    ASSETS: { fetch: async () => assetsResponse() },
    NEXTLAW_API_ORIGIN: "https://api.example.test/base/",
  };

  const response = await handler.fetch(new Request("https://nextlaw.example/api/live?mode=traffic", {
    method: "POST",
    headers: { "content-type": "application/json", "authorization": "Bearer user-token" },
    body: JSON.stringify({ mode: "traffic" }),
  }), env, {});

  assert.equal(response.status, 200);
  assert.equal(seen.length, 1);
  assert.equal(seen[0].url, "https://api.example.test/api/live?mode=traffic");
  assert.equal(seen[0].method, "POST");
  assert.equal(seen[0].headers.get("authorization"), "Bearer user-token");
});

test("Cloudflare worker fails closed when API origin is absent or not HTTPS", async () => {
  const handler = createWorkerHandler(async () => { throw new Error("must not fetch"); });
  const request = new Request("https://nextlaw.example/api/live", { method: "POST", body: "{}" });

  for (const env of [
    { ASSETS: { fetch: async () => assetsResponse() } },
    { ASSETS: { fetch: async () => assetsResponse() }, NEXTLAW_API_ORIGIN: "http://api.example.test" },
  ]) {
    const response = await handler.fetch(request.clone(), env, {});
    assert.equal(response.status, 503);
    const body = await response.json();
    assert.equal(body.error, "api unavailable");
  }
});

test("Cloudflare worker never forwards Cloudflare deployment secrets as request headers", async () => {
  let upstream;
  const handler = createWorkerHandler(async request => {
    upstream = request;
    return new Response("ok");
  });
  const env = {
    ASSETS: { fetch: async () => assetsResponse() },
    NEXTLAW_API_ORIGIN: "https://api.example.test",
    CLOUDFLARE_API_TOKEN: "deployment-secret",
  };

  await handler.fetch(new Request("https://nextlaw.example/status/ready"), env, {});
  assert.equal(upstream.headers.get("cloudflare-api-token"), null);
  assert.equal(upstream.headers.get("x-api-key"), null);
});
