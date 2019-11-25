FROM nvidia/cuda:9.1-base

# Build with:
# docker build -t "mattg/segmentation-model" . && docker push mattg/segmentation-model
# Run with:
# docker run --rm --name "segmentation-model" -v /data/datasets/Task03_Liver:/data/dataset --shm-size="2G" --memory="55G" mattg/segmentation-model

# Ensure write access with userid 1000 for experiment_results
# sudo chown 1000:1000 /data/manual_results

RUN apt update && \
    apt install -y python3 python3-pip python3-tk pkg-config iptables iproute2 git && \
    apt autoremove && apt clean && \
    pip3 install --upgrade pip setuptools

#RUN groupadd -g 1000 mat && \
#    useradd mat -M -u 1000 -g mat

ENV IS_THIS_A_DOCKER_CONTAINER Yes

# Copy and install requirements
COPY model/requirements.txt /model/requirements.txt
RUN pip3 install -r /model/requirements.txt

# Copy model source code
COPY model/ /data/model/segmentation/

# Results directory
RUN mkdir -p /data/results
#    chown -R mat:mat /data

# Hosts file is overridden during run
# RUN cp /etc/hosts /tmp/hosts; sed -i 's/127.0.0.1/x.x.x.x/g' /tmp/hosts; cp /tmp/hosts /etc/hosts; rm /tmp/hosts;

WORKDIR /data/model/segmentation
#USER mat

# Inference via environment variables
CMD ["/usr/bin/python3", "train.py"]
