import pandas as pd
import numpy as np

# Predefined Stress Scenarios (Shocks to specific sectors/asset classes)
SCENARIOS = {
    "2008 Financial Crisis": {
        "Financials": -0.40,
        "Technology": -0.25,
        "Energy": -0.30,
        "Healthcare": -0.15,
        "Consumer Defensive": -0.10,
        "Industrials": -0.35,
        "Utilities": -0.15,
        "Consumer Cyclical": -0.30,
        "Bonds": 0.10  # Flight to safety
    },
    "COVID-19 Crash": {
        "Financials": -0.35,
        "Technology": -0.20,
        "Energy": -0.50,
        "Healthcare": -0.10,
        "Consumer Defensive": -0.05,
        "Industrials": -0.35,
        "Utilities": -0.25,
        "Consumer Cyclical": -0.40,
        "Bonds": 0.05
    },
    "Tech Sector Selloff": {
        "Technology": -0.35,
        "Consumer Cyclical": -0.15,
        "Bonds": 0.02
    },
    "Rate Shock (+200bps)": {
        "Bonds": -0.15,
        "Technology": -0.20,
        "Utilities": -0.20,
        "Financials": 0.05  # Banks might benefit from net interest margin initially
    },
    "Energy Crisis": {
        "Energy": -0.40,
        "Industrials": -0.15,
        "Utilities": -0.10
    }
}

def apply_stress_scenario(portfolio_weights: dict, sector_mapping: dict, scenario_name: str) -> dict:
    """
    Applies a predefined stress scenario to the portfolio.
    portfolio_weights: dict of ticker -> weight
    sector_mapping: dict of ticker -> sector
    Returns a dict with impact details.
    """
    if scenario_name not in SCENARIOS:
        raise ValueError(f"Scenario '{scenario_name}' not found.")
        
    shocks = SCENARIOS[scenario_name]
    
    stressed_returns = {}
    portfolio_loss = 0.0
    
    for ticker, weight in portfolio_weights.items():
        sector = sector_mapping.get(ticker, "Unknown")
        shock = shocks.get(sector, 0.0) # 0 shock if sector not in scenario
        asset_loss = weight * shock
        
        stressed_returns[ticker] = {
            "Sector": sector,
            "Weight": weight,
            "Shock": shock,
            "Contribution to Portfolio Return": asset_loss
        }
        portfolio_loss += asset_loss
        
    return {
        "scenario": scenario_name,
        "total_portfolio_return": portfolio_loss,
        "asset_details": stressed_returns
    }
