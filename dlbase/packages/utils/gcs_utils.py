""" A utilities file with functions to work with GCloud Storage
"""
from google.cloud import storage

CONDA_STORAGE_BUCKET_NAME = "deeplearning-platform-conda"


def conda_storage_bucket():
  """Returns the storage bucket that has our Conda packages.

  Returns:
      google.cloud.storage.bucket.Bucket: Storage bucket with conda packages.
  """
  return storage.Client(project="deeplearning-platform").get_bucket(
        CONDA_STORAGE_BUCKET_NAME)


def delete_prefix(bucket, prefix):
  """Deletes all the files in a bucket prefix.

  Args:
      bucket (storage.bucket.Bucket): The bucket to delete the prefix from.
      prefix (string): The relative prefix to delete in the bucket.
  """
  blobs = bucket.list_blobs(prefix=prefix)
  bucket.delete_blobs(list(blobs))


def prefix_exists(bucket, prefix):
  """Returns true if the bucket has an object with the provided prefix.

  Args:
      bucket (google.cloud.storage.bucket.Bucket): bucket to check
      prefix (string): prefix to check for an object

  Returns:
      bool: whether or not the object exists
  """
  blobs = bucket.list_blobs(prefix=prefix, max_results=1)
  for _ in blobs:
    return True
  return False
