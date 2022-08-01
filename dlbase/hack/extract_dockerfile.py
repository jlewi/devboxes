"""This script is intended to try to reverse engineer the Dockerfile used in an image.

We can use gcrane config to output information about a docker image

e.g 
gcrane config gcr.io/dev-bytetoko/devbox@sha256:ead81fd81e48c876c91b3561a87943ce6493ba9abe8747cf8dc2d4dffdeffd58 > ~/tmp/config.json

The history contains most of the information needed to get a Dockerfile.
This script just prints the information in a way that's easy to copy
and paste into a Dockerfile
"""

import json

if __name__ == "__main__":
    file = "/Users/jlewi/tmp/config.json"
    with open(file) as handle:
        contents = json.load(handle)

    for c in contents["history"]:
        print(c["created_by"])