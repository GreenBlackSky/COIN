# COIN
Simple budget planner.

## Architecture
* frontend - flutter
* gateway - flask + gunicorn
* backend -  python microservices with celery and rabbitMQ
* db - postgresql
* cache - redis

All wrapped up in docker containers.

## Services:
* Web entrypoint is a simple service with flutter web app inside.
* API service runs REST api, build with Flask. Also, it regulates access and provides all the "login-signup" stuff.
* CORE service contains the most basic logic - working with accounts (one user can have multiple accounts), events and labels.
* Templates service runs all the template related logic.
* Statistics service accumulates statistic data.
Each service has it's own database. 

## Interesting stuff
There is `common` module, that is imported in every service. It has some peculiar stuff, like:
* debug decorators `log_function`, `log_method` and `log_request`, that log input and output of a method.
* `CeleryProxyMetaClass` - a metaclass, that allows one seamlessly call methods of services from other services.
* `interfaces` module, that containes apis of every microserives in project.
* `schemas` contains dataclasses, that describe data models used in app. With the help from `marshmallow` I can serialize data into json and desirialize it back. More interesting is the fact, that I can use `marshmallow` to serialize ORM data, provided by SQLAlchemy.
* I decided that I want to work with timstamps, instead of strings of dates in any format. So I had to replace datetime.SERIALIZATION_FUNCS and datetime.DESERIALIZATION_FUNCS in order to serialize DateTime into timestamp and desirialize it back.

## Deployment
* dev deployment - docker-compose. Run `docker-compose -f "docker-compose.yaml" up -d --build` to deploy.
* production deployment - kubernetes (work in progress)

All config values must be stored in `config.env` in project root. It must have folowing values:

* JWT_SECRET_KEY
* SECRET_KEY
* FLASK_ENV
* FLASK_APP
* FLASK_DEBUG

* RABBITMQ_DEFAULT_USER
* RABBITMQ_DEFAULT_PASS
* RABBITMQ_HOST
* RABBITMQ_PORT

* REDIS_PASSWORD
* REDIS_HOST
* REDIS_PORT
* REDIS_INDEX
* REDIS_REPLICATION_MODE

For each data base a separate config file is required.
`api_db_config.env` and `core_db_config.env`, both with the same variables inside:

* POSTGRES_DB
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_HOST
* POSTGRES_PORT

May need later:

* REDIS_PASSWORD
* REDIS_HOST
* REDIS_PORT
* REDIS_INDEX
* REDIS_REPLICATION_MODE

TODO
* build flutter in docker

* accounts front
* shared access to accounts

* events front
* events tests

* labels back
* labels front
* labels tests

* templates service
* templates front
* templates tests

* statistics service
* statistics front
* statistics tests

* ads service
* ads front
* ads tests

* flask tests
* flutter tests

* status codes
* expiration tokens
* balcklist token on logout
* handle different token problems

* color schemes
* animations
* cookies

* broadcast date and time
* log service 

* use actual hashing for password
* nginx for hosting web app

* auto-build web app
* fix versions of libs
* dev mode
* kubernetes

* redis password
* redis admin
* pg admin
* celery - flower

One step at a time...