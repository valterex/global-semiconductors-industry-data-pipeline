import kagglehub
from prefect import task
from prefect.tasks import task_input_hash

FILES = [
    "ai_chip_market.csv",
    "chip_prices.csv",
    "export_controls.csv",
    "fab_capacity.csv",
    "chip_companies_financials.csv",
]
DATASET_HANDLE = "sergionefedov/global-semiconductor-industry-2010-2026"


@task(
    retries=3,
    retry_delay_seconds=30,
    log_prints=True,
    cache_key_fn=task_input_hash,
    task_run_name="download-dataset",
)
def download_dataset(handle: str) -> str:
    return kagglehub.dataset_download(handle)
