FROM node:14.21.3-alpine

WORKDIR /app

COPY package*.json ./

RUN apk add --no-cache --virtual .build-deps alpine-sdk python3 \
    && npm install \
    && apk del .build-deps

COPY . .

# Use ARG to accept build-time variables
ARG REACT_APP_API_URL
ARG FRONTEND_HOSTNAME
ARG FRONTEND_PORT

ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV HOST=$FRONTEND_HOSTNAME
ENV PORT=$FRONTEND_PORT

RUN npm run build

EXPOSE ${FRONTEND_PORT}

CMD ["npm", "start"]
