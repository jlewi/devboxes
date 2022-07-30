"""Get the latest successfully built nightly package set.
"""

import argparse

from packages.utils import datastore_utils


def main():
  parser = argparse.ArgumentParser(
      description="Get latest nightly package set name.")

  parser.parse_args()

  return datastore_utils.get_latest_nightly_package_set_name()


if __name__ == "__main__":
  main()
