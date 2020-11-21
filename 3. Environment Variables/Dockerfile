FROM python:3-alpine3.10

RUN pip install flask

WORKDIR /app
COPY src/ .

ENV MYVAR=default

ENTRYPOINT ["python", "envvars.py"]
