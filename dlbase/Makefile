# Use the hacked version of skaffold to try to debug the build.
SKAFFOLD ?= /Users/jlewi/git_skaffold/out/skaffold
.PHONY: build
build-dir: 
	mkdir  -p ./.build

build: build-dir
	# Enable debug logs to try to figure out what's causing 
	# error copying logs to stdout: invalid write result
	$(SKAFFOLD) build -v info --timestamps=true  --file-output .build/image.json

# update the base image in the vscode image
update-image: build
	./set_image.sh

# Deploy the testpod
apply:
	kustomize build testpod | kubectl apply -f -