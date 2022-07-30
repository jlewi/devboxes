"""Helper utils for packages logic.

TODO: refactor the utils for packages/images/containers logic so there is less
repeated code.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import logging

from google.cloud import datastore

from common import config_utils
from common import constants
from common import db_constants


logger = logging.getLogger(__name__)


def get_latest_nightly_package_set_name(date=None):
  """Gets the name of the latest package set successfully built before or on a
  certain date. If no date is provided, use the current date.

  Args:
    date (optional): defaults to current date.

  Returns:
    (String) package set name.
  """
  if not date:
    date = datetime.datetime.utcnow()

  record = _query_latest_nightly_package_set(date=date)
  print(record.key.name)

  return record.key.name


def add_package_set_to_db(package_set_name, commit, frameworks):
  """Adds a new entry for the package set in the database.

  Args:
    package_set_name: package set name.
    commit: commit SHA tag used to build the package set.
    frameworks: list of frameworks included in the package set.
  """
  datastore_client = datastore.Client(project="deeplearning-platform")
  kind = db_constants.PACKAGE_SETS_KIND
  task_key = datastore_client.key(kind, package_set_name)

  frameworks_list = ",".join(sorted(frameworks.split(",")))

  if _get_package_set_record(package_set_name):
    warning_msg = (f"Warning: {package_set_name} already exists as a package "
                   f"set in the database. Overwriting...")
    print(warning_msg)

  # Prepares the new entity
  task = datastore.Entity(key=task_key)
  task[db_constants.CREATION_TIME_KEY] = datetime.datetime.utcnow()
  task[db_constants.COMMIT_KEY] = commit
  task[db_constants.FRAMEWORKS_KEY] = frameworks_list
  task[db_constants.STATUS_KEY] = db_constants.BUILD_STATUS_RUNNING
  task[db_constants.IS_NIGHTLY_BUILD] = package_set_name.startswith("nightly-")

  # Saves the entity
  datastore_client.put(task)


def set_package_set_status(package_set_name, status):
  """Sets the build status of the package set in the database.

  Args:
    package_set_name: package set name.
    status: job status.
  """
  if status not in constants.VALID_JOB_STATUSES:
    raise ValueError(f"invalid status {status} given. "
                     f"Valid statuses: {constants.VALID_JOB_STATUSES}")

  datastore_client = datastore.Client(project="deeplearning-platform")
  with datastore_client.transaction():
    task = _get_package_set_record(package_set_name)
    task[db_constants.STATUS_KEY] = status
    datastore_client.put(task)


def _query_latest_nightly_package_set(date):
  """Returns the latest successful nightly package set created before or during
  the listed date in reverse chronological order. If no date is provided, uses
  the current date.

  Args:
    date: the cutoff for package set creation dates.

  Returns:
    (<datastore record>) most recent package set
  """
  datastore_client = datastore.Client(project="deeplearning-platform")

  query = datastore_client.query(kind=db_constants.PACKAGE_SETS_KIND)
  # TODO: there's a catch here, since technically the package frameworks list
  # can be a superset of the DLVMs images' needs. The long term solution will
  # most likely involve looping to build a complex Datastore query to check
  # if each individual framework is present.
  supported_packages = config_utils.get_supported_packages()
  query.add_filter(db_constants.FRAMEWORKS_KEY, '=',
                   ",".join(sorted(supported_packages)))
  query.add_filter(db_constants.STATUS_KEY, '=',
                   db_constants.BUILD_STATUS_SUCCEEDED)
  query.add_filter(db_constants.IS_NIGHTLY_BUILD, '=', True)

  if date:
    query.add_filter(db_constants.CREATION_TIME_KEY, '<=', date)
  query.order = [f"-{db_constants.CREATION_TIME_KEY}"]
  latest = list(query.fetch(limit=1))[0]

  return latest


def _get_package_set_record(package_set_name):
  """Gets package set record from DB.

  Args:
    package_set_name: package set name.

  Returns:
    Datastore record with the package set's data.
  """
  datastore_client = datastore.Client(project="deeplearning-platform")
  task_key = datastore_client.key(db_constants.PACKAGE_SETS_KIND,
                                  package_set_name)

  return datastore_client.get(task_key)
