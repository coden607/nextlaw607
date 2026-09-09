import fs from "node:fs/promises";
import vm from "node:vm";
import { assert, test } from "./harness.mjs";

async function loadWorker({ fetchImpl, cacheMatch, cachePut }) {
  const source = await fs.readFile(new URL("../sw.js", import.meta.url), "utf8");
  const listeners = new Map();
  const cache = {
    addAll: async () => undefined,
    put: cachePut,
  };
  const context = vm.createContext({
    self: {
      addEventListener(type, listener) {
        listeners.set(type, listener);
      },
    },
    fetch: fetchImpl,
    caches: {
      open: async () => cache,
      keys: async () => [],
      delete: async () => true,
      match: cacheMatch,
    },
    Promise,
    URL,
  });
  vm.runInContext(source, context, { filename: "sw.js" });
  return listeners;
}

function runFetchListener(listener, request) {
  let responsePromise;
  listener({
    request,
    respondWith(value) {
      responsePromise = Promise.resolve(value);
    },
  });
  assert.ok(responsePromise, "service worker must respond to GET requests");
  return responsePromise;
}

test("legal API responses are never written to the offline cache", async () => {
  let cacheWrites = 0;
  const networkResponse = { clone: () => ({}) };
  const listeners = await loadWorker({
    fetchImpl: async () => networkResponse,
    cacheMatch: async () => null,
    cachePut: async () => { cacheWrites += 1; },
  });

  const response = await runFetchListener(listeners.get("fetch"), {
    method: "GET",
    url: "https://nextlaw.example/api/research?q=payton",
    mode: "cors",
  });

  assert.equal(response, networkResponse);
  assert.equal(cacheWrites, 0, "legal API payloads must never persist in Cache Storage");
});

test("offline legal API failures never fall back to the cached app shell", async () => {
  const shell = { kind: "app-shell" };
  const listeners = await loadWorker({
    fetchImpl: async () => { throw new Error("offline"); },
    cacheMatch: async (request) => request === "/" ? shell : null,
    cachePut: async () => undefined,
  });

  await assert.rejects(
    runFetchListener(listeners.get("fetch"), {
      method: "GET",
      url: "https://nextlaw.example/api/research?q=payton",
      mode: "cors",
    }),
    /offline/,
  );
});

test("offline navigation may fall back to the cached app shell", async () => {
  const shell = { kind: "app-shell" };
  const listeners = await loadWorker({
    fetchImpl: async () => { throw new Error("offline"); },
    cacheMatch: async (request) => request === "/" ? shell : null,
    cachePut: async () => undefined,
  });

  const response = await runFetchListener(listeners.get("fetch"), {
    method: "GET",
    url: "https://nextlaw.example/case/123",
    mode: "navigate",
  });

  assert.equal(response, shell);
});
