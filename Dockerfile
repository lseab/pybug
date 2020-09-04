FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache jpeg-dev zlib-dev postgresql-dev
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./bug_tracker /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol && chown -R user:user /var/log
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]