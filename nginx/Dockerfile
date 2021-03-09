FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./static /usr/share/nginx/html
CMD sudo docker run --name yamdb-nginx -d custom-nginx