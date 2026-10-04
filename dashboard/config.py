import os


def gcp_config() -> tuple[str | None, str | None]:
    return os.environ.get("GCP_PROJECT_ID"), os.environ.get("GCP_DATASET")
