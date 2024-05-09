FROM python:3.11.1-slim-buster
COPY . usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt
RUN pip install uvicorn

ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload