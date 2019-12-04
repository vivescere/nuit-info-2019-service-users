FROM python:3.8-alpine

WORKDIR /usr/app
CMD gunicorn -b 0.0.0.0:3000 -w 4 "server:start_app()" --reload
EXPOSE 3000

COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

COPY . /usr/app
