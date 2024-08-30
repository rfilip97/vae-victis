FROM python:3.12.5-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
