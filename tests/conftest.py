import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_prices():
    dates = pd.date_range("2023-01-01", periods=100)
    data = np.random.lognormal(mean=0.0005, sigma=0.01, size=(100, 3)).cumprod(axis=0)
    return pd.DataFrame(data, index=dates, columns=["AAPL", "MSFT", "GOOGL"])


@pytest.fixture
def sample_returns(sample_prices):
    from src.market_risk.returns import compute_daily_returns

    return compute_daily_returns(sample_prices)


@pytest.fixture
def sample_credit_df():
    data = {
        "borrower_id": ["B001", "B002", "B003"],
        "sector": ["Technology", "Healthcare", "Technology"],
        "exposure": [1000000, 500000, 2000000],
        "leverage_ratio": [3.5, 7.2, 2.1],
        "interest_coverage": [5.1, 1.2, 8.4],
        "current_ratio": [1.5, 0.8, 2.1],
        "revenue_growth": [0.15, -0.05, 0.25],
        "years_in_business": [10, 3, 25],
        "has_collateral": [1, 0, 1],
        "pd": [0.01, 0.08, 0.005],
        "rating": ["A", "CCC", "AA"],
    }
    return pd.DataFrame(data)
