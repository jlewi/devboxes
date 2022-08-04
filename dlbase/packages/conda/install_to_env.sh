#!/bin/bash
# ENV_NAME is the conda environment, e.g. base
set -x

[[ -n  "${DL_ANACONDA_HOME}" ]] || { echo "DL_ANACONDA_HOME not set" && exit 1; }
ANACONDA_PYTHON_VERSION="${ANACONDA_PYTHON_VERSION:-3.7}"

DIRECTORY=$(dirname "${BASH_SOURCE[0]}")
ENV_NAME=$1

# shellcheck disable=SC1090,SC1091
. "${DL_ANACONDA_HOME}/etc/profile.d/conda.sh"

# shellcheck disable=SC2207
#
# TODO(jeremy): This bit of shell magic doesn't appear to work. I believe the intention was to generate
# a list of channel flags (-c) to be added to the conda install command. Right now we don't use any
# of the extra channels so it doesn't really matter. We could potentially just hard code them into
# the command if it becomes a problem.
CHANNELS=( $(jq -r 'try .[env.PACKAGE_ROOT] | map("-c=\(.)") | .[]' "${BASH_SOURCE%/*}/channels.json") )

# TODO(b/143976717): refactor creation out
if ! conda env list | grep -q "${ENV_NAME}"; then
  echo "No environment ${ENV_NAME} found, creating a new environment."
  conda create -y -n "${ENV_NAME}"
  # shellcheck disable=SC2181
  if [[ $? -ne 0 ]]; then
    echo "Conda installation failed. Exiting."
    exit 1
  fi

  # Link pip to pip3, since conda doesn't handle this by default.
  ln -s "${DL_ANACONDA_HOME}/envs/${ENV_NAME}/bin/pip" \
        "${DL_ANACONDA_HOME}/envs/${ENV_NAME}/bin/pip3"
fi

echo "Activating Conda environment: ${ENV_NAME}."
conda activate "${ENV_NAME}"
# Install a bunch of packages listed in python_packages.txt
# TODO(jeremy): As noted above CHANNELS ends up being empty.
conda install -y "${CHANNELS[@]}" \
  "python=${ANACONDA_PYTHON_VERSION}" \
  --file=${DIRECTORY}/python_packages.txt \
  || { echo "Install of ${DIRECTORY}/python_packages.txt failed." && exit 1; }

# Install some additional packages using pip.
# These are packages that don't appear to be available in CONDA
/opt/conda/bin/pip3 install -r ${DIRECTORY}/requirements.txt