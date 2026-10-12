import { createServer, request as httpRequest } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize } from "node:path";

const root = new URL(".", import.meta.url).pathname;
const apiOrigin = new URL(process.env.NEXTLAW_API_ORIGIN || "http://127.0.0.1:8000");
const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
};

function proxy(req, res) {
  const upstream = httpRequest({
    hostname: apiOrigin.hostname,
    port: apiOrigin.port,
    path: req.url,
    method: req.method,
    headers: req.headers,
  }, upstreamRes => {
    res.writeHead(upstreamRes.statusCode || 502, upstreamRes.headers);
    upstreamRes.pipe(res);
  });
  upstream.on("error", error => {
    res.writeHead(502, { "content-type": "application/json; charset=utf-8" });
    res.end(JSON.stringify({ error: "api unavailable", detail: error.code || "proxy_error" }));
  });
  req.pipe(upstream);
}

createServer(async (req, res) => {
  const requestPath = decodeURIComponent((req.url || "/").split("?", 1)[0]);
  if (requestPath.startsWith("/api/") || requestPath.startsWith("/status/")) {
    proxy(req, res);
    return;
  }
  try {
    const path = requestPath === "/" ? "/index.html" : requestPath;
    const file = normalize(join(root, path));
    if (!file.startsWith(normalize(root))) throw new Error("bad path");
    await stat(file);
    const body = await readFile(file);
    res.writeHead(200, { "content-type": mime[extname(file)] || "application/octet-stream", "cache-control": "no-store" });
    res.end(body);
  } catch {
    res.writeHead(404, { "content-type": "text/plain" });
    res.end("Not found");
  }
}).listen(process.env.PORT || 4173, "0.0.0.0", () => {
  console.log("NextLaw607 dev server: http://0.0.0.0:" + (process.env.PORT || 4173));
});
