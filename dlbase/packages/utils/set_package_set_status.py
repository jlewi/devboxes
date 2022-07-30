# Lint as: python3

import argparse

from packages.utils import datastore_utils


def main():
  parser = argparse.ArgumentParser(description="Set package set status.")
  parser.add_argument("--package-set-name", dest="package_set_name", required=True)
  parser.add_argument("--status", dest="status", required=True)

  args = parser.parse_args()

  datastore_utils.set_package_set_status(args.package_set_name, args.status)


if __name__ == "__main__":
  main()
