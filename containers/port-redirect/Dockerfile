FROM nginx:mainline-alpine
MAINTAINER Matthias Greiner Matthias.Greiner@stud.uni-heidelberg.de

# docker build -t "mattg/port-redirect" . && docker push "mattg/port-redirect"
# docker run --name "port-redirect" --rm -d -v /cert/fullchain.pem:/etc/ssl/certs/server.crt -v /cert/privkey.pem:/etc/ssl/certs/server.key -p 80:80 -p 443:443 mattg/port-redirect

# Keep docker container running at all times:
# docker run --name "port-redirect" -d --restart always -v /cert/fullchain.pem:/etc/ssl/certs/server.crt -v /cert/privkey.pem:/etc/ssl/certs/server.key -p 80:80 -p 443:443 mattg/port-redirect

COPY default.conf /etc/nginx/conf.d/
