FROM python:3.8.5

WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt 
FROM nginx
COPY /code/nginx.conf /etc/nginx/nginx.conf
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000