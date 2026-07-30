# System Architecture

PortfolioSentinel is designed as a modular, data-driven application. The architecture separates data fetching, analytical computations, and frontend presentation to ensure scalability and testability.

## High-Level Data Flow

```text
       yfinance
           │
           ▼
    Data Pipeline
           │
           ▼
   Feature Engineering
           │
    ┌──────┴──────┐
    ▼             ▼
Market Risk   Credit Risk
    │             │
    └──────┬──────┘
           ▼
     Alert Engine
           ▼
    Streamlit Dashboard
           ▼
    PDF / Excel Reports
```

## Component Breakdown

### 1. Data Pipeline (`src/data_pipeline/`)
Responsible for ingesting and cleaning raw data from external APIs and local synthetic datasets.
- **Market Data (`market_data.py`)**: Fetches 30 years of historical pricing data from Yahoo Finance (`yfinance`) for 15 major assets. Implements multi-level index parsing and aggressive in-memory caching to prevent API rate-limiting.
- **Credit Data (`credit_data.py`)**: Generates and manages a synthetic corporate loan book of 200+ borrowers, mapping realistic financial ratios (e.g., Leverage, Interest Coverage).
- **Data Cleaning (`cleaning.py`)**: Implements strict data validation. Handles `NaN` imputation via forward-filling for time-series and median-filling for cross-sectional credit data, preventing downstream machine learning failures.

### 2. Core Analytics Engines (`src/market_risk/` & `src/credit_risk/`)
The analytical brains of the application, completely decoupled from the UI.
- **Market Risk**: Uses vectorized `NumPy` operations to compute 21-day rolling volatility, historical drawdowns, and parametric Value at Risk (VaR). The Monte Carlo engine simulates 1,000+ paths over a 21-day horizon using Cholesky decomposition for correlated assets.
- **Credit Risk**: Uses `scikit-learn` to train a Logistic Regression model on the fly. It predicts the Probability of Default (PD) for each borrower and maps it to industry-standard credit ratings (AAA to D) to calculate Expected Credit Loss (ECL).

### 3. Alert Engine & Persistence (`src/alerts/` & `src/data_pipeline/database.py`)
- **Monitoring**: Constantly evaluates current portfolio metrics against configurable risk thresholds (e.g., VaR > 5%, Portfolio Drawdown > 10%).
- **SQLite Database**: A lightweight, file-based database (`data/processed/risk_database.sqlite`) is used to persist alerts and daily risk snapshots. To prevent locking issues during extreme market events, the engine aggregates systemic asset-level flags into higher-level portfolio alerts before writing to the database.

### 4. Presentation Layer (`app.py` & `pages/`)
- **Streamlit**: Provides a reactive, state-driven user interface.
- **Plotly**: Renders interactive, high-performance web-GL charts (histograms, heatmaps, and line charts).
- **Report Generation (`src/reporting/`)**: Compiles the current UI state and SQLite data into distributable PDF risk reports (`ReportLab`) and Excel logs (`openpyxl`).
