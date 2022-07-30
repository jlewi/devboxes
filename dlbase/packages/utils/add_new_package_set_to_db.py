# Lint as: python3

import argparse

from packages.utils import datastore_utils


def main():
  parser = argparse.ArgumentParser(description="Create package set record")
  parser.add_argument("--package-set-name", dest="package_set_name", required=True)
  parser.add_argument("--commit", dest="commit", required=True)
  parser.add_argument("--frameworks", dest="frameworks", required=True)

  args = parser.parse_args()

  datastore_utils.add_package_set_to_db(args.package_set_name,
                                        args.commit,
                                        args.frameworks)


if __name__ == "__main__":
  main()
