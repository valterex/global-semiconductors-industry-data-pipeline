#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import kagglehub

FILES = [
    "ai_chip_market.csv",
    "chip_prices.csv",
    "export_controls.csv",
    "fab_capacity.csv",
    "chip_companies_financials.csv",
]

DATASET_HANDLE = "sergionefedov/global-semiconductor-industry-2010-2026"
DATABASE_URL = "postgresql+psycopg://***REMOVED***@localhost:5432/global-semiconductor-industry-2010-2026"
CHUNKSIZE = 100_000


def run() -> None:
    engine = create_engine(DATABASE_URL)
    path = kagglehub.dataset_download(DATASET_HANDLE)

    for file_name in tqdm(FILES):
        df = pd.read_csv(
            f"{path}/{file_name}",
            iterator=True,
            chunksize=CHUNKSIZE,
        )

        table_name = file_name.removesuffix(".csv")
        first = True

        for chunk in df:
            if first:
                chunk.head(0).to_sql(
                    name=table_name,
                    con=engine,
                    if_exists="replace",
                    index=False,
                )
                first = False

            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
            )


if __name__ == "__main__":
    run()
