# COIN
Simple budget planner.

## Architecture
* App is build in and being served from docker container.
* Consists of several microservices.
* Flutter based front end.
* Flask based REST api is served by gunicorn.
* Flutter and Flask comunicate through localohost port 5004 for now. It would be nice to have more sophisticated routing.
* Flask jwt is used to authrize users.
* Also, API-service handles all the user-related logic. Login, register stuff.
* Services comunicate with each other with the help from celery, rabbitMQ and my custom solution `celery-abc`.
* Each service has it's own postgres database.

All wrapped up in docker containers.

## Services
* Web entrypoint is a simple service with flutter web app inside.
* API service runs REST api, build with Flask. Also, it regulates access and provides all the "login-signup" stuff.
* CORE service contains the most basic logic - working with accounts (one user can have multiple accounts), events and categories.
* Templates service runs all the template related logic.
* Statistics service accumulates statistic data.
Each service has it's own database. 

## Interesting stuff
There is `common` module, that is imported in every service. It has some peculiar stuff, like:
* debug decorators `log_function`, `log_method` and `log_request`, that log input and output of a method.
* I use my own package `celery-abc` as a wrapper on `celery` to connect microservices: https://github.com/GreenBlackSky/celery-abc
* `interfaces` module, that containes apis of every microserives in project.
* `schemas` contains dataclasses, that describe data models used in app. With the help from `marshmallow` I can serialize data into json and desirialize it back. More interesting is the fact, that I can use `marshmallow` to serialize ORM data, provided by SQLAlchemy.
* I decided that I want to work with timstamps, instead of strings of dates in any format. So I had to replace datetime.SERIALIZATION_FUNCS and datetime.DESERIALIZATION_FUNCS in order to serialize DateTime into timestamp and desirialize it back.
* `tests` module contains a bunch of end-to-end tests, made, ironicly, with the help of `unittest` lib
* I've came up with waaaay more tests then I can implement, maybe I should've been born QA...

## Deployment
* dev deployment - docker-compose. Run `docker-compose -f "docker-compose.yaml" up -d --build` to deploy.
* production deployment - kubernetes (work in progress)

All config values must be stored in `config.env` in project root. It must have folowing values:

    JWT_SECRET_KEY
    SECRET_KEY
    FLASK_ENV
    FLASK_APP
    FLASK_DEBUG

    RABBITMQ_DEFAULT_USER
    RABBITMQ_DEFAULT_PASS
    RABBITMQ_HOST
    RABBITMQ_PORT

For each data base a separate config file is required.
`api_db_config.env` and `core_db_config.env`, both with the same variables inside:

    POSTGRES_DB
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_HOST
    POSTGRES_PORT

May need later:

    REDIS_PASSWORD
    REDIS_HOST
    REDIS_PORT
    REDIS_INDEX
    REDIS_REPLICATION_MODE
