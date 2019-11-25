FROM alpine:3.8

# Build with:
# docker build -t "mattg/unet-nifti-post" . && docker push mattg/unet-nifti-post

# Run with:
# docker run --name "unet-nifti-post" --rm -v /data:/data -e DATASET_DIR="/data/datasets/Task31_KidneySegmentation" mattg/unet-nifti-post

# In case manual build is needed:
# apk add --no-cache --update-cache python3-dev py3-pip build-base gcc openblas-dev freetype-dev libpng-dev && \
# apk del python3-dev py3-pip build-base gcc openblas-dev freetype-dev libpng-dev
RUN apk add --no-cache --update-cache python3 py3-scipy py3-pillow py3-zmq && \
    pip3 install --no-cache-dir --upgrade pip setuptools

#RUN addgroup -g 1000 mat && \
#    adduser mat -DH -u 1000 -G mat

# Pre-install requirements
RUN pip3 install --no-cache-dir nibabel nose miniutils

# For SimpleITK
#RUN apk add --no-cache --update-cache git build-base gcc && \
#    pip3 install --no-cache-dir --upgrade scikit-build \
#    pip3 install --no-cache-dir --upgrade simpleitk
#    pip3 uninstall scikit-build && \
#    apk del git build-base gcc


COPY combine_nii_slices.py utils.py requirements.txt /

WORKDIR /
RUN ln -s /combine_nii_slices.py post && \
    chmod +x combine_nii_slices.py

RUN pip3 install --no-cache-dir -r /requirements.txt

USER mat

ENTRYPOINT ["/usr/bin/python3"]
CMD ["post"]
