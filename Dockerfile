FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt

ENV FLASK_APP=index.py
ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0