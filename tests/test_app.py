from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "dashboard" / "app.py"


def test_app_requires_env(monkeypatch) -> None:
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    monkeypatch.delenv("GCP_DATASET", raising=False)

    at = AppTest.from_file(str(APP)).run()

    assert len(at.error) == 1
    assert "GCP_PROJECT_ID" in at.error[0].value
