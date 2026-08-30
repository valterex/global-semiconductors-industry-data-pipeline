# Data Pipeline — Semiconductor Industry

An ELT pipeline that ingests the [Global Semiconductor Industry (2010–2026)](https://www.kaggle.com/datasets/sergionefedov/global-semiconductor-industry-2010-2026) dataset from Kaggle into a Google Cloud Storage data lake and BigQuery.

## Architecture

| Component | Role |
|---|---|
| Terraform | Provisions the GCS bucket and BigQuery dataset |
| Kestra | Orchestrates extract (`kagglehub`) → upload to GCS → load into BigQuery |
| Docker Compose | Runs Kestra and its Postgres backend locally |

## Prerequisites

- Docker
- Terraform
- `gcloud` CLI

## Quick start

1. Provision the GCP infrastructure:

   ```sh
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   terraform init
   terraform apply
   ```

2. Authenticate with Application Default Credentials (no service account key):

   ```sh
   gcloud auth application-default login
   ```

3. Configure and start Kestra:

   ```sh
   cp .env.example .env
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

## Configuration

- `terraform/terraform.tfvars` — GCP project ID and bucket name (gitignored).
- `.env` — Postgres and web UI credentials
- `flows/01_gcp_kv.yaml` — KV values; project ID and bucket name are supplied as flow inputs.

## Cleanup

```sh
cd terraform && terraform destroy
```

## Linting

```sh
uv sync
pre-commit run --all-files
```
