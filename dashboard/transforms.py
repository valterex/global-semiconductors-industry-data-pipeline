from typing import cast

import pandas as pd


def year_range(revenue: pd.DataFrame, controls: pd.DataFrame) -> tuple[int, int]:
    min_year = min(
        cast(int, revenue["year"].min()),
        cast(int, controls["year"].min()),
    )
    max_year = max(
        cast(int, revenue["year"].max()),
        cast(int, controls["year"].max()),
    )
    return min_year, max_year


def filter_by_year(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    return cast(pd.DataFrame, df[df["year"].between(start, end)])


def filter_by_vendors(df: pd.DataFrame, vendors: list[str]) -> pd.DataFrame:
    if not vendors:
        return df
    return cast(pd.DataFrame, df[df["vendor"].isin(vendors)])


def pivot_revenue(revenue: pd.DataFrame) -> pd.DataFrame:
    return cast(
        pd.DataFrame,
        revenue.pivot(index="year", columns="vendor", values="estimated_revenue_usd_m"),
    )


def pivot_controls(controls: pd.DataFrame) -> pd.DataFrame:
    return cast(
        pd.DataFrame,
        controls.pivot(index="year", columns="administration", values="actions"),
    )
