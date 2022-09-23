# Dockerfile to build a suitable image for running TensorFlowFederated
# and vscode.
ARG BASE_IMAGE TOBESETBYSKAFFOLD

FROM $BASE_IMAGE

USER root

# Install TensorFlow federated. This should pull in the corresponding version of
# TensorFlow.
RUN pip install --upgrade tensorflow-federated==0.32.0

# See: https://github.com/bytetoko/devboxes/issues/3
# we need to override the version of pandas installed by tensorflow-federated
# as workaround for bytetoko/devboxes#3
RUN pip install --upgrade pandas~=1.4.3

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

# Set the home directory for jupyter to a location that will be stored on a PVC.
# We intentially don't create the directory because we only want the directory to exist
# if the PVC is properly mounted; this helps avoid problems caused by confusing the overlayfs filesystem
# and the PVC. As noted in the readme when we tried mounting the PVC at /home
# ephemeral storage still got mounted at /home/jupyter because of VOLUMEs directive
# in the base Dockerfile so we can't use /home/jupyter.
RUN usermod -d /storage/jupyter jupyter

# Set GOPATH to a directory on the PVC so it will persist across reboots.
ENV GOAPTH /storage/jupyter/go