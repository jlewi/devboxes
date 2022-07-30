"""Gets metadata for license from datastore."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import sys

from google.cloud import datastore


_DATASTORE_CLIENT = datastore.Client(project="deeplearning-platform")
# These packages are installed in non-standard ways, so we manually need
# to acquire the licenses
_EXCLUDED_PATTERNS = [
    '-e git',  # manually installed from git repository
    'gcpscheduler',  # internal scheduler plugin
    'notebook-executor',  # custom Notebook executor package
    'explainers',  # internal package
    'explainable-ai-sdk',  # internal package
    'tensorflow-cloud',  # tensorflow_cloud package
    'cloud-tpu-client',  # internal tpu client
    'oauth2client',  # internal google oauth2 client lib.
    'google-jupyter-kernelmanager',  # internal custom kernel manager
    'google-cloud-*',  # google cloud packages
    'beatrix[_-]jupyterlab',  # internal managed jupyter extension
    'caip-notebooks-*',  # caip-notebooks extension:
                         # e.g.caip-notebooks-serverextension
    'absl-py',  # internal package
    'Keras', # internal package
    'ml-pipelines-sdk', # internal package
    'keyrings.google-artifactregistry-auth', # internal package
]
_EXCLUDED_PATTERNS_REGEX = [re.compile(pat) for pat in _EXCLUDED_PATTERNS]


def is_package_approved(package_name):
  """Checks if package has been approved by legal.

  Args:
    package_name: packages name.

  Returns:
    True if package approved, otherwise False.
  """
  task_key = _DATASTORE_CLIENT.key("license", package_name)
  license_raw = _DATASTORE_CLIENT.get(task_key)
  if license_raw:
    return license_raw["approved"]
  return False


def get_license_url_for_packages(package_name):
  """Gets license url from DB.

  Args:
    package_name: packages name.

  Returns:
    license's URL.
  """
  package_name_candidates = [package_name, package_name.replace('-', '_')]
  for name in package_name_candidates:
    task_key = _DATASTORE_CLIENT.key("license", name)
    license_raw = _DATASTORE_CLIENT.get(task_key)
    if license_raw:
      return license_raw["url"]

  return None


# Exits 0 if url found and package approved
#       1 if url not found or package not approved
#       2 if package matches exclusions above
def main():
  parser = argparse.ArgumentParser(
      description="Get license URL")
  parser.add_argument("--name", required=True)

  args = parser.parse_args()
  name = args.name.lower()
  for regex in _EXCLUDED_PATTERNS_REGEX:
    if regex.search(name):
       # pylint: disable=C0209
      print("package {} matches an excluded pattern, skipping".format(name))
      sys.exit(2)

  license_url = get_license_url_for_packages(name)
  error = ""
  if not license_url:
     # pylint: disable=C0209
    error = "package {} does not have the license".format(name)

  if error:
    print(error)
    sys.exit(1)

  print(license_url)
  sys.exit(0)


if __name__ == "__main__":
  main()
