# IMG is the base path for images..
# Individual images will be
# $(IMG)/$(NAME):$(TAG)
CONTEXT=label-bot-dev

PROJECT ?= dev-bytetoko
IMG ?= gcr.io/${PROJECT}/vscode

.PHONY: build
build-dir: 
	mkdir  -p ./.build

build: build-dir
	skaffold build --file-output .build/image.json
	@echo Built $(IMG):latest
	@echo Built $(IMG):$(TAG)

build-gcb: build-dir	
	gcloud builds submit --machine-type=n1-highcpu-32 --project=$(PROJECT) --tag=$(IMG):$(TAG) \
		--timeout=3600 ./.build
	@echo Built $(IMG):$(TAG)

push: build
	docker push $(IMG):$(TAG) 
	docker push $(IMG):latest


apply:
	# TODO(jlewi): What's the best way to make sure the statefulset pod gets kicked?
	# should we delete it manually or could we add a unique annotation?
	kustomize build | kubectl --context=$(CONTEXT) apply -f -
	kubectl --context=$(CONTEXT) \
 		-n $(shell yq r Kptfile openAPI.definitions["io.k8s.cli.setters.namespace"].["x-k8s-cli"].setter.value) \
 		delete pods \
 		$(shell yq r Kptfile openAPI.definitions["io.k8s.cli.setters.name"].["x-k8s-cli"].setter.value)-0