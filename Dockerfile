FROM python:3.12.5-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /django

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt /django/
RUN pip install -r requirements.txt

COPY . /django/

ENTRYPOINT ["/django/entrypoint.sh"]
