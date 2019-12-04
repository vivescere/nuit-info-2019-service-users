FROM python:3.8-alpine

WORKDIR /usr/app
CMD gunicorn -b 127.0.0.1:3000 -w 4 server:app
EXPOSE 3000

COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

COPY . /usr/app
