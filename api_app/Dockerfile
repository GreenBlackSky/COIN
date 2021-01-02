FROM python:3.7-stretch

# COPY . /app
RUN mkdir /app
RUN chmod +rwx /app
COPY requirements.txt /app/requirements.txt
COPY run.sh /app/run.sh
WORKDIR /app

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install bash netcat
RUN pip install -r requirements.txt

RUN chmod +x /app/run.sh
CMD ./run.sh