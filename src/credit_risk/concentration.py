import pandas as pd
import numpy as np

def calculate_hhi(exposures: pd.Series) -> float:
    """
    Calculates Herfindahl-Hirschman Index (HHI) for concentration.
    Values > 0.25 typically indicate high concentration.
    """
    total = exposures.sum()
    if total == 0: return 0.0
    shares = exposures / total
    hhi = (shares ** 2).sum()
    return hhi

def sector_concentration(credit_df: pd.DataFrame) -> dict:
    """Returns exposure by sector and sector HHI."""
    sector_exp = credit_df.groupby("sector")["exposure"].sum()
    hhi = calculate_hhi(sector_exp)
    return {
        "exposures": sector_exp,
        "hhi": hhi
    }

def borrower_concentration(credit_df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Returns top N largest exposures."""
    top = credit_df.nlargest(top_n, "exposure")
    total_exposure = credit_df["exposure"].sum()
    top["pct_of_portfolio"] = top["exposure"] / total_exposure
    return top[["borrower_id", "sector", "exposure", "pct_of_portfolio", "rating"]]
