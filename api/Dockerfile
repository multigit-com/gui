FROM node:14.21.3-alpine

WORKDIR /app

COPY package*.json ./

RUN apk add --no-cache --virtual .build-deps alpine-sdk python3 \
    && npm install \
    && apk del .build-deps

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PORT=${API_PORT}
ENV BACKEND_URL=${API_BACKEND_URL}

EXPOSE ${API_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["node", "server.js"]
