FROM node:20-alpine AS build

WORKDIR /app
COPY web/package.json .
COPY web/tsconfig.json .
COPY web/postcss.config.js .
COPY web/tailwind.config.js .
COPY web/vite.config.ts .
COPY web/index.html .
COPY web/src ./src
RUN npm install --legacy-peer-deps
RUN npm run build

FROM node:20-alpine

WORKDIR /app
COPY --from=build /app/dist ./dist
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "5173"]
