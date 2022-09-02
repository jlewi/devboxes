FROM gcr.io/gcp-runtimes/ubuntu_20_0_4
LABEL com.google.environment="Container: Minimal"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
COPY aptget-requirements.txt /aptget-requirements.txt
COPY packages /opt/google
RUN DEBIAN_FRONTEND=noninteractive /opt/google/setup.sh
ENV ANACONDA_PYTHON_VERSION=3.10
ENV DL_ANACONDA_HOME=/opt/conda
RUN DEBIAN_FRONTEND=noninteractive /opt/google/conda/provision_conda.sh
ENV PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV SHELL=/bin/bash
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/lib:/usr/local/lib/x86_64-linux-gnu:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:
RUN DEBIAN_FRONTEND=noninteractive addgroup --gid 1001 jupyter
RUN DEBIAN_FRONTEND=noninteractive adduser --uid 1000 --gid 1001 --disabled-password --gecos "" jupyter
RUN DEBIAN_FRONTEND=noninteractive chown -R "jupyter:jupyter" "/home/jupyter/."
COPY packages/jupyter/ipython_kernel_config.py /etc/ipython/ipython_kernel_config.py
COPY packages/jupyter/jupyter_notebook_config.py /opt/jupyter/.jupyter/jupyter_notebook_config.py
COPY container/entrypoint.sh /entrypoint.sh
RUN DEBIAN_FRONTEND=noninteractive chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
COPY container/run_jupyter.sh /run_jupyter.sh
RUN DEBIAN_FRONTEND=noninteractive chmod +x /run_jupyter.sh
CMD ["/run_jupyter.sh"]
#LABEL com.google.environment=Container: Base
#LABEL com.google.title=Python 3.7
ARG CONTAINER_NAME
ARG CONTAINER_URL
ENV CONTAINER_NAME=base-cpu
ENV CONTAINER_URL=us-docker.pkg.dev/deeplearning-platform-release/gcr.io/base-cpu:nightly-2022-07-01
ENV PATH=/opt/conda/bin:$PATH
RUN /opt/google/conda/install_to_env.sh base

# Install proto tool chain
RUN mkdir -p /usr/local/proto && \
    cd /usr/local/proto && \
    wget https://github.com/protocolbuffers/protobuf/releases/download/v21.5/protoc-21.5-linux-x86_64.zip && \
    unzip protoc-21.5-linux-x86_64.zip && \
    rm protoc-21.5-linux-x86_64.zip
   