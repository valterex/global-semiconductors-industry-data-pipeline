# Data Pipeline — Semiconductor Industry

An ELT pipeline that ingests the [Global Semiconductor Industry (2010–2026)](https://www.kaggle.com/datasets/sergionefedov/global-semiconductor-industry-2010-2026) dataset from Kaggle into a Google Cloud Storage data lake and BigQuery data warehouse.

## Prerequisites

- Docker
- Terraform
- `gcloud` CLI

## Quick start

1. Provision the GCP infrastructure:

   ```sh
   cd terraform
   cp terraform.tfvars.example terraform.tfvars

   # Create the bucket that stores remote Terraform state,
   # then set that name as the `bucket` value in the `backend "gcs"` block
   # at the top of main.tf.
   gcloud storage buckets create gs://<your-state-bucket> --location=EU

   # -migrate-state moves any existing local terraform.tfstate into GCS.
   terraform init -migrate-state
   terraform apply
   ```

2. Authenticate with Application Default Credentials:

   ```sh
   gcloud auth application-default login
   ```

3. Configure and start Kestra:

   Create a `.env` file at the repo root with the following variables set:

   ```sh
   POSTGRES_DB
   POSTGRES_USER
   POSTGRES_PASSWORD
   KESTRA_BASIC_AUTH_USERNAME
   KESTRA_BASIC_AUTH_PASSWORD
   ```

   Docker:

   ```sh
   docker compose up -d
   docker build -t kestra-semiconductor:latest .
   ```

4. Import and run the flows:

   ```sh
   set -a; source .env; set +a

   curl -X POST -u "$KESTRA_BASIC_AUTH_USERNAME:$KESTRA_BASIC_AUTH_PASSWORD" \
     http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/01_gcp_kv.yaml

   curl -X POST -u "$KESTRA_BASIC_AUTH_USERNAME:$KESTRA_BASIC_AUTH_PASSWORD" \
     http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_gcp_ingest.yaml

   # set the KV values
   curl -X POST -u "$KESTRA_BASIC_AUTH_USERNAME:$KESTRA_BASIC_AUTH_PASSWORD" \
     'http://localhost:8080/api/v1/executions/semiconductor/01_gcp_kv' \
     -H 'Content-Type: application/json' \
     -d '{"inputs":{"gcp_project_id":"<project>","gcp_bucket_name":"<bucket>"}}'

   # run the pipeline
   curl -X POST -u "$KESTRA_BASIC_AUTH_USERNAME:$KESTRA_BASIC_AUTH_PASSWORD" \
     'http://localhost:8080/api/v1/executions/semiconductor/02_gcp_ingest'
   ```

   Kestra UI: http://localhost:8080

## Cleanup

Deletion is intentionally protected: `terraform destroy` will fail if the GCS
bucket still holds data (`force_destroy = false`) or while the BigQuery dataset
still has tables (`delete_contents_on_destroy = false`). To tear everything
down, empty the bucket and set `delete_contents_on_destroy = true` in `main.tf`,
then run:

```sh
cd terraform && terraform destroy
```

## Linting

```sh
uv sync
pre-commit run --all-files
```
