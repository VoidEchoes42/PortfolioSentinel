import pytest
import pandas as pd
import numpy as np
from src.market_risk.returns import compute_daily_returns, compute_cumulative_returns
from src.market_risk.var_cvar import historical_var, parametric_var

@pytest.fixture
def sample_prices():
    dates = pd.date_range("2023-01-01", periods=5, freq="D")
    return pd.DataFrame({
        "AAPL": [150, 152, 151, 155, 153],
        "MSFT": [250, 248, 252, 255, 260]
    }, index=dates)

def test_compute_daily_returns(sample_prices):
    returns = compute_daily_returns(sample_prices)
    assert len(returns) == 4
    assert np.isclose(returns.iloc[0]["AAPL"], 2/150)
    
def test_historical_var():
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0, 0.01, 1000))
    var = historical_var(returns, 0.95)
    assert var > 0
    assert var < 0.05  # should be around 1.64 * 0.01

def test_parametric_var():
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.001, 0.02, 1000))
    var = parametric_var(returns, 0.99)
    assert var > 0
