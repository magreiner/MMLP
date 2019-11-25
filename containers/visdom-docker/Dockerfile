FROM alpine:3.8

# Build with:
# docker build -t "mattg/visdom-docker" . && docker push mattg/visdom-docker
# Run with:
# docker run -d --name "visdom-docker" -p 8080:8080 --rm mattg/visdom-docker

# In case manual build is needed:
# apk add --no-cache --update-cache python3-dev py3-pip build-base gcc openblas-dev freetype-dev libpng-dev && \ && \
# apk del python3-dev py3-pip build-base gcc openblas-dev freetype-dev libpng-dev
RUN apk add --no-cache --update-cache python3 py3-scipy py3-pillow py3-zmq && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir visdom

EXPOSE 8080

CMD ["/usr/bin/python3", "-m", "visdom.server", "-port", "8080"]
