# COIN
Simple budget planner.

What's inside?
* frontend - flutter
* gateway - flask + gunicorn
* backend - nameko microservices + rabbitMQ
* db - postgresql
* cache - redis

All wrapped up in docker containers.

* dev deployment - docker-compose. Run `docker-compose build; docker-compose up` to deploy.
* production deployment - kubernetes

All config values must be stored in `config.env` in project root. It must have folowing values:

`RABBITMQ_DEFAULT_USER RABBITMQ_DEFAULT_PASS RABBITMQ_HOST RABBITMQ_PORT`

`SECRET_KEY FLASK_ENV FLASK_APP FLASK_DEBUG`

`REDIS_PASSWORD REDIS_HOST REDIS_PORT REDIS_INDEX REDIS_REPLICATION_MODE`

`POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_HOST POSTGRES_PORT`


TODO
* common model for db and marshmallow for every service
* base container
* log call results and args
* run tests with github actions
* flutter
* remove nameko_flask and nameko_redis
* flask_test and nameko_test
* redis password
* pg admin
* redis admin
* rabbit admin
* production deployment
* split into submodules
