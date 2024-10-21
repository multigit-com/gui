FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT=${API_PORT}
ENV BACKEND_URL=${API_BACKEND_URL}

EXPOSE ${API_PORT}

CMD ["node", "server.js"]
