import pandas as pd
import numpy as np

def calculate_lgd(has_collateral: int, sector: str) -> float:
    """
    Estimates Loss Given Default (LGD).
    Secured loans (has_collateral=1) have lower LGD.
    Some sectors have higher recovery rates (e.g., Utilities, Real Estate).
    """
    base_lgd = 0.45 # Standard uncollateralized LGD
    
    if has_collateral == 1:
        base_lgd -= 0.20 # Collateral reduces loss by 20%
        
    if sector in ["Utilities", "Financials"]:
        base_lgd -= 0.05
    elif sector in ["Technology", "Healthcare"]:
        base_lgd += 0.05
        
    return max(0.10, min(base_lgd, 1.0))

def calculate_expected_loss(credit_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Expected Loss (EL) = PD * EAD * LGD.
    Adds 'lgd' and 'expected_loss' columns to the dataframe.
    """
    df = credit_df.copy()
    
    # EAD is assumed to be the current exposure
    if "pd" not in df.columns:
        raise ValueError("DataFrame must contain a 'pd' (Probability of Default) column.")
        
    df["lgd"] = df.apply(lambda row: calculate_lgd(row["has_collateral"], row["sector"]), axis=1)
    df["expected_loss"] = df["pd"] * df["exposure"] * df["lgd"]
    
    return df
