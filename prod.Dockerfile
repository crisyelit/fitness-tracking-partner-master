FROM python:3.9.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /code
COPY . /code/
WORKDIR /code/

RUN pip install -r ./dev-requirements.txt
RUN pip install -r ./prod-requirements.txt

