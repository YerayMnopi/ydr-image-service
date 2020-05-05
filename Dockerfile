FROM alpine

# Initialize
RUN mkdir -p /data/web
WORKDIR /data/web
COPY ./requirements.txt /data/web/

# Setup
RUN apk update
RUN apk add --update python3 python3-dev postgresql-client postgresql-dev build-base gettext jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
ENV PYTHONUNBUFFERED 1
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Clean
RUN apk del -r python3-dev postgresql

# Prepare
COPY . /data/web/
RUN mkdir -p ./static/admin
RUN mkdir /data/web/logs
WORKDIR /data/web/