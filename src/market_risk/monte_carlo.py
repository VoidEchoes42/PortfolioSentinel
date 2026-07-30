import numpy as np
import pandas as pd

def run_monte_carlo_simulation(returns: pd.DataFrame, weights: np.ndarray, num_simulations: int = 1000, time_horizon: int = 21, seed: int = None) -> dict:
    """
    Runs Monte Carlo simulation for portfolio losses.
    Assumes multivariate normal distribution of returns.
    """
    cov_matrix = returns.cov().values
    mean_returns = returns.mean().values
    
    # Simulate random daily returns for the given time horizon
    if seed is not None:
        np.random.seed(seed)
    # Generate (num_simulations, time_horizon, num_assets)
    sim_returns = np.random.multivariate_normal(mean_returns, cov_matrix, (num_simulations, time_horizon))
    
    # Calculate portfolio returns for each simulation
    # Dot product with weights gives (num_simulations, time_horizon)
    port_sim_returns = np.dot(sim_returns, weights)
    
    # Cumulative returns over the time horizon
    cumulative_returns = np.prod(1 + port_sim_returns, axis=1) - 1
    
    # Calculate 95% and 99% VaR from the simulation
    var_95 = -np.percentile(cumulative_returns, 5)
    var_99 = -np.percentile(cumulative_returns, 1)
    
    # Calculate Expected Shortfall (CVaR)
    cvar_95 = -np.mean(cumulative_returns[cumulative_returns <= -var_95])
    
    return {
        "final_returns": cumulative_returns,
        "var_95": max(0, var_95),
        "var_99": max(0, var_99),
        "cvar_95": max(0, cvar_95)
    }
