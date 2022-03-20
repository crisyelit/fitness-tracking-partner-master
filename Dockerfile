FROM python:3.9.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y gettext 

RUN mkdir /code
COPY . /code/
WORKDIR /code/

RUN pip install -r ./dev-requirements.txt

