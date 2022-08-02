#!/bin/bash
# Update the base image to the latest built image.
set -x

ROOT=$(git rev-parse --show-toplevel)


NEWBASE=$(yq e ".builds[0].tag" ${ROOT}/dlbase/.build/image.json) 

yq e ".build.artifacts[0].kaniko.buildArgs.BASE_IMAGE = \"${NEWBASE}\"" -i ${ROOT}/vscode/skaffold.yaml

cd ${ROOT}/dlbase/testpod/
kustomize edit set image base-cpu=${NEWBASE}