from unittest.mock import MagicMock

import pandas as pd

from dashboard.queries import (
    build_ai_chip_revenue_query,
    build_export_controls_query,
    load_ai_chip_revenue,
    load_export_controls,
)


def test_build_ai_chip_revenue_query() -> None:
    sql = build_ai_chip_revenue_query("my-project", "my_dataset")
    assert sql == (
        "select vendor, year, estimated_revenue_usd_m "
        "from `my-project.my_dataset.fct_ai_chip_revenue_yearly`"
    )


def test_build_export_controls_query() -> None:
    sql = build_export_controls_query("my-project", "my_dataset")
    assert sql == (
        "select year, administration, actions "
        "from `my-project.my_dataset.fct_export_controls_yearly`"
    )


def test_load_ai_chip_revenue() -> None:
    client = MagicMock()
    frame = pd.DataFrame({"vendor": ["NVIDIA", "AMD"], "year": [2023, 2023]})
    client.query.return_value.to_dataframe.return_value = frame

    result = load_ai_chip_revenue(client, "my-project", "my_dataset")

    pd.testing.assert_frame_equal(result, frame)
    client.query.assert_called_once_with(
        build_ai_chip_revenue_query("my-project", "my_dataset")
    )


def test_load_export_controls() -> None:
    client = MagicMock()
    frame = pd.DataFrame({"year": [2022, 2023], "actions": [5, 7]})
    client.query.return_value.to_dataframe.return_value = frame

    result = load_export_controls(client, "my-project", "my_dataset")

    pd.testing.assert_frame_equal(result, frame)
    client.query.assert_called_once_with(
        build_export_controls_query("my-project", "my_dataset")
    )
