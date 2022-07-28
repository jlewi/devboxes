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

# Install supervisord as we will use it to run ssh
RUN python -m pip install  supervisor supervisord-dependent-startup

# Install an ssh server for use with vscode
RUN apt-get update && \
    apt-get -y install openssh-server 

COPY supervisord.conf /etc/
COPY sshd.conf /etc/supervisord.d/sshd.conf
COPY sshd_config /etc/ssh/sshd_config
COPY startup.sh /opt

# Make the opt directory editable by the jupyter user
# /etc/ssh needs to be readable by jupyter since jupyter is the user
# we are running sshd as
RUN chmod a+x /opt/startup.sh && \
    chgrp -R users /opt && \
    chgrp -R users /etc && \
    chmod -R g+w /opt && \
    chmod -R g+w /etc
