FROM python:3.8.5

RUN pip install -r requirements.txt
WORKDIR /code
COPY . /code
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000