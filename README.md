# Data Pipeline — Global Semiconductor Industry

ELT pipeline for the [Global Semiconductor Industry (2010–2026)](https://www.kaggle.com/datasets/sergionefedov/global-semiconductor-industry-2010-2026) Kaggle dataset.

```
Kaggle ──> GCS (data lake) ──> BigQuery (warehouse)
```

## Run

```sh
# 1. Provision GCS + BigQuery
cd terraform && cp terraform.tfvars.example terraform.tfvars  # fill in values
terraform init && terraform apply

# 2. Start Prefect server + worker
cd .. && cp .env.example .env               
docker compose up -d --build                  # UI at http://localhost:4200

# 3. Create GCP blocks
export PREFECT_API_URL=http://localhost:4200/api
export GCP_PROJECT_ID=<project> GCP_SERVICE_ACCOUNT_FILE=<path-to-sa.json>
uv run python scripts/create_gcp_blocks.py

# 4. Deploy + run
prefect deploy --all
prefect deployment run gcp-elt/gcp-elt --param project_id=<project>
```

## Lint & type-check

```sh
uv run ruff check src scripts
uv run ruff format --check src scripts
uv run pyright
```

## Commit convention

Commits follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): description`, e.g. `feat: add ingestion flow`, `fix: handle empty files`, `chore: update deps`. A commitizen hook validates this — enable it once:

```sh
uv run pre-commit install --hook-type commit-msg
```
