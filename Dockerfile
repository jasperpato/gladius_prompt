# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

COPY . /

CMD [ "python", "src/gladius_prompt.py"]