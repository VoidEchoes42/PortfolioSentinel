import pandas as pd

def clean_market_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans market price data.
    - Fills missing dates (forward fill, then backward fill for start of series)
    - Drops columns that are entirely NaN
    """
    if df.empty:
        return df
        
    df = df.copy()
    
    # Drop assets that have no data at all
    df.dropna(axis=1, how="all", inplace=True)
    
    # Forward fill missing daily prices (e.g., trading halts)
    df.ffill(inplace=True)
    
    # Backward fill for any leading NaNs
    df.bfill(inplace=True)
    
    return df

def clean_credit_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans credit portfolio data.
    - Handles missing values in ratios
    - Ensures correct datatypes
    """
    if df.empty:
        return df
        
    df = df.copy()
    
    # For a synthetic dataset, we might not have NaNs, but good practice for real data:
    numeric_cols = ["leverage_ratio", "interest_coverage", "current_ratio", "revenue_growth", "exposure"]
    for col in numeric_cols:
        if col in df.columns:
            # Fill missing with median
            df[col] = df[col].fillna(df[col].median())
            
    if "years_in_business" in df.columns:
        df["years_in_business"] = df["years_in_business"].fillna(0).astype(int)
        
    if "has_collateral" in df.columns:
        df["has_collateral"] = df["has_collateral"].fillna(0).astype(int)
        
    return df
