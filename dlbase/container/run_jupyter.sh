#!/bin/bash
if [[ -n "${NOTEBOOK_DISABLE_ROOT}" ]]; then
  /opt/conda/bin/jupyter lab --ip 0.0.0.0 --config=/opt/jupyter/.jupyter/jupyter_notebook_config.py
else
  /opt/conda/bin/jupyter lab --allow-root --ip 0.0.0.0 --config=/opt/jupyter/.jupyter/jupyter_notebook_config.py
fi