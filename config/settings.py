from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"
MODELS_DIR = BASE_DIR / "models"

# Create directories if they don't exist
for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SYNTHETIC_DATA_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Market Data Settings
MARKET_TICKERS = [
    "AAPL", "JPM", "XOM", "JNJ", "PG",
    "MSFT", "AMZN", "GS", "CVX", "UNH",
    "BA", "CAT", "WMT", "NEE", "TLT"
]

SECTOR_MAPPING = {
    "AAPL": "Technology", "MSFT": "Technology", "AMZN": "Consumer Cyclical",
    "JPM": "Financials", "GS": "Financials",
    "XOM": "Energy", "CVX": "Energy",
    "JNJ": "Healthcare", "UNH": "Healthcare",
    "PG": "Consumer Defensive", "WMT": "Consumer Defensive",
    "BA": "Industrials", "CAT": "Industrials",
    "NEE": "Utilities",
    "TLT": "Bonds"
}

# Default Lookback Period for historical data (years)
DEFAULT_LOOKBACK_YEARS = 3

# Risk & Alert Thresholds
THRESHOLDS = {
    "volatility_warning": 0.20,       # 20% annualized vol
    "volatility_critical": 0.30,      # 30% annualized vol
    "drawdown_warning": 0.10,         # 10% drawdown
    "drawdown_critical": 0.15,        # 15% drawdown
    "var_95_critical": 0.05,          # 5% 1-day VaR
    "pd_warning": 0.10,               # 10% Probability of Default
    "pd_critical": 0.15,              # 15% Probability of Default
    "hhi_concentration": 0.25,        # HHI > 0.25 = highly concentrated
    "leverage_warning": 6.0,          # Debt/EBITDA above 6x
    "interest_coverage_warning": 1.5, # EBITDA/Interest below 1.5x
    "revenue_growth_warning": -0.10   # Revenue declining > 10%
}

# UI Settings
UI_COLORS = {
    "background": "#0e1117",
    "primary": "#1f77b4",
    "critical": "#d62728",
    "warning": "#ff7f0e",
    "safe": "#2ca02c"
}
