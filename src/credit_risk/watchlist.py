import pandas as pd
from config.settings import THRESHOLDS

def generate_watchlist(credit_df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags borrowers that breach risk thresholds and adds them to a watchlist.
    """
    watchlist = []
    
    for _, row in credit_df.iterrows():
        reasons = []
        
        # PD Warning
        if row.get("pd", 0) > THRESHOLDS["pd_critical"]:
            reasons.append(f"Critical PD ({row['pd']:.1%})")
        elif row.get("pd", 0) > THRESHOLDS["pd_warning"]:
            reasons.append(f"High PD ({row['pd']:.1%})")
            
        # Financial Health Warnings
        if row["leverage_ratio"] > THRESHOLDS.get("leverage_warning", 6.0):
            reasons.append(f"High Leverage ({row['leverage_ratio']:.1f}x)")
            
        if row["interest_coverage"] < THRESHOLDS.get("interest_coverage_warning", 1.5):
            reasons.append(f"Weak Interest Coverage ({row['interest_coverage']:.1f}x)")
            
        if row["revenue_growth"] < THRESHOLDS.get("revenue_growth_warning", -0.10):
            reasons.append(f"Declining Revenue ({row['revenue_growth']:.1%})")
            
        if len(reasons) >= 2 or (row.get("pd", 0) > THRESHOLDS["pd_warning"]):
            watchlist.append({
                "borrower_id": row["borrower_id"],
                "sector": row["sector"],
                "exposure": row["exposure"],
                "rating": row.get("rating", "N/A"),
                "reasons": "; ".join(reasons),
                "severity": "High" if row.get("pd", 0) > THRESHOLDS["pd_critical"] else "Medium"
            })
            
    return pd.DataFrame(watchlist)
