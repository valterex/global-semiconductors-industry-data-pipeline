import pandas as pd
import pytest


@pytest.fixture
def revenue_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "vendor": ["NVIDIA", "NVIDIA", "AMD", "Intel"],
            "year": [2022, 2023, 2023, 2023],
            "estimated_revenue_usd_m": [100.0, 150.0, 80.0, 60.0],
        }
    )


@pytest.fixture
def controls_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "year": [2022, 2023],
            "administration": ["Biden", "Biden"],
            "actions": [5, 7],
        }
    )
