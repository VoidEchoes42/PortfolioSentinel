import numpy as np
import pandas as pd


def risk_contribution(returns: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    """
    Computes percentage risk contribution of each asset to the portfolio volatility.
    Uses marginal contribution to risk (Euler allocation).
    """
    cov_matrix = returns.cov() * 252  # annualized
    portfolio_vol = np.sqrt(weights.T @ cov_matrix @ weights)

    # Marginal Risk Contribution = Covariance * weights / Portfolio Vol
    mrc = (cov_matrix @ weights) / portfolio_vol

    # Risk Contribution = weights * MRC
    rc = weights * mrc

    # Percentage Risk Contribution
    prc = rc / portfolio_vol

    return pd.Series(prc, index=returns.columns)


def marginal_var(
    returns: pd.DataFrame, weights: np.ndarray, confidence: float = 0.95
) -> pd.Series:
    """
    Computes marginal VaR for each asset.
    Approximated using parametric (normal) assumption.
    """
    from scipy.stats import norm

    cov_matrix = returns.cov() * 252
    portfolio_vol = np.sqrt(weights.T @ cov_matrix @ weights)

    z_score = norm.ppf(1 - confidence)

    # Marginal impact on portfolio volatility
    mrc = (cov_matrix @ weights) / portfolio_vol

    # Marginal VaR
    mvar = -z_score * mrc

    return pd.Series(mvar, index=returns.columns)
