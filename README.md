# Global Semiconductor Industry ELT Pipeline

An ELT pipeline that ingests the [Global Semiconductor Industry (2010–2026)](https://www.kaggle.com/datasets/sergionefedov/global-semiconductor-industry-2010-2026) dataset from Kaggle into a Google Cloud Storage data lake and BigQuery data warehouse, then transforms it into analytics-ready models with dbt.

## Prerequisites

- Docker
- Terraform
- `gcloud` CLI
- `uv`
- `pre-commit`

## Quick start

1. Provision the GCP infrastructure:

   ```sh
   # Fill in at least `project` and `gcs_bucket_name` in terraform.tfvars.
   cd terraform
   cp terraform.tfvars.example terraform.tfvars

   # Create the bucket that stores remote Terraform state,
   # then set that name as the `bucket` value in the `backend "gcs"` block
   # at the top of main.tf.
   gcloud storage buckets create gs://<your-state-bucket> --location=EU

   # -migrate-state moves any existing local terraform.tfstate into GCS.
   terraform init -migrate-state
   terraform apply

   # The created bucket and dataset names are exposed as Terraform outputs.
   terraform output
   ```

2. Authenticate with Application Default Credentials:

   ```sh
   gcloud auth application-default login
   ```

3. Configure and start Kestra:

   Create a `.env` file at the repo root with the following variables set:

   ```sh
   POSTGRES_DB=<database-name>
   POSTGRES_USER=<postgres-user>
   POSTGRES_PASSWORD=<postgres-password>

   KESTRA_BASIC_AUTH_USERNAME=<username> # Must be an email address
   KESTRA_BASIC_AUTH_PASSWORD=<password>
   ```

   Docker:

   ```sh
   docker compose up -d
   docker build -t kestra-semiconductor:latest .
   ```

4. Import the flows:

   ```sh
   set -a; source .env; set +a

   curl -X POST -u "$KESTRA_BASIC_AUTH_USERNAME:$KESTRA_BASIC_AUTH_PASSWORD" \
     http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/01_gcp_kv.yaml

   curl -X POST -u "$KESTRA_BASIC_AUTH_USERNAME:$KESTRA_BASIC_AUTH_PASSWORD" \
     http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_gcp_ingest.yaml
   ```

5. Set the config and run the pipeline from the Kestra UI (http://localhost:8080):

   1. Set the config: open **Flows → semiconductor → 01_gcp_kv** and click
      **New execution**. Fill in `gcp_project_id` and `gcp_bucket_name` (leave
      `gcp_location` and `gcp_dataset` on their defaults unless you changed
      them), then click **Execute**. This writes the GCP config to the KV store.

   2. Run the pipeline: open **Flows → semiconductor → 02_gcp_ingest** and
      click **New execution → Execute**.

6. Install and configure dbt

   ```sh
   # install dbt (kept out of the Kestra Docker image)
   uv sync --group dbt

   # create your local profile (uses your existing Application Default Credentials)
   cd dbt
   cp profiles.yml.example profiles.yml

   # must match the gcp_project_id set in the Kestra KV store
   export GCP_PROJECT_ID=<your-project>

   # no `dbt deps` step — the project uses no packages
   uv run --group dbt dbt build --profiles-dir .
   uv run --group dbt dbt docs generate --profiles-dir .
   uv run --group dbt dbt docs serve --profiles-dir .
   cd ..
   ```

   The dataset is hardcoded to `global_semiconductor_industry` in
   `profiles.yml.example` and `models/staging/sources.yml` — keep it aligned with
   `bq_dataset_name` in `terraform/variables.tf` if you change that default.

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
