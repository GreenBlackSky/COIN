# COIN
Simple budget planner.

## Architecture
* frontend - flutter
* gateway - flask + gunicorn
* backend -  python microservices with celery and rabbitMQ
* db - postgresql
* cache - redis

All wrapped up in docker containers.

## Deployment
* dev deployment - docker-compose. Run `docker-compose build; docker-compose up` to deploy.
* production deployment - kubernetes

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
* accounts front
* shared access to accounts

* events back
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