import pytest
import numpy as np
from src.market_risk.monte_carlo import run_monte_carlo_simulation
from src.market_risk.stress_testing import apply_stress_scenario, SCENARIOS


def test_monte_carlo_returns_correct_shape(sample_returns):
    weights = np.ones(len(sample_returns.columns)) / len(sample_returns.columns)
    result = run_monte_carlo_simulation(sample_returns, weights, num_simulations=100, time_horizon=5)
    assert len(result["final_returns"]) == 100
    assert result["var_95"] >= 0
    assert result["var_99"] >= result["var_95"]


def test_monte_carlo_without_seed_gives_different_results(sample_returns):
    """Verify that without a fixed seed, results vary across calls."""
    weights = np.ones(len(sample_returns.columns)) / len(sample_returns.columns)
    r1 = run_monte_carlo_simulation(sample_returns, weights, num_simulations=50, time_horizon=5)
    r2 = run_monte_carlo_simulation(sample_returns, weights, num_simulations=50, time_horizon=5)
    # The two runs should (almost certainly) not be identical
    assert not np.array_equal(r1["final_returns"], r2["final_returns"])


def test_stress_scenario_returns_loss():
    weights = {"AAPL": 0.5, "JPM": 0.5}
    sector_map = {"AAPL": "Technology", "JPM": "Financials"}
    result = apply_stress_scenario(weights, sector_map, "2008 Financial Crisis")
    assert result["total_portfolio_return"] < 0  # should be negative


def test_stress_scenario_unknown_ticker_gets_fallback():
    weights = {"UNKNOWN": 1.0}
    sector_map = {"UNKNOWN": "SomeNewSector"}
    result = apply_stress_scenario(weights, sector_map, "COVID-19 Crash")
    # Should get the -0.10 fallback, not 0.0
    assert result["total_portfolio_return"] < 0
