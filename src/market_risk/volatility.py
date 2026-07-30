import pandas as pd
import numpy as np

def rolling_volatility(returns: pd.DataFrame, window: int = 21, annualize: bool = True) -> pd.DataFrame:
    """Computes rolling historical volatility (standard deviation of returns)."""
    vol = returns.rolling(window=window).std()
    if annualize:
        vol = vol * np.sqrt(252)
    return vol

def ewma_volatility(returns: pd.DataFrame, span: int = 21, annualize: bool = True) -> pd.DataFrame:
    """Computes Exponentially Weighted Moving Average (EWMA) volatility."""
    vol = returns.ewm(span=span).std()
    if annualize:
        vol = vol * np.sqrt(252)
    return vol

def compute_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
    """Computes CAPM beta of an asset relative to the market."""
    covariance = np.cov(asset_returns, market_returns)[0, 1]
    market_variance = np.var(market_returns, ddof=1)
    return covariance / market_variance if market_variance != 0 else 1.0

def compute_correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """Computes pairwise Pearson correlation matrix."""
    return returns.corr()
