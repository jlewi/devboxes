#!/bin/bash -eu
#
# Downloads and install Conda
set -x

DL_ANACONDA_HOME="${DL_ANACONDA_HOME:-/opt/conda}"
# I think the python version here (python 3.9) is the version of Python used by conda itself.
# The environments created by CONDA can use a different version of python. That version
# gets set in install_to_env by the conda install command.
ANACONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh"

# Workaround for https://github.com/ContinuumIO/anaconda-issues/issues/11148
mkdir -p "/root/.conda"
ANACONDA_INSTALLER=anaconda_installer.sh
wget -q -nv "${ANACONDA_URL}" -O "${ANACONDA_INSTALLER}" 2>&1
chmod +x "${ANACONDA_INSTALLER}"
# Display Miniconda3 installer file information.
sed -n '3,7p' "${ANACONDA_INSTALLER}" 2>&1
"./${ANACONDA_INSTALLER}" -b -p "${DL_ANACONDA_HOME}"
rm "${ANACONDA_INSTALLER}"

# This will allow all users to install initially, but the cache will be
# user locked after.
chmod -R ugo+w "${DL_ANACONDA_HOME}"
# shellcheck disable=SC1090,SC1091
. "${DL_ANACONDA_HOME}/etc/profile.d/conda.sh"

if [[ ${NO_CONDA_AUTOUPDATE:-0} -gt 0 ]]; then
  echo "Pinning conda ..."
  conda config --file "${DL_ANACONDA_HOME}/.condarc" --set auto_update_conda false
  conda --version > "${DL_ANACONDA_HOME}"/conda-meta/pinned
fi

# Since packages are built on conda-forge, set conda-forge as primary channel
# to reduce conflicts.
conda config --file "${DL_ANACONDA_HOME}/.condarc" --add channels conda-forge

# Conda doesn't automatically create the pip -> pip3 symlink.
PIP3_SYMLINK_PATH="${DL_ANACONDA_HOME}/bin/pip3"
if [[ ! -f "${PIP3_SYMLINK_PATH}" ]]; then
  ln -s "${DL_ANACONDA_HOME}/bin/pip" "${PIP3_SYMLINK_PATH}"
else
  echo "A file already exists at ${PIP3_SYMLINK_PATH}."
  if [[ -L "${PIP3_SYMLINK_PATH}" && -d "${PIP3_SYMLINK_PATH}" ]]; then
    echo "The file is a symlink that points to $(readlink "${PIP3_SYMLINK_PATH}")"
  fi
fi
set +x
