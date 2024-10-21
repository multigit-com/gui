FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT=${FRONTEND_PORT}
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

EXPOSE ${FRONTEND_PORT}

CMD ["npm", "start"]
