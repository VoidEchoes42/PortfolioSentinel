import numpy as np
import pandas as pd

from src.market_risk.returns import (
    compute_cumulative_returns,
    compute_daily_returns,
    compute_drawdown,
)
from src.market_risk.var_cvar import historical_cvar, historical_var, parametric_var
from src.market_risk.volatility import compute_beta, rolling_volatility


def test_compute_daily_returns(sample_prices):
    returns = compute_daily_returns(sample_prices)
    assert len(returns) == 29  # 30 prices -> 29 returns
    assert returns.shape[1] == 2


def test_cumulative_returns_start_near_zero(sample_returns):
    cum = compute_cumulative_returns(sample_returns)
    # First cumulative return should be close to the first daily return
    assert abs(cum.iloc[0]["AAPL"]) < 0.05


def test_drawdown_always_negative_or_zero(sample_prices):
    dd = compute_drawdown(sample_prices)
    assert (dd <= 0).all().all()


def test_historical_var_positive():
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0, 0.01, 1000))
    var = historical_var(returns, 0.95)
    assert var > 0
    assert var < 0.05


def test_parametric_var_positive():
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.001, 0.02, 1000))
    var = parametric_var(returns, 0.99)
    assert var > 0


def test_cvar_greater_than_var():
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0, 0.02, 1000))
    var = historical_var(returns, 0.95)
    cvar = historical_cvar(returns, 0.95)
    assert cvar >= var


def test_compute_beta_market_against_itself():
    np.random.seed(42)
    market = pd.Series(np.random.normal(0, 0.01, 500))
    beta = compute_beta(market, market)
    assert np.isclose(beta, 1.0, atol=0.01)


def test_rolling_volatility_shape(sample_returns):
    vol = rolling_volatility(sample_returns, window=5)
    assert vol.shape == sample_returns.shape
