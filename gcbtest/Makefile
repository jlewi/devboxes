build:
	gcloud builds submit --region=us-west2 \
		--tag gcr.io/dev-bytetoko/quickstart-image:tag1

skaffold:
	mkdir -p .build
	skaffold build -v info --timestamps=true --file-output .build/image.json			