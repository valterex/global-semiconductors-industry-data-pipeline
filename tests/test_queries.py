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
    assert "`my-project.my_dataset.fct_ai_chip_revenue_yearly`" in sql


def test_build_export_controls_query() -> None:
    sql = build_export_controls_query("my-project", "my_dataset")
    assert "`my-project.my_dataset.fct_export_controls_yearly`" in sql


def test_load_ai_chip_revenue() -> None:
    client = MagicMock()
    client.query.return_value.to_dataframe.return_value = pd.DataFrame(
        {"vendor": ["NVIDIA"]}
    )
    result = load_ai_chip_revenue(client, "p", "d")
    assert result["vendor"].tolist() == ["NVIDIA"]
    client.query.assert_called_once()


def test_load_export_controls() -> None:
    client = MagicMock()
    client.query.return_value.to_dataframe.return_value = pd.DataFrame({"year": [2023]})
    result = load_export_controls(client, "p", "d")
    assert result["year"].tolist() == [2023]
    client.query.assert_called_once()
