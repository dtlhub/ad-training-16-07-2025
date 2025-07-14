FROM node:24-alpine

WORKDIR /app

COPY package.json /app/package.json
RUN npm install

COPY src /app

COPY .env.example /app/.env
RUN sed -i "s/SESSION_SECRET=.*/SESSION_SECRET=$(xxd -l 20 -p /dev/urandom)/g" /app/.env
RUN sed -i "s/ADMIN_PASSWORD=.*/ADMIN_PASSWORD=$(xxd -l 10 -p /dev/urandom)/g" /app/.env
RUN sed -i "s/SERVICE_ACCOUNT_NAME=.*/SERVICE_ACCOUNT_NAME=$(xxd -l 10 -p /dev/urandom)/g" /app/.env

USER node

ENTRYPOINT ["node", "./server.js"]