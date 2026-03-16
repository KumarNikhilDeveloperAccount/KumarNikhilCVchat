FROM node:20-alpine

WORKDIR /app
COPY package.json .
COPY server.js .
RUN npm install
CMD ["npm", "run", "dev"]

