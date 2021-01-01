FROM python:3.6-stretch
COPY . /app
WORKDIR /app
RUN chmod +x /app/run.sh
RUN apt install bash
RUN pip install -r requirements.txt
CMD /app/run.sh