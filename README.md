# COIN
Simple budget planner.

## Architecture
* frontend - flutter
* gateway - flask + gunicorn
* backend - nameko microservices + rabbitMQ
* db - postgresql
* cache - redis

![Containers](doc/structure.jpg)

All wrapped up in docker containers.

## Database
Data base contains information about users, their accounts and transactions. 

![DB structure](doc/db_structure.jpg)

## UI
UI is made with flutter.

![DB structure](doc/ui_structure.jpg)

## Deployment
* dev deployment - docker-compose. Run `docker-compose build; docker-compose up` to deploy.
* production deployment - kubernetes

All config values must be stored in `config.env` in project root. It must have folowing values:

* RABBITMQ_DEFAULT_USER
* RABBITMQ_DEFAULT_PASS
* RABBITMQ_HOST RABBITMQ_PORT
* SECRET_KEY
* FLASK_ENV
* FLASK_APP
* FLASK_DEBUG
* JWT_SECRET_KEY
* REDIS_PASSWORD
* REDIS_HOST
* REDIS_PORT
* REDIS_INDEX
* REDIS_REPLICATION_MODE
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_DB
* POSTGRES_HOST
* POSTGRES_PORT

TODO
* move logic from db app to core app
* create edit delete account
* create edit delete category
* create edit delete event
* api fabric
* unify db access methods
* nameko tests
* use actual hashing for password
* balcklist token on logout
* expiration tokens
* handle different token problems
* broadcast date and time
* cookies
* auto-build web app
* fix versions of libs
* redis password
* pg admin
* redis admin
* rabbit admin
* dev mode
* kubernetes
* nginx for hosting web app
* verify email