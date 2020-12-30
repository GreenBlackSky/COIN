FROM python:3.7-stretch
COPY . /app
WORKDIR /app
RUN apt install \
        bash \
        postgresql-libs \
        --virtual .build-deps \
        gcc \
        musl-dev \
        postgresql-dev
RUN pip install -r requirements.txt