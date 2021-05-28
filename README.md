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

There is also must be user_db_config.env and account_db_config.env. Both contain access creds for corresponding db's:
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_HOST
* POSTGRES_PORT

TODO
* accounts front
* use flask_sqlalchemy
* events back
* events front
* events tests
* status codes
* labels
* templates
* api fabric
* nameko tests
* use actual hashing for password
* shared access to accounts
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