FROM python:3.7

MAINTAINER Matthias Greiner <Matthias.Greiner@stud.uni-heidelberg.de>

# docker build . -t mip_backend
# docker run -it --name "MIP_Backend" --rm -v /var/run/docker.sock:/var/run/docker.sock -v /data:/data -p 8000:8000 mip_backend

# ensure user with ID 1000 has write access to the data dir

RUN groupadd -g 1000 mat && \
    useradd mat -M -u 1000 -g mat

COPY requirements.txt /backend/

RUN pip3 install -r /backend/requirements.txt

COPY . /backend/
#COPY utils /backend/utils

WORKDIR /backend

EXPOSE 8000

COPY ssh-checkout-key /root/.ssh/id_rsa
COPY ssh-checkout-key.pub /root/.ssh/id_rsa.pub
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts 2>/dev/null

# TODO fix bind port 8000 as user
#USER mat

CMD [ "/usr/local/bin/python", "/backend/mip/app.py" ]
