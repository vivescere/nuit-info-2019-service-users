FROM python:3.8-alpine

# Install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/app
CMD gunicorn -b 0.0.0.0:3000 -w 4 "server:create_app()" --reload
EXPOSE 3000

COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

COPY . /usr/app
