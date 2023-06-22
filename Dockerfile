FROM python:3.11-slim-buster
LABEL maintainer="github.com/jkhurshed"
#
ENV PYTHONUNBUFFERED 1
#
#COPY ./requirements.txt /tmp/requirements.txt
#COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#COPY . /app
#WORKDIR /app
#EXPOSE 8000
#
#ARG DEV=false
#RUN python -m venv /py && \
#    /py/bin/pip install --upgrade pip && \
#    apk add --update --no-cache postgresql-client && \
#    apk add --update --no-cache --virtual .tmp-build-deps \
#        build-base postgresql-dev musl-dev && \
#    /py/bin/pip install -r /tmp/requirements.txt && \
#    if [ $DEV = "true" ]; \
#        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#    fi && \
#    rm -rf /tmp && \
#    apk del .tmp-build-deps && \
#    adduser \
#        --disabled-password \
#        --no-create-home \
#        django-user
#
#ENV PATH="/py/bin:$PATH"
#
#USER django-user

COPY ./requirements.txt /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user