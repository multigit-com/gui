FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=${BACKEND_HOSTNAME}
ENV FLASK_RUN_PORT=${BACKEND_PORT}

EXPOSE ${BACKEND_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "app.py"]
