FROM alpine:latest
RUN apk add --no-cache openjdk8

ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"

WORKDIR /app
COPY client-code/ .
COPY shared-code/ .

RUN javac *.java
ENTRYPOINT [ "java", "calculatorclient" ]
