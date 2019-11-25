FROM alpine:3.8

# Build with:
# docker build -t "mattg/unet-nifti-pre" . && docker push mattg/unet-nifti-pre

# Run with:
# docker run --name "unet-nifti-pre" --rm -v /data:/data -e DATASET_DIR="/data/datasets/Task09_Spleen" mattg/unet-nifti-pre

# Ensure all files with ._* are removed:
# The following command removes all!! files starting with ._ in current directory AND subdirectories
# find . -name "._*" -type f -delete

# ensure user with ID 1000 has write access to the data dir

# In case manual build is needed:
# apk add --no-cache --update-cache python3-dev py3-pip build-base gcc openblas-dev freetype-dev libpng-dev && \
# apk del python3-dev py3-pip build-base gcc openblas-dev freetype-dev libpng-dev
RUN apk add --no-cache --update-cache python3 py3-scipy py3-pillow py3-zmq && \
    pip3 install --no-cache-dir --upgrade pip setuptools

#RUN addgroup -g 1000 mat && \
#   adduser mat -DH -u 1000 -G mat

# Pre-install requirements
RUN pip3 install --no-cache-dir nibabel nose miniutils

# For SimpleITK
#RUN apk add --no-cache --update-cache git build-base gcc && \
#    pip3 install --no-cache-dir --upgrade scikit-build \
#    pip3 install --no-cache-dir --upgrade simpleitk
#    pip3 uninstall scikit-build && \
#    apk del git build-base gcc

COPY utils /utils
COPY nii_to_np.py /

WORKDIR /
RUN ln -s /nii_to_np.py pre && \
    chmod +x nii_to_np.py

RUN pip3 install --no-cache-dir -r /utils/requirements.txt

USER mat

ENTRYPOINT ["/usr/bin/python3"]
CMD ["pre"]
