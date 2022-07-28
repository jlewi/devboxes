# IMG is the base path for images..
# Individual images will be
# $(IMG)/$(NAME):$(TAG)
CONTEXT=label-bot-dev

PROJECT ?= dev-bytetoko
IMG ?= gcr.io/${PROJECT}/de

.PHONY: build
build-dir: 
	mkdir  -p ./.build

build: build-dir
	skaffold build --timestamps=true -v info  --file-output .build/image.json
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

update-pod: update-image
	kustomize build | kubectl apply -f -