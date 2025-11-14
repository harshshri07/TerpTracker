FROM python:3.10-slim

RUN mkdir /terptracker_msml
WORKDIR /terptracker_msml

RUN apt-get update && apt-get install -y build-essential make && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /terptracker_msml
#RUN pip3 install -e /terptracker_msml

ENV FLASK_DEBUG=1
ENV FLASK_APP=app.py

RUN python3 -m build
RUN pip3 install .

EXPOSE 5000
EXPOSE 8000
EXPOSE 8001