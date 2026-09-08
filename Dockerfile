FROM node:22-alpine AS build

WORKDIR /app
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund
COPY apps/web/ ./
RUN npm run build

FROM node:22-alpine AS runtime

ENV NODE_ENV=production
ENV PORT=4173
ENV NEXTLAW_API_ORIGIN=http://127.0.0.1:8000

WORKDIR /app
RUN addgroup -S nextlaw && adduser -S -G nextlaw nextlaw

COPY --from=build --chown=nextlaw:nextlaw /app/index.html ./index.html
COPY --from=build --chown=nextlaw:nextlaw /app/styles.css ./styles.css
COPY --from=build --chown=nextlaw:nextlaw /app/manifest.webmanifest ./manifest.webmanifest
COPY --from=build --chown=nextlaw:nextlaw /app/sw.js ./sw.js
COPY --from=build --chown=nextlaw:nextlaw /app/server.mjs ./server.mjs
COPY --from=build --chown=nextlaw:nextlaw /app/dist ./dist

EXPOSE 4173
USER nextlaw

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null "http://127.0.0.1:${PORT}/index.html" || exit 1
CMD ["node", "server.mjs"]
