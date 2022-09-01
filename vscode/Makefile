# IMG is the base path for images..
# Individual images will be
# $(IMG)/$(NAME):$(TAG)
CONTEXT=label-bot-dev

PROJECT ?= dev-bytetoko
IMG ?= gcr.io/${PROJECT}/de

# Use the hacked version of skaffold to try to debug the build.
SKAFFOLD ?= /Users/jlewi/git_skaffold/out/skaffold

.PHONY: build
build-dir: 
	mkdir  -p ./.build

build: build-dir
	# Enable debug logs to try to figure out what's causing 
	# error copying logs to stdout: invalid write result
	$(SKAFFOLD) build -v debug --timestamps=true  --file-output .build/image.json
	NEWIMAGE=$$(yq e ".builds[0].tag" .build/image.json) && \
		echo Built $${NEWIMAGE}

build-gcb: build-dir	
	gcloud builds submit --machine-type=n1-highcpu-32 --project=$(PROJECT) --tag=$(IMG):$(TAG) \
		--timeout=3600 ./.build
	echo Built $(IMG):$(TAG)

get-image:
	NEWIMAGE=$$(yq e ".builds[0].tag" .build/image.json) && \
		echo Built $${NEWIMAGE}

set-image:
  # $$ escapes the $ so that Make doesn't do the substitution but differs it to the sheel
	NEWIMAGE=$$(yq e ".builds[0].tag" .build/image.json) && \
	kustomize edit set image tensorflow=$${NEWIMAGE}

update-image: build set-image

hydrate:
	rm -rf  .build/hydrated
	mkdir -p .build/hydrated
	kustomize build -o .build/hydrated .

apply: hydrate
	kubectl apply -f .build/hydrated

update-pod: update-image apply

# TODO(jeremy): How can we do a better job of filtering this?
cleanup:
	kubectl -n boxes delete statefulsets jlewi-box