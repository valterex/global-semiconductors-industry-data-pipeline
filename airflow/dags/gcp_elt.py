"""Airflow DAG: Kaggle -> GCS -> BigQuery ELT for the semiconductor dataset."""

import shutil
from datetime import datetime, timedelta

import kagglehub
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.hooks.gcs import GCSHook

FILES = [
    "ai_chip_market.csv",
    "chip_prices.csv",
    "export_controls.csv",
    "fab_capacity.csv",
    "chip_companies_financials.csv",
]

DATASET_HANDLE = "sergionefedov/global-semiconductor-industry-2010-2026"
GCS_BUCKET = "global_semiconductor_industry_bucket"
GCS_FOLDER = "raw"
BQ_DATASET = "global_semiconductor_industry"
CONN_ID = "google_cloud_default"


@dag(
    dag_id="gcp_elt",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(seconds=10),
    },
    params={"project_id": ""},
    tags=["semiconductor"],
)
def gcp_elt() -> None:
    @task(retries=3, retry_delay=timedelta(seconds=30))
    def download_dataset() -> str:
        return kagglehub.dataset_download(DATASET_HANDLE)

    @task
    def upload_to_gcs(file_name: str, local_path: str) -> str:
        object_name = f"{GCS_FOLDER}/{file_name}"
        GCSHook(gcp_conn_id=CONN_ID).upload(
            bucket_name=GCS_BUCKET,
            object_name=object_name,
            filename=f"{local_path}/{file_name}",
        )
        return object_name

    @task
    def create_external_table(file_name: str) -> None:
        project_id = get_current_context()["params"]["project_id"]
        if not project_id:
            raise ValueError(
                'Missing project_id: trigger the DAG with {"project_id": "..."}'
            )
        table = file_name.removesuffix(".csv")
        uri = f"gs://{GCS_BUCKET}/{GCS_FOLDER}/{file_name}"
        ddl = (
            f"CREATE OR REPLACE EXTERNAL TABLE "
            f"`{project_id}.{BQ_DATASET}.external_{table}` "
            f"OPTIONS (format='CSV', uris=['{uri}'], skip_leading_rows=1, "
            f"allow_quoted_newlines=true)"
        )
        BigQueryHook(gcp_conn_id=CONN_ID, use_legacy_sql=False).run_query(sql=ddl)

    @task
    def create_native_table(file_name: str) -> None:
        project_id = get_current_context()["params"]["project_id"]
        if not project_id:
            raise ValueError(
                'Missing project_id: trigger the DAG with {"project_id": "..."}'
            )
        table = file_name.removesuffix(".csv")
        ddl = (
            f"CREATE OR REPLACE TABLE `{project_id}.{BQ_DATASET}.{table}` AS "
            f"SELECT * FROM `{project_id}.{BQ_DATASET}.external_{table}`"
        )
        BigQueryHook(gcp_conn_id=CONN_ID, use_legacy_sql=False).run_query(sql=ddl)

    @task
    def purge_files(local_path: str) -> None:
        shutil.rmtree(local_path, ignore_errors=True)

    local_path = download_dataset()
    uploads = upload_to_gcs.partial(local_path=local_path).expand(file_name=FILES)
    externals = create_external_table.expand(file_name=FILES)
    natives = create_native_table.expand(file_name=FILES)
    purge = purge_files(local_path)

    uploads >> externals >> natives >> purge


gcp_elt()
