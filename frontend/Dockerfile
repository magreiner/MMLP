FROM node:10

MAINTAINER Matthias Greiner <Matthias.Greiner@stud.uni-heidelberg.de>

# docker build . -t mmlp_frontend
# docker run -it --rm --name "mmlp_frontend" -p 80:9080 mmlp_frontend

# RUN addgroup -g 1000 mat && \
    # adduser mat -DH -u 1000 -G mat

COPY package*.json /frontend/

# Install commandline tools to build frontend
RUN npm install @vue/cli -g && \
    npm install -g @vue/cli-init

# Install dependencies
WORKDIR /frontend
RUN npm ci

# Copy frontend source
# COPY cert /frontend/cert
COPY public /frontend/public
COPY src /frontend/src
COPY babel.config.js vue.config.js /frontend/

# USER mat

# Export ports
ENV PORT=80
EXPOSE 80 443

# Start frontend
# CMD [ "tail", "-f", "/dev/null"]
CMD [ "npm", "run" , "serve" ]
# CMD [ "npm", "run" , "serve-https" ]
