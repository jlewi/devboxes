#!/bin/bash
# ENV_NAME is the conda environment, e.g. base
# PACKAGE_META should be in the form "dlenv-*-meta", which pins dependencies.
set -x

[[ -n  "${DL_ANACONDA_HOME}" ]] || { echo "DL_ANACONDA_HOME not set" && exit 1; }
[[ -n  "${CONDA_REPOSITORY}" ]] || { echo "CONDA_REPOSITORY not set" && exit 1; }
ANACONDA_PYTHON_VERSION="${ANACONDA_PYTHON_VERSION:-3.7}"

ENV_NAME=$1
PACKAGE_META=$2

if ! [[ "${PACKAGE_META}" =~ meta ]]; then
  echo "Package must be in the form dlenv-*-meta, for example dlenv-tf-1-15-cpu-meta."
  exit 1
fi

# shellcheck disable=SC1090,SC1091
. "${DL_ANACONDA_HOME}/etc/profile.d/conda.sh"

echo "Installing ${PACKAGE_META} to environment ${ENV_NAME}."
# Package name always in the form dlenv-<type>(-version), just get <type>
[[ "${PACKAGE_META}" =~ dlenv-([a-z]+) ]]
export PACKAGE_ROOT="${BASH_REMATCH[1]}"
# shellcheck disable=SC2207
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
# The base package must be explicitly installed, otherwise when a dependency
# is changed the package attempts to uninstall itself.
PACKAGE="${PACKAGE_META%-meta}"
conda install -y -c "${CONDA_REPOSITORY}" "${CHANNELS[@]}" \
  "python=${ANACONDA_PYTHON_VERSION}" \
  "${PACKAGE}" \
  "${PACKAGE_META}" \
  || { echo "Install of ${PACKAGE_META} failed." && exit 1; }
# Our metapackages pin exact versions. Remove so user can upgrade/downgrade packages
echo "Removing metapackage pins."
conda remove --force "${PACKAGE_META}"
conda clean -y -a

# Only update permissions on DLVM.
if [[ -z "${ENV_DOCKER}" ]]; then
  chmod -R ugo+w "${DL_ANACONDA_HOME}"
fi
