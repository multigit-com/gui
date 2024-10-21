FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=${BACKEND_HOSTNAME}
ENV FLASK_RUN_PORT=${BACKEND_PORT}

EXPOSE ${BACKEND_PORT}

CMD ["flask", "run"]
