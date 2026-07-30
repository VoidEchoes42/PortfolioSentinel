import numpy as np
import pandas as pd


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Computes daily returns from price series."""
    return prices.pct_change().dropna()


def compute_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Computes cumulative product of returns."""
    return (1 + returns).cumprod() - 1


def compute_drawdown(prices: pd.DataFrame) -> pd.DataFrame:
    """Computes the drawdown series for each asset."""
    roll_max = prices.cummax()
    drawdown = (prices - roll_max) / roll_max
    return drawdown


def compute_max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """Computes the maximum drawdown for each asset."""
    drawdown = compute_drawdown(prices)
    return drawdown.min()


def portfolio_returns(returns: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    """Computes portfolio returns given asset weights."""
    return returns.dot(weights)
