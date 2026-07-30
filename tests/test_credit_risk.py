import pytest
import pandas as pd
from src.credit_risk.exposure import calculate_lgd, calculate_expected_loss
from src.credit_risk.concentration import calculate_hhi

def test_calculate_lgd():
    lgd_secured_utility = calculate_lgd(1, "Utilities")
    lgd_unsecured_tech = calculate_lgd(0, "Technology")
    
    # Base: 0.45. Secured: -0.20. Utility: -0.05 => 0.20
    assert lgd_secured_utility == 0.20
    
    # Base: 0.45. Unsecured: 0. Tech: +0.05 => 0.50
    assert lgd_unsecured_tech == 0.50

def test_calculate_expected_loss():
    df = pd.DataFrame({
        "pd": [0.10],
        "exposure": [1_000_000],
        "has_collateral": [1],
        "sector": ["Financials"]
    })
    
    # LGD for Secured Financial = 0.45 - 0.20 - 0.05 = 0.20
    # EL = 0.10 * 1,000,000 * 0.20 = 20,000
    el_df = calculate_expected_loss(df)
    assert "expected_loss" in el_df.columns
    assert el_df.iloc[0]["expected_loss"] == 20000

def test_calculate_hhi():
    exposures = pd.Series([50, 50])
    hhi = calculate_hhi(exposures)
    # (0.5)^2 + (0.5)^2 = 0.5
    assert hhi == 0.5
