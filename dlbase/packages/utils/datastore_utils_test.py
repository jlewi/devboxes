""" This file tests packages/utils/datastore_utils.py
"""

import unittest
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch
from common import db_constants
from packages.utils import datastore_utils


SAMPLE_PACKAGE_SET_RECORD = {
    "key": (db_constants.PACKAGE_SETS_KIND, "package_set_1"),
    db_constants.CREATION_TIME_KEY: "2021-03-17",
    db_constants.COMMIT_KEY: "1234567",
    db_constants.FRAMEWORKS_KEY: "pytorch,tf",
    db_constants.STATUS_KEY: db_constants.BUILD_STATUS_RUNNING
}
SAMPLE_PACKAGE_SET_RECORD_2 = {
    "key": (db_constants.PACKAGE_SETS_KIND, "package_set_2"),
    db_constants.CREATION_TIME_KEY: "2021-04-18",
    db_constants.COMMIT_KEY: "5555555",
    db_constants.FRAMEWORKS_KEY: "tf",
    db_constants.STATUS_KEY: db_constants.BUILD_STATUS_SUCCEEDED
}
EXPECTED_SUCCEEDED_PACKAGE_SET_RECORD = {
    "key": (db_constants.PACKAGE_SETS_KIND, "package_set_1"),
    db_constants.CREATION_TIME_KEY: "2021-03-17",
    db_constants.COMMIT_KEY: "1234567",
    db_constants.FRAMEWORKS_KEY: "pytorch,tf",
    db_constants.STATUS_KEY: db_constants.BUILD_STATUS_SUCCEEDED
}


class DatastoreUtilsTest(unittest.TestCase):

  def setUp(self):
    self.mock_client = patch(
        "packages.utils.datastore_utils.datastore.Client").start()
    # Allow for mocking the datastore client's instance
    self.mock_client.return_value = self.mock_client

    # We need to mock the key and entity into an object that can be compared
    def mock_key(kind, kind_id):
      return (kind, kind_id)

    def mock_entity(key):
      return {
          "key": key
      }
    self.mock_client.key = mock_key
    patch(
        "packages.utils.datastore_utils.datastore.Entity",
        new=mock_entity).start()

    mock_datetime = MagicMock()
    mock_datetime.utcnow.return_value = "2022-02-02"
    patch("packages.utils.datastore_utils.datetime.datetime",
          new=mock_datetime).start()

  def tearDown(self):
    patch.stopall()

  @patch("packages.utils.datastore_utils._query_latest_nightly_package_set")
  def test_get_latest_nightly_package_set_name(self, mock_query):
    # Test date provided
    mock_record = MagicMock()
    mock_query.return_value = mock_record

    mock_record.key.name = "package_set_1"
    self.assertEqual(
        "package_set_1",
        datastore_utils.get_latest_nightly_package_set_name("2021-01-01"))
    mock_query.assert_called_with(date="2021-01-01")

    mock_query.reset_mock()

    # Test default datetime fallback
    mock_record.key.name = "package_set_2"
    self.assertEqual(
        "package_set_2",
        datastore_utils.get_latest_nightly_package_set_name())
    mock_query.assert_called_with(date="2022-02-02")

  def test_add_package_set_to_db_nightlycase(self):
    with patch("packages.utils.datastore_utils._get_package_set_record",
               return_value=None):
      datastore_utils.add_package_set_to_db(
          package_set_name="nightly-yyyy-mm-dd",
          commit="12345",
          frameworks="tf,frameworks"
      )
      self.mock_client.put.assert_called_with({
          "key": (db_constants.PACKAGE_SETS_KIND, "nightly-yyyy-mm-dd"),
          db_constants.CREATION_TIME_KEY: "2022-02-02",
          db_constants.COMMIT_KEY: "12345",
          db_constants.FRAMEWORKS_KEY: "frameworks,tf",
          db_constants.STATUS_KEY: db_constants.BUILD_STATUS_RUNNING,
          db_constants.IS_NIGHTLY_BUILD: True})

  def test_add_package_set_to_db_nonnightlycase(self):
    with patch("packages.utils.datastore_utils._get_package_set_record",
               return_value=None):
      datastore_utils.add_package_set_to_db(
          package_set_name="package_set1",
          commit="12345",
          frameworks="tf,frameworks"
      )
      self.mock_client.put.assert_called_with({
          "key": (db_constants.PACKAGE_SETS_KIND, "package_set1"),
          db_constants.CREATION_TIME_KEY: "2022-02-02",
          db_constants.COMMIT_KEY: "12345",
          db_constants.FRAMEWORKS_KEY: "frameworks,tf",
          db_constants.STATUS_KEY: db_constants.BUILD_STATUS_RUNNING,
          db_constants.IS_NIGHTLY_BUILD: False})

  def test_set_package_set_status(self):
    with self.assertRaises(ValueError):
      datastore_utils.set_package_set_status(
          package_set_name="package_set1",
          status="invalid status"
      )
      self.mock_client.put.assert_not_called()

    with patch("packages.utils.datastore_utils._get_package_set_record",
               return_value=SAMPLE_PACKAGE_SET_RECORD):
      datastore_utils.set_package_set_status(
          package_set_name="package_set1",
          status=db_constants.BUILD_STATUS_SUCCEEDED
      )
      self.mock_client.put.assert_called_with(
          EXPECTED_SUCCEEDED_PACKAGE_SET_RECORD
      )

  def test__query_latest_nightly_package_set(self):
    # pylint: disable=protected-access
    mock_query = MagicMock()
    self.mock_client.query.return_value = mock_query

    with patch("packages.utils.datastore_utils." +
               "config_utils.get_supported_packages", return_value=[
                   "base",
                   "tf/1-15",
                   "tf/2-1"
               ]):
      mock_query.fetch.return_value = iter([SAMPLE_PACKAGE_SET_RECORD])
      self.assertEqual(
          SAMPLE_PACKAGE_SET_RECORD,
          datastore_utils._query_latest_nightly_package_set(None))
      mock_query.add_filter.assert_has_calls(
          [
              call(db_constants.FRAMEWORKS_KEY, '=', "base,tf/1-15,tf/2-1"),
              call(db_constants.STATUS_KEY, '=',
                   db_constants.BUILD_STATUS_SUCCEEDED)
          ],
          any_order=True
      )
      self.assertEqual(mock_query.order, ["-creation_time"])

      mock_query.reset_mock()

      # Test with provided date and multiple fetched results.
      mock_query.fetch.return_value = iter(
          [SAMPLE_PACKAGE_SET_RECORD_2, SAMPLE_PACKAGE_SET_RECORD])
      self.assertEqual(
          SAMPLE_PACKAGE_SET_RECORD_2,
          datastore_utils._query_latest_nightly_package_set("2021-05-11"))
      mock_query.add_filter.assert_has_calls(
          [
              call(db_constants.FRAMEWORKS_KEY, '=', "base,tf/1-15,tf/2-1"),
              call(db_constants.STATUS_KEY, '=',
                   db_constants.BUILD_STATUS_SUCCEEDED),
              call(db_constants.CREATION_TIME_KEY, '<=', "2021-05-11")
          ],
          any_order=True
      )
      self.assertEqual(mock_query.order, ["-creation_time"])

  def test__get_package_set_record(self):
    # pylint: disable=protected-access
    self.mock_client.get.return_value = SAMPLE_PACKAGE_SET_RECORD
    self.assertEqual(
        SAMPLE_PACKAGE_SET_RECORD,
        datastore_utils._get_package_set_record("package_set1")
    )
    self.mock_client.get.assert_called_with(
        (db_constants.PACKAGE_SETS_KIND, "package_set1")
    )


unittest.main()
