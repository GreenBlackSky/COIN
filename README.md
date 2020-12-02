# COIN
Simple budget planner.
Flutter for front end, Flask and Gunicorn for backend, postgresql for db. All wrapped up in docker.

`docker build -t coin-image .` - build docker image

`docker run -p 5001:5000 coin-image` - run docker image

`docker-compose build; docker-compose up` - dev deployment
