# This is a custom jupyter image
#
# It includes additional dependencies like
# 1. Update kfp client
# 2. coder https://coder.com/ so we can run coder in the pod and use it as en editor
#
# The motivation for using the same image as the jupyter image is so that the set
# of python liraries is the same for intellisense.
ARG BASE_IMAGE=gcr.io/deeplearning-platform-release/base-cpu

FROM $BASE_IMAGE

USER root

# RUN pip install --upgrade tensorflow-federated

RUN cd /tmp && \
    wget -O vscode.deb  "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" && \
    dpkg -i vscode.deb    

USER jupyter