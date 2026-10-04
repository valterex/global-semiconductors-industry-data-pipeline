import pandas as pd

from dashboard.transforms import (
    filter_by_vendors,
    filter_by_year,
    pivot_controls,
    pivot_revenue,
    year_range,
)


def test_year_range(revenue_df: pd.DataFrame, controls_df: pd.DataFrame) -> None:
    assert year_range(revenue_df, controls_df) == (2022, 2023)


def test_filter_by_year(revenue_df: pd.DataFrame) -> None:
    result = filter_by_year(revenue_df, 2023, 2023)
    assert result["year"].tolist() == [2023, 2023, 2023]


def test_filter_by_vendors(revenue_df: pd.DataFrame) -> None:
    result = filter_by_vendors(revenue_df, ["NVIDIA"])
    assert result["vendor"].unique().tolist() == ["NVIDIA"]


def test_filter_by_vendors_empty_is_noop(revenue_df: pd.DataFrame) -> None:
    result = filter_by_vendors(revenue_df, [])
    pd.testing.assert_frame_equal(result, revenue_df)


def test_pivot_revenue(revenue_df: pd.DataFrame) -> None:
    result = pivot_revenue(revenue_df)
    assert result.columns.tolist() == ["AMD", "Intel", "NVIDIA"]
    assert result.loc[2023, "NVIDIA"] == 150.0


def test_pivot_controls(controls_df: pd.DataFrame) -> None:
    result = pivot_controls(controls_df)
    assert result.loc[2022, "Biden"] == 5
