import pandas as pd
import pytest

from dashboard.transforms import (
    filter_by_vendors,
    filter_by_year,
    pivot_controls,
    pivot_revenue,
    year_range,
)


def test_year_range(revenue_df: pd.DataFrame, controls_df: pd.DataFrame) -> None:
    assert year_range(revenue_df, controls_df) == (2022, 2023)


@pytest.mark.parametrize(
    ("start", "end", "expected_years"),
    [
        (2022, 2023, [2022, 2023, 2023, 2023]),
        (2023, 2023, [2023, 2023, 2023]),
        (2020, 2021, []),
    ],
)
def test_filter_by_year(
    revenue_df: pd.DataFrame, start: int, end: int, expected_years: list[int]
) -> None:
    result = filter_by_year(revenue_df, start, end)
    assert result["year"].tolist() == expected_years


@pytest.mark.parametrize(
    ("vendors", "expected"),
    [
        (["NVIDIA"], ["NVIDIA", "NVIDIA"]),
        (["Qualcomm"], []),
    ],
)
def test_filter_by_vendors(
    revenue_df: pd.DataFrame, vendors: list[str], expected: list[str]
) -> None:
    result = filter_by_vendors(revenue_df, vendors)
    assert result["vendor"].tolist() == expected


def test_filter_by_vendors_empty_is_noop(revenue_df: pd.DataFrame) -> None:
    result = filter_by_vendors(revenue_df, [])
    pd.testing.assert_frame_equal(result, revenue_df)


def test_pivot_revenue(revenue_df: pd.DataFrame) -> None:
    result = pivot_revenue(revenue_df)
    expected = pd.DataFrame(
        {
            "AMD": [float("nan"), 80.0],
            "Intel": [float("nan"), 60.0],
            "NVIDIA": [100.0, 150.0],
        },
        index=pd.Index([2022, 2023], name="year"),
    )
    expected.columns.name = "vendor"
    pd.testing.assert_frame_equal(result, expected)


def test_pivot_revenue_duplicate_year_vendor_raises() -> None:
    dup = pd.DataFrame(
        {
            "vendor": ["NVIDIA", "NVIDIA"],
            "year": [2023, 2023],
            "estimated_revenue_usd_m": [100.0, 150.0],
        }
    )
    with pytest.raises(ValueError, match="Index contains duplicate entries"):
        pivot_revenue(dup)


def test_pivot_controls(controls_df: pd.DataFrame) -> None:
    result = pivot_controls(controls_df)
    expected = pd.DataFrame(
        {"Biden": [5, 7]},
        index=pd.Index([2022, 2023], name="year"),
    )
    expected.columns.name = "administration"
    pd.testing.assert_frame_equal(result, expected)
