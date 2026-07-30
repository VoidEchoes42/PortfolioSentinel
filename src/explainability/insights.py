import numpy as np
import pandas as pd


def feature_importance(model_pipeline, feature_names: list) -> pd.DataFrame:
    """
    Extracts feature importance from the Logistic Regression model.
    Uses absolute coefficient values.
    """
    classifier = model_pipeline.named_steps["classifier"]
    coeffs = classifier.coef_[0]

    importance_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Coefficient": coeffs,
            "Absolute_Importance": np.abs(coeffs),
        }
    )

    importance_df = importance_df.sort_values(by="Absolute_Importance", ascending=False)
    return importance_df


def generate_portfolio_summary(
    market_vol: float, market_var: float, credit_el: float, active_alerts: int
) -> str:
    """Generates an executive summary of the portfolio's current risk profile."""

    summary = f"Portfolio vol is running at {market_vol:.1%}, with a 1-day 95% Value at Risk of {market_var:.1%}. "

    if active_alerts > 0:
        summary += f"There are {active_alerts} active risk alerts requiring attention. "
    else:
        summary += "All risk metrics are within limits. "

    summary += f"Credit book EL is ${credit_el:,.0f}."

    return summary


def generate_credit_insight(borrower_row: pd.Series) -> str:
    """Generates explanatory text for why a specific borrower is high risk."""
    reasons = []
    if borrower_row.get("leverage_ratio", 0) > 6.0:
        reasons.append("excessive leverage")
    if borrower_row.get("interest_coverage", 10) < 1.5:
        reasons.append("weak interest coverage")
    if borrower_row.get("revenue_growth", 0) < 0:
        reasons.append("declining revenue")

    if not reasons:
        return f"Borrower {borrower_row.get('borrower_id', 'Unknown')} looks fine — no flags raised."

    reason_text = ", ".join(reasons[:-1]) + (
        " and " + reasons[-1] if len(reasons) > 1 else reasons[0]
    )
    return f"Borrower {borrower_row.get('borrower_id', 'Unknown')} is flagged for {reason_text}."
