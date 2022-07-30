#!/bin/bash
if [[ -x "/init.sh" ]]; then
  /init.sh
fi
. "${DL_ANACONDA_HOME}/etc/profile.d/conda.sh"
conda activate base
exec "$@"