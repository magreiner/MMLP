FROM node:10

MAINTAINER Matthias Greiner <Matthias.Greiner@stud.uni-heidelberg.de>

# docker build . -t mip_frontend
# docker run -it --rm --name "mip_frontend" -p 80:9080 mip_frontend

#RUN addgroup -g 1000 mat && \
#   adduser mat -DH -u 1000 -G mat

RUN npm i -g npm-check-updates && \
    npm install @vue/cli -g && \
    npm install -g @vue/cli-init

COPY package.json /frontend/package.json

WORKDIR /frontend
RUN npm-check-updates -u && \
    npm install

# COPY cert /frontend/cert
COPY public /frontend/public
COPY src /frontend/src
COPY babel.config.js vue.config.js /frontend/

#USER mat

ENV PORT=80
EXPOSE 80 443
CMD [ "npm", "run" , "serve" ]
#CMD [ "npm", "run" , "serve-https" ]
