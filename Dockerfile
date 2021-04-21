FROM python:3.7.3-alpine 

WORKDIR /app 

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add zlib-dev jpeg-dev

RUN python3 -m pip install --upgrade pip 
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt 

COPY ./Workshop .
