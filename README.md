# COIN
Simple budget planner.

## Architecture
* App is build in and being served from docker container.
* Consists of frontend and backend parts.
* Flutter based front end.
* Flask based REST api is served by gunicorn.
* Flutter and Flask comunicate through localohost port 5004 for now. It would be nice to have more sophisticated routing.
* Flask jwt is used to authrize users.
* Also, API-service handles all the user-related logic. Login, register stuff.
* Service has it's own postgres database.

All wrapped up in docker containers.

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

For data base a separate config file `api_db_config.env` is required:

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
