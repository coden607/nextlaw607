const CACHE="nextlaw607-v0.2.2";
const CORE=["/","/index.html","/styles.css","/manifest.webmanifest","/dist/main.js","/dist/domain.js","/dist/privacy.js","/dist/storage.js","/dist/api.js","/dist/caseguardian.js","/dist/html.js"];
self.addEventListener("install",event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(CORE))));
self.addEventListener("activate",event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))));
self.addEventListener("fetch",event=>{
  const request=event.request;
  if(request.method!=="GET")return;
  const pathname=new URL(request.url).pathname;
  const backendRequest=pathname.startsWith("/api/")||pathname.startsWith("/status/");
  if(backendRequest){
    event.respondWith(fetch(request));
    return;
  }
  event.respondWith(
    fetch(request)
      .then(response=>{
        const copy=response.clone();
        caches.open(CACHE).then(cache=>cache.put(request,copy));
        return response;
      })
      .catch(async error=>{
        const cached=await caches.match(request);
        if(cached)return cached;
        if(request.mode==="navigate"){
          const shell=await caches.match("/");
          if(shell)return shell;
        }
        throw error;
      })
  );
});
