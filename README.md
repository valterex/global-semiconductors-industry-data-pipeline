# Data Pipeline — Global Semiconductor Industry

ELT pipeline for the [Global Semiconductor Industry (2010–2026)](https://www.kaggle.com/datasets/sergionefedov/global-semiconductor-industry-2010-2026) Kaggle dataset.

```
Kaggle ──> GCS (data lake) ──> BigQuery (warehouse)
```

Stack: Airflow · GCS · BigQuery · Terraform · uv

## Prerequisites

- GCP service-account JSON at `airflow/secrets/service-account.json` (gitignored).
- Kaggle credentials in `~/.kaggle/kaggle.json` (mounted read-only into the scheduler).

## Run

```sh
# 1. Provision GCS + BigQuery
cd terraform && cp terraform.tfvars.example terraform.tfvars  # fill in values
terraform init && terraform apply

# 2. Start Airflow (webserver + scheduler + Postgres)
cd ../airflow && cp .env.example .env    # fill in values (set AIRFLOW_UID=$(id -u) on macOS)
docker compose up -d --build             # UI at http://localhost:8080

# 3. Register the GCP connection (one-time)
docker compose exec airflow-scheduler airflow connections add google_cloud_default \
  --conn-type google_cloud_platform \
  --conn-extra '{"extra__google_cloud_platform__key_path": "/opt/airflow/secrets/service-account.json"}'

# 4. Trigger the DAG
docker compose exec airflow-scheduler airflow dags trigger gcp_elt \
  --conf '{"project_id": "<your-gcp-project>"}'
```

Or trigger from the UI: **DAGs → gcp_elt → Trigger DAG w/ config** with `{"project_id": "..."}`.

The DAG (`airflow/dags/gcp_elt.py`) downloads the dataset, uploads each CSV to
GCS, then creates an external and a native BigQuery table per file. GCP auth
comes from the `google_cloud_default` connection; `project_id` is a DAG param.

## Lint

```sh
uv run ruff check airflow/dags
uv run ruff format --check airflow/dags
```

## Commit convention

Commits follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): description`, e.g. `feat: add ingestion flow`, `fix: handle empty files`, `chore: update deps`. A commitizen hook validates this — enable it once:

```sh
uv run pre-commit install --hook-type commit-msg
```
