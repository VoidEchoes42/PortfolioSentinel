import numpy as np
import pandas as pd

from src.credit_risk.concentration import calculate_hhi
from src.credit_risk.exposure import calculate_expected_loss, calculate_lgd
from src.credit_risk.scoring import assign_credit_rating, train_credit_model
from src.credit_risk.watchlist import generate_watchlist


def test_calculate_lgd_secured_utility():
    # Base 0.45 - 0.20 (collateral) - 0.05 (utility) = 0.20
    assert calculate_lgd(1, "Utilities") == 0.20


def test_calculate_lgd_unsecured_tech():
    # Base 0.45 + 0.05 (tech) = 0.50
    assert calculate_lgd(0, "Technology") == 0.50


def test_lgd_floor():
    # Should never go below 0.10
    assert calculate_lgd(1, "Utilities") >= 0.10


def test_expected_loss_formula():
    df = pd.DataFrame(
        {
            "pd": [0.10],
            "exposure": [1_000_000],
            "has_collateral": [1],
            "sector": ["Financials"],
        }
    )
    el_df = calculate_expected_loss(df)
    # LGD = 0.45 - 0.20 - 0.05 = 0.20
    # EL = 0.10 * 1,000,000 * 0.20 = 20,000
    assert el_df.iloc[0]["expected_loss"] == 20_000


def test_hhi_equal_split():
    exposures = pd.Series([50, 50])
    assert calculate_hhi(exposures) == 0.5


def test_hhi_single_borrower():
    exposures = pd.Series([100])
    assert calculate_hhi(exposures) == 1.0


def test_hhi_diversified():
    exposures = pd.Series([25, 25, 25, 25])
    assert calculate_hhi(exposures) == 0.25


def test_credit_rating_mapping():
    assert assign_credit_rating(0.001) == "AAA"
    assert assign_credit_rating(0.05) == "BB"
    assert assign_credit_rating(0.30) == "D"


def test_train_credit_model_returns_metrics(sample_credit_df):
    # Need enough data for a split - extend the sample
    big_df = pd.concat([sample_credit_df] * 20, ignore_index=True)
    big_df["default"] = np.random.choice([0, 1], size=len(big_df), p=[0.85, 0.15])
    _model, metrics = train_credit_model(big_df, save_model=False)
    assert "accuracy" in metrics
    assert "roc_auc" in metrics
    assert 0 <= metrics["accuracy"] <= 1


def test_watchlist_flags_risky_borrowers():
    df = pd.DataFrame(
        {
            "borrower_id": ["B_001"],
            "sector": ["Tech"],
            "leverage_ratio": [8.0],
            "interest_coverage": [1.0],
            "revenue_growth": [-0.20],
            "exposure": [1_000_000],
            "pd": [0.20],
            "rating": ["CCC"],
        }
    )
    watchlist = generate_watchlist(df)
    assert len(watchlist) >= 1
