import numpy as np
import pandas as pd

from config.settings import SYNTHETIC_DATA_DIR


def generate_credit_portfolio(
    n_borrowers=200, seed=42, output_file="credit_portfolio.csv"
):
    """
    Generates a realistic synthetic dataset for a corporate loan portfolio.
    Features are designed to be predictive of default risk.
    """
    np.random.seed(seed)

    # Generate Borrower IDs
    borrower_ids = [f"B_{str(i).zfill(4)}" for i in range(1, n_borrowers + 1)]

    # Sectors distribution
    sectors = np.random.choice(
        [
            "Technology",
            "Financials",
            "Energy",
            "Healthcare",
            "Consumer Defensive",
            "Industrials",
            "Utilities",
        ],
        size=n_borrowers,
        p=[0.20, 0.15, 0.10, 0.15, 0.15, 0.15, 0.10],
    )

    # Financial Ratios (Base distributions)
    # 1. Leverage Ratio (Debt / EBITDA) - higher is worse (typically 1x - 8x)
    leverage = np.random.lognormal(mean=0.8, sigma=0.6, size=n_borrowers)
    leverage = np.clip(leverage, 0.1, 15.0)

    # 2. Interest Coverage Ratio (EBITDA / Interest Expense) - lower is worse (typically 1x - 20x)
    interest_coverage = np.random.lognormal(mean=1.5, sigma=0.8, size=n_borrowers)
    interest_coverage = np.clip(interest_coverage, 0.1, 50.0)

    # 3. Current Ratio (Current Assets / Current Liabilities) - lower is worse (typically 0.5 - 3.0)
    current_ratio = np.random.normal(loc=1.5, scale=0.8, size=n_borrowers)
    current_ratio = np.clip(current_ratio, 0.2, 5.0)

    # 4. Revenue Growth (%) - lower/negative is worse
    rev_growth = np.random.normal(loc=0.05, scale=0.15, size=n_borrowers)

    # Other Features
    years_in_business = np.random.poisson(lam=15, size=n_borrowers)
    years_in_business = np.clip(years_in_business, 1, 100)

    has_collateral = np.random.choice([0, 1], size=n_borrowers, p=[0.3, 0.7])

    # Base Exposure (EAD surrogate) - Lognormal distribution
    exposure = np.random.lognormal(mean=15, sigma=1.5, size=n_borrowers)  # ~ $3M mean

    # Generate Synthetic Default Target (Binary)
    # Construct a risk score from financial ratios to set up the binary default target
    # Higher leverage, lower coverage, lower current ratio, negative growth increase risk
    risk_score = (
        0.5 * leverage
        - 0.4 * np.log1p(interest_coverage)
        - 0.3 * current_ratio
        - 2.0 * rev_growth
        - 0.1 * np.sqrt(years_in_business)
        - 0.5 * has_collateral
    )

    # Add noise
    risk_score += np.random.normal(0, 1.0, size=n_borrowers)

    # Convert to probability using sigmoid
    true_pd = 1 / (1 + np.exp(-risk_score))

    # Adjust intercept to target a reasonable portfolio default rate (~ 5-8%)
    target_default_rate = 0.07
    current_rate = np.mean(true_pd)
    adjustment = np.log(target_default_rate / (1 - target_default_rate)) - np.log(
        current_rate / (1 - current_rate)
    )

    adjusted_pd = 1 / (1 + np.exp(-(risk_score + adjustment)))

    # Actual binary default outcome (for training purposes)
    default_target = np.random.binomial(1, adjusted_pd)

    df = pd.DataFrame(
        {
            "borrower_id": borrower_ids,
            "sector": sectors,
            "leverage_ratio": leverage,
            "interest_coverage": interest_coverage,
            "current_ratio": current_ratio,
            "revenue_growth": rev_growth,
            "years_in_business": years_in_business,
            "has_collateral": has_collateral,
            "exposure": exposure,
            "default": default_target,
        }
    )

    out_path = SYNTHETIC_DATA_DIR / output_file
    df.to_csv(out_path, index=False)
    print(f"Synthetic credit portfolio generated and saved to {out_path}")
    return df


def load_credit_portfolio(file_name="credit_portfolio.csv"):
    """Loads the credit portfolio from disk, generating it if it doesn't exist."""
    file_path = SYNTHETIC_DATA_DIR / file_name
    if not file_path.exists():
        print("Credit portfolio not found. Generating...")
        return generate_credit_portfolio(output_file=file_name)
    return pd.read_csv(file_path)


if __name__ == "__main__":
    generate_credit_portfolio()
