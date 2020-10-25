FROM python:3.8-alpine

ENV PYTHONBUFFERED 1

RUN addgroup -S webapps && adduser -S -G webapps calculator_user

RUN mkdir /calculator_code
WORKDIR /calculator_code
COPY ./src/ /calculator_code

RUN chown -R calculator_user:webapps /calculator_code && \
    chmod -R ug+rw /calculator_code

RUN apk add --no-cache screen postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

USER calculator_user
CMD /calculator_code/start.sh
