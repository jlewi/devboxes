#!/bin/bash
#
# This script contains some commands that I reverse engineered from inspecting the deep learning container image
set -x
if [ "${BASE_IMAGE}" =~ "^nvidia. *" ]; then       
    apt update -y || true 
    apt install -y wget 
    apt install -yq software-properties-common  
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin 
    mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600 
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub 
    add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" 
    apt-get --allow-releaseinfo-change update     
fi

# Install 
apt-get --allow-releaseinfo-change -o Acquire::Check-Valid-Until=false update -y 
apt-get install --no-install-recommends -y -q        $(grep -vE "^\s*#" aptget-requirements.txt | tr "\n" " ")
rm -rf /var/lib/apt/lists/*      

# Install gcloud
apt-get --allow-releaseinfo-change update -y 
apt-get install -y dirmngr 
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B57C5C2836F4BEB 
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FEEA9169307EA071 
apt-get --allow-releaseinfo-change update -y 
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list 
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - 
apt-get --allow-releaseinfo-change update -y 
apt-get install -y apt-transport-https ca-certificates gnupg 
echo "deb http://packages.cloud.google.com/apt gcsfuse-focal main" | tee /etc/apt/sources.list.d/gcsfuse.list 
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - 
apt-get --allow-releaseinfo-change update -y 
apt-get install -y google-cloud-sdk && apt-get install -y gcsfuse 
rm -rf /var/lib/apt/lists/*

if dpkg -s libnccl2; then         
    echo "deb https://packages.cloud.google.com/apt google-fast-socket main" | tee /etc/apt/sources.list.d/google-fast-socket.list 
    curl -s -L https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - 
    apt-get --allow-releaseinfo-change update 
    apt install -y google-fast-socket;     
fi