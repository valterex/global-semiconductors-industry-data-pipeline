from dashboard.config import gcp_config


def test_gcp_config_unset(monkeypatch) -> None:
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    monkeypatch.delenv("GCP_DATASET", raising=False)
    assert gcp_config() == (None, None)


def test_gcp_config_set(monkeypatch) -> None:
    monkeypatch.setenv("GCP_PROJECT_ID", "my-project")
    monkeypatch.setenv("GCP_DATASET", "my_dataset")
    assert gcp_config() == ("my-project", "my_dataset")
