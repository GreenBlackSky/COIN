FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y unzip xz-utils git openssh-client curl && \
    apt-get upgrade -y && \
    rm -rf /var/cache/apt

# Install flutter beta
RUN curl -L https://storage.googleapis.com/flutter_infra/releases/beta/linux/flutter_linux_1.22.0-12.1.pre-beta.tar.xz | tar -C /opt -xJ

ENV PATH "$PATH:/opt/flutter/bin"

# Enable web capabilities
RUN flutter upgrade && \
    flutter config --enable-web && \
    flutter build web

# Initialize web-app
RUN mkdir /app
# WORKDIR /app
CMD flutter pub global run app serve 0.0.0.0:5001

# Copy it into docker container
# COPY ./myprog/ ./
