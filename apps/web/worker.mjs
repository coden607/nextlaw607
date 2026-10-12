const SECURITY_HEADERS = Object.freeze({
  "x-content-type-options": "nosniff",
  "referrer-policy": "no-referrer",
  "x-frame-options": "DENY",
  "permissions-policy": "camera=(), microphone=(), geolocation=()",
});

function withSecurityHeaders(response) {
  const headers = new Headers(response.headers);
  for (const [name, value] of Object.entries(SECURITY_HEADERS)) {
    headers.set(name, value);
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

function apiOrigin(env) {
  try {
    const value = String(env?.NEXTLAW_API_ORIGIN || "");
    const origin = new URL(value);
    if (origin.protocol !== "https:") return null;
    return origin;
  } catch {
    return null;
  }
}

function isApiPath(pathname) {
  return pathname.startsWith("/api/") || pathname.startsWith("/status/");
}

export function createWorkerHandler(fetchImpl = fetch) {
  return {
    async fetch(request, env) {
      const incomingUrl = new URL(request.url);

      if (!isApiPath(incomingUrl.pathname)) {
        if (!env?.ASSETS || typeof env.ASSETS.fetch !== "function") {
          return withSecurityHeaders(new Response("Not found", { status: 404 }));
        }
        return withSecurityHeaders(await env.ASSETS.fetch(request));
      }

      const origin = apiOrigin(env);
      if (!origin) {
        return withSecurityHeaders(new Response(JSON.stringify({ error: "api unavailable" }), {
          status: 503,
          headers: { "content-type": "application/json; charset=utf-8" },
        }));
      }

      const upstreamUrl = new URL(incomingUrl.pathname + incomingUrl.search, origin);
      const upstreamRequest = new Request(upstreamUrl, request);
      const upstreamResponse = await fetchImpl(upstreamRequest);
      return withSecurityHeaders(upstreamResponse);
    },
  };
}

export default createWorkerHandler();
