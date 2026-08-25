import os
import shutil
from typing import cast

from prefect import flow, task
from prefect_gcp import BigQueryWarehouse, GcsBucket

from src.flows.common import DATASET_HANDLE, FILES, download_dataset


@task(
    retries=2,
    retry_delay_seconds=10,
    log_prints=True,
    task_run_name="upload-{file_name}",
)
def upload_to_gcs(
    file_name: str,
    local_path: str,
    bucket_block_name: str,
    gcs_folder: str,
) -> str:
    """Upload a single CSV to GCS and return its bucket object path."""
    path = f"{gcs_folder}/{file_name}"
    gcs = cast(GcsBucket, GcsBucket.load(bucket_block_name))
    gcs.upload_from_path(from_path=os.path.join(
        local_path, file_name), to_path=path)
    print(f"Uploaded {file_name} to gs://{gcs.bucket}/{path}")
    return path


@task(
    retries=2,
    retry_delay_seconds=10,
    log_prints=True,
    task_run_name="external-{file_name}",
)
def create_external_table(
    file_name: str,
    bucket_name: str,
    gcs_folder: str,
    warehouse_block_name: str,
    project_id: str,
    dataset: str,
) -> None:
    """Create a BigQuery external table pointing at a CSV in GCS."""
    bq = cast(BigQueryWarehouse, BigQueryWarehouse.load(warehouse_block_name))
    table = file_name.removesuffix(".csv")
    external_table = f"external_{table}"
    uri = f"gs://{bucket_name}/{gcs_folder}/{file_name}"

    ddl = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{project_id}.{dataset}.{external_table}`
        OPTIONS (
            format = 'CSV',
            uris = ['{uri}'],
            skip_leading_rows = 1,
            allow_quoted_newlines = true
        )
    """

    bq.execute(ddl)
    print(f"Created external table {dataset}.{external_table}")


@task(
    retries=2,
    retry_delay_seconds=10,
    log_prints=True,
    task_run_name="native-{file_name}",
)
def create_native_table(
    file_name: str,
    warehouse_block_name: str,
    project_id: str,
    dataset: str,
) -> None:
    """Materialize a native BigQuery table from the external table."""
    bq = cast(BigQueryWarehouse, BigQueryWarehouse.load(warehouse_block_name))
    table = file_name.removesuffix(".csv")
    external_table = f"external_{table}"

    ddl = f"""
        CREATE OR REPLACE TABLE `{project_id}.{dataset}.{table}` AS
        SELECT * FROM `{project_id}.{dataset}.{external_table}`
    """

    bq.execute(ddl)
    print(f"Created table {dataset}.{table}")


@task(log_prints=True, task_run_name="purge-files")
def purge_files(local_path: str) -> None:
    """Remove the locally downloaded dataset files."""
    shutil.rmtree(local_path, ignore_errors=True)
    print(f"Purged local files at {local_path}")


@flow(name="gcp-elt", log_prints=True)
def gcp_elt_flow(
    dataset_handle: str = DATASET_HANDLE,
    bucket_block_name: str = "semiconductor-data-lake",
    warehouse_block_name: str = "semiconductor-warehouse",
    bucket_name: str = "global_semiconductor_industry_bucket",
    project_id: str | None = None,
    dataset: str = "global_semiconductor_industry",
    gcs_folder: str = "raw",
) -> None:
    """Download the dataset, land it in GCS, and load it into BigQuery."""
    project_id = project_id or os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("project_id is required")

    local_path = download_dataset(dataset_handle)
    for future in upload_to_gcs.map(FILES, local_path, bucket_block_name, gcs_folder):
        future.wait()

    for file_name in FILES:
        create_external_table(
            file_name,
            bucket_name,
            gcs_folder,
            warehouse_block_name,
            project_id,
            dataset,
        )
        create_native_table(file_name, warehouse_block_name,
                            project_id, dataset)

    purge_files(local_path)


if __name__ == "__main__":
    gcp_elt_flow()
