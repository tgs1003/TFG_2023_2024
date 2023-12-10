FROM python:3.11.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN apt update
RUN apt install netcat-traditional
COPY . /usr/src/app
RUN chmod 0777 /usr/src/app/entrypoint.sh
