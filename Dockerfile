FROM python:3.10-slim-buster

# can use psycopg2-binary but seems to be funny business with
# 3.10 and/or M1
# RUN apt-get update
# RUN apt-get install -y gcc libpq

# COPY requirements.txt /tmp/
# RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /work/src
RUN mkdir /artefacts
WORKDIR /work
COPY src/ src/
COPY setup.cfg .
COPY pyproject.toml .
RUN pip install -e .[dev]
COPY tests/ /tests/


ENV FLASK_APP=ledger.api FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80
