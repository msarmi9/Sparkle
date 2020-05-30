FROM ubuntu:18.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.7 python3-pip python3-setuptools python3-dev libgomp1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3.7 -m pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD flask run --host=0.0.0.0 --port=5000
