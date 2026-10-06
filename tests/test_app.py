from pathlib import Path
from unittest.mock import MagicMock, patch

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "dashboard" / "app.py"


def test_app_requires_env(monkeypatch) -> None:
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    monkeypatch.delenv("GCP_DATASET", raising=False)

    at = AppTest.from_file(str(APP)).run()

    assert len(at.error) == 1
    assert "GCP_PROJECT_ID" in at.error[0].value


def test_app_happy_path(monkeypatch, revenue_df, controls_df) -> None:
    monkeypatch.setenv("GCP_PROJECT_ID", "test-project")
    monkeypatch.setenv("GCP_DATASET", "test_dataset")

    client = MagicMock()
    client.query.side_effect = [
        MagicMock(to_dataframe=MagicMock(return_value=revenue_df)),
        MagicMock(to_dataframe=MagicMock(return_value=controls_df)),
    ]

    with patch("dashboard.queries.get_client", return_value=client):
        at = AppTest.from_file(str(APP)).run()

    assert len(at.error) == 0
