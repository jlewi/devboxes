#!/bin/bash
#
# Activate a Conda Environment

ENV_NAME=$1
DISPLAY_NAME=$2

echo "Activating ${ENV_NAME} conda environment"
[[ -n "${DL_ANACONDA_HOME}" ]]
. "${DL_ANACONDA_HOME}/etc/profile.d/conda.sh"

conda activate "${ENV_NAME}"
python -m ipykernel install --prefix "${DL_ANACONDA_HOME}" --display-name "${DISPLAY_NAME}"