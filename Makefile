create-cluster:
	gcloud --project=dev-bytetoko container clusters create-auto dev \
		--region=us-west1

# create the GCP service account for the kaniko namespace
kaniko-gsa:
	gcloud iam service-accounts create kaniko \
	    --project=dev-bytetoko

kaniko-gsa-roles:
	gcloud projects add-iam-policy-binding dev-bytetoko \
	    --member "serviceAccount:kaniko@dev-bytetoko.iam.gserviceaccount.com" \
	    --role "roles/storage.objectAdmin" \
	    --role "roles/storage.admin" \ 
	gcloud iam service-accounts add-iam-policy-binding kaniko@dev-bytetoko.iam.gserviceaccount.com \
    	--role roles/iam.workloadIdentityUser \
	    --member "serviceAccount:dev-bytetoko.svc.id.goog[kaniko/kaniko]"