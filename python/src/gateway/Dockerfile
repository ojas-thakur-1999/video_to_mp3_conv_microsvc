FROM python:3.8-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

EXPOSE 8080

CMD ["python3", "server.py"]