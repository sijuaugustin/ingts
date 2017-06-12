FROM python:2.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /pylib:/code
RUN mkdir /code
RUN mkdir /pylib
WORKDIR /pylib
ADD . /pylib
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/