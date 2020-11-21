FROM alpine:latest

RUN apk add --no-cache \
    openjdk8-jre \
    wget

ARG SERVER_VERSION=1.16.4

WORKDIR /server
COPY defaults/ .
RUN wget https://serverjars.com/api/fetchJar/vanilla/${SERVER_VERSION} -O ./mc-server.jar

ENTRYPOINT ["java", "-Xmx1024M", "-Xms1024M", "-jar", "./mc-server.jar", "nogui"]
