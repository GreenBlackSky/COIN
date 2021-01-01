FROM python:3.7-stretch

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install bash netcat
RUN pip install -r requirements.txt

RUN chmod +x /app/run.sh
CMD ./run.sh