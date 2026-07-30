import pandas as pd
import numpy as np
from scipy.stats import norm


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Computes Historical Value at Risk (VaR)."""
    if len(returns) == 0:
        return 0.0
    return -np.percentile(returns, (1 - confidence) * 100)


def parametric_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Computes Parametric (Normal) Value at Risk (VaR)."""
    if len(returns) == 0:
        return 0.0
    mu = np.mean(returns)
    sigma = np.std(returns)
    z_score = norm.ppf(1 - confidence)
    return -(mu + z_score * sigma)


def historical_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    """Computes Historical Conditional Value at Risk (Expected Shortfall)."""
    if len(returns) == 0:
        return 0.0
    var_threshold = -historical_var(returns, confidence)
    tail_losses = returns[returns <= var_threshold]
    if len(tail_losses) == 0:
        return -var_threshold
    return -tail_losses.mean()


def portfolio_var(
    returns: pd.DataFrame, weights: np.ndarray, confidence: float = 0.95
) -> float:
    """Computes portfolio Historical VaR."""
    port_ret = returns.dot(weights)
    return historical_var(port_ret, confidence)
