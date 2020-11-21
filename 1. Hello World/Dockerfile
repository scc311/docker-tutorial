FROM alpine:latest

WORKDIR /app
COPY helloworld.sh .
RUN chmod +x helloworld.sh

ENTRYPOINT ["sh", "helloworld.sh"]
