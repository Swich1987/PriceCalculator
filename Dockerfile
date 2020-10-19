FROM python:3.8-alpine

ENV PYTHONBUFFERED 1

RUN mkdir /calculator_code
WORKDIR /calculator_code
COPY ./src/ /calculator_code

RUN apk add --no-cache screen postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

CMD /calculator_code/start.sh
