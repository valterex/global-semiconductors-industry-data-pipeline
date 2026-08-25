import json
import os
from pathlib import Path

from prefect_gcp import BigQueryWarehouse, GcpCredentials, GcsBucket


def main() -> None:
    service_account_file = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
    project_id = os.getenv("GCP_PROJECT_ID")

    if not service_account_file:
        raise ValueError("GCP_SERVICE_ACCOUNT_FILE is not set")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID is not set")

    service_account_info = json.loads(Path(service_account_file).read_text())

    credentials = GcpCredentials(
        service_account_info=service_account_info,
        project=project_id,
    )
    credentials.save("semiconductor-credentials", overwrite=True)

    bucket_name = os.getenv(
        "GCP_BUCKET_NAME", "global_semiconductor_industry_bucket")

    GcsBucket(
        bucket=bucket_name,
        gcp_credentials=credentials,
    ).save("semiconductor-data-lake", overwrite=True)

    BigQueryWarehouse(
        gcp_credentials=credentials,
    ).save("semiconductor-warehouse", overwrite=True)

    print(
        "Created blocks: semiconductor-credentials, semiconductor-data-lake, semiconductor-warehouse"
    )


if __name__ == "__main__":
    main()
