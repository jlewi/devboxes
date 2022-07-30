"""AI Notebooks Jupyter Service configuration file."""

import logging
import os
import sys
import requests
from requests.adapters import HTTPAdapter
from jupyter_client import kernelspec

# pylint: disable=anomalous-backslash-in-string, line-too-long, undefined-variable
c.NotebookApp.open_browser = False
c.ServerApp.token = ""
c.ServerApp.password = ""
c.ServerApp.port = 8080
c.ServerApp.allow_origin_pat = "(^https://8080-dot-[0-9]+-dot-devshell\.appspot\.com$)|(^https://colab\.research\.google\.com$)|((https?://)?[0-9a-z]+-dot-datalab-vm[\-0-9a-z]*\.googleusercontent\.com)|((https?://)?[0-9a-z]+-dot-[\-0-9a-z]*\.notebooks\.googleusercontent\.com)|((https?://)?[0-9a-z\-]+\.[0-9a-z\-]+\.cloudshell\.dev)|((https?://)ssh\.cloud\.google\.com/devshell)"
c.ServerApp.allow_remote_access = True
c.ServerApp.disable_check_xsrf = False
c.ServerApp.notebook_dir = "/home/jupyter"
# pylint: enable=anomalous-backslash-in-string, line-too-long, undefined-variable

BASE_PATH = "/opt/deeplearning/metadata/"
MAX_RETRIES = 2
METADATA_URL = "http://metadata/computeMetadata/v1"
METADATA_FLAVOR = {"Metadata-Flavor": "Google"}


def _get_session(prefix="http://", max_retries=MAX_RETRIES):
  """Return an HTTP Session.

  Args:
    prefix(str): Prefix for URL
    max_retries(int): Maximum number of retries each connection should attempt.

  Returns:
    A requests.Session()
  """
  session = requests.Session()
  session.mount(prefix, HTTPAdapter(max_retries=max_retries))
  return session


def get_jupyter_user():
  """Get default Jupyter user."""
  jupyter_user = "jupyter"
  if get_attribute_value("jupyter-user"):
    jupyter_user = get_attribute_value("jupyter-user")
  return jupyter_user


def get_attribute_value(attribute):
  """Get Metadata value.

  Args:
    attribute(str): Attribute key to look in Compute Metadata.

  Returns:
    Attribute value or None
  """
  if attribute is None:
    raise ValueError("Invalid attribute. Attribute is None")
  try:
    session = _get_session(max_retries=5)
    response = session.get(
      f"{METADATA_URL}/instance/attributes/{attribute}",
      headers=METADATA_FLAVOR,
    )
    response.raise_for_status()
    print(f"Metadata {attribute}:{response.text}")
    return response.text
  except requests.exceptions.HTTPError as err:
    if err.response.status_code == 404:
      print(err)
  return None


def handle_attribute_value(attribute_value):
  """If attribute value exists, check if its true or false."""
  if attribute_value is None or attribute_value == "":
    return False
  if attribute_value.lower() == "true":
    return True
  return False


def _disable_downloads():
  """Disable file downloads from JupyterLab.

  Handlers are created at startup time.
  """
  jupyter_user = get_jupyter_user()
  jupyter_home = f"/home/{jupyter_user}"
  sys.path.append(f"{jupyter_home}/.jupyter/")
  # pylint: disable=unused-import,import-outside-toplevel,undefined-variable
  import handlers
  c.ContentsManager.files_handler_class = 'handlers.ForbidFilesHandler'
  c.ContentsManager.files_handler_params = {}
  # Prevent export/printing of calculated values that likely have PII
  c.TemplateExporter.exclude_input_prompt = True
  c.TemplateExporter.exclude_output = True
  # pylint: enable=unused-import,import-outside-toplevel,undefined-variable

def read_from_file(path):
  """Read metadata file.

  Args:
    path(str) Location of file with metadata information.

  Returns:
    A string.
  """
  with open(path, "r", encoding="utf-8") as file:
    return file.read().replace("\n", "")


def get_env_name():
  return read_from_file(os.path.join(BASE_PATH, "env_version"))


def get_env_uri():
  return read_from_file(os.path.join(BASE_PATH, "env_uri"))


local_kernelspec_cache = {}
def metadata_env_pre_save(model, **kwargs):  # pylint: disable=unused-argument
  """Save metadata from Jupyter Environment.

  Args:
    model(dict): Notebooks information
  """

  try:
    # only run on notebooks
    if model["type"] != "notebook":
      return
    # only run on nbformat v4 or later
    if model["content"]["nbformat"] < 4:
      return
    model_metadata = model["content"]["metadata"]
    if "kernelspec" in model_metadata:
      kernel = model_metadata["kernelspec"]["name"]
      # remote kernels have no compatible container at the moment
      if kernel.startswith("remote-"):
        del model_metadata["kernelspec"]
        model_metadata["environment"] = {
            "type": "gcloud",
            "name": get_env_name(),
        }
        return
      # local kernels will have the local prefix in managed notebooks
      if kernel.startswith("local-"):
        kernel = kernel.split("-", 1)[1]
        if kernel not in local_kernelspec_cache:
          for k in kernelspec.find_kernel_specs():
            local_kernelspec_cache[k] = kernelspec.get_kernel_spec(k)
        kernel_metadata = local_kernelspec_cache[kernel].metadata
        model_metadata["environment"] = {
            "type": "gcloud",
            "name": get_env_name(),
            "uri": kernel_metadata["google.kernel_container"],
            # local name may not match kernel name on container
            "kernel": kernel_metadata["google.kernel_name"],
        }
        return
      # non-managed notebooks should have correct kernelspec listed
      model_metadata["environment"] = {
          "type": "gcloud",
          "name": get_env_name(),
          "uri": get_env_uri(),
          "kernel": kernel,
      }
  # pylint: disable=broad-except
  except (FileNotFoundError, KeyError, OSError, Exception) as e:
    logging.error("Failed to enrich the Notebook with metadata: %s", e)

# pylint: disable=undefined-variable
c.FileContentsManager.pre_save_hook = metadata_env_pre_save

# https://jupyterlab.readthedocs.io/en/stable/user/rtc.html
use_collaborative = get_attribute_value('use-collaborative')
if handle_attribute_value(use_collaborative):
  print('Using JupyterLab Collaborative flag')
  c.LabApp.collaborative = True

disable_downloads = get_attribute_value('notebook-disable-downloads')
if handle_attribute_value(disable_downloads):
  _disable_downloads()

disable_terminal = get_attribute_value('notebook-disable-terminal')
if handle_attribute_value(disable_terminal):
  c.NotebookApp.terminals_enabled = False

c.FileContentsManager.delete_to_trash = False
delete_to_trash = get_attribute_value('notebook-enable-delete-to-trash')
if handle_attribute_value(delete_to_trash):
  c.FileContentsManager.delete_to_trash = True

# Additional scripts append Jupyter configuration. Please keep this line.
