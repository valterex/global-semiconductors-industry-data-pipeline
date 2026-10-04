import pandas as pd
from google.cloud import bigquery


def get_client(project: str) -> bigquery.Client:
    return bigquery.Client(project=project)


def build_ai_chip_revenue_query(project: str, dataset: str) -> str:
    return (
        "select vendor, year, estimated_revenue_usd_m "
        f"from `{project}.{dataset}.fct_ai_chip_revenue_yearly`"
    )


def build_export_controls_query(project: str, dataset: str) -> str:
    return (
        "select year, administration, actions "
        f"from `{project}.{dataset}.fct_export_controls_yearly`"
    )


def load_ai_chip_revenue(
    client: bigquery.Client, project: str, dataset: str
) -> pd.DataFrame:
    return client.query(build_ai_chip_revenue_query(project, dataset)).to_dataframe()


def load_export_controls(
    client: bigquery.Client, project: str, dataset: str
) -> pd.DataFrame:
    return client.query(build_export_controls_query(project, dataset)).to_dataframe()
