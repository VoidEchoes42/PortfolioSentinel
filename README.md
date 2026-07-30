# PortfolioSentinel: Market & Credit Risk Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![Build](https://github.com/VoidEchoes42/PortfolioSentinel/actions/workflows/ci.yml/badge.svg)

**PortfolioSentinel** is a risk analytics dashboard designed for banking and investment portfolio monitoring. It integrates market risk, credit risk modeling, scenario analysis, and an automated alerting system into a stakeholder-ready UI.

## 🚀 Key Features

### 📈 Market Risk
- **Value at Risk (VaR) & CVaR**: Historical and parametric calculations for portfolio tail risk.
- **Monte Carlo Simulation**: 1000-path simulation of portfolio returns over a 21-day horizon.
- **Volatility & Drawdown**: Rolling volatility (21-day) and interactive drawdown curves.
- **Stress Testing**: Assess portfolio resilience against historical shocks (e.g., 2008 Financial Crisis, COVID-19 Crash).

### 🏦 Credit Risk
- **Probability of Default (PD) Modeling**: Machine learning pipeline (Logistic Regression) predicting borrower default based on financial health ratios.
- **Expected Credit Loss (ECL)**: Calculates Exposure at Default (EAD) and Loss Given Default (LGD) mapped to sector and collateral.
- **Concentration Risk**: Evaluates sector-level exposure using the Herfindahl-Hirschman Index (HHI).
- **Borrower Analysis**: Generates risk factor commentary based on financial ratio thresholds on why specific borrowers are flagged for high risk.

### 🚨 Automation & Reporting
- **Alert Engine**: Actively monitors portfolios against configurable thresholds (VaR breaches, volatility spikes, PD degradation).
- **Database Logging**: All alerts and daily risk snapshots are persisted in a local SQLite database for auditing.
- **Exportable Reports**: Generate PDF risk summaries and Excel alert logs for stakeholder reporting.
- **Reproducible Pipeline**: CI/CD ready with GitHub Actions, `pytest`, `ruff`, and `black`.

---

## 🛠️ Tech Stack & Methodology
- **Languages**: Python (Pandas, NumPy, scikit-learn, SciPy)
- **Data Integration**: `yfinance` (market data), `pandas-datareader` (FRED macroeconomic indicators)
- **UI & Visualization**: Streamlit, Plotly
- **Database**: SQLite
- **Reporting**: ReportLab (PDF), openpyxl (Excel)
- **Code Quality**: `pytest`, `ruff`, `black`, `mypy`

---

## 💻 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/VoidEchoes42/PortfolioSentinel.git
cd PortfolioSentinel
```

2. **Create a virtual environment (Conda or venv)**
```bash
conda create -n ml_env python=3.11
conda activate ml_env
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the dashboard**
```bash
streamlit run app.py
```
Navigate to `http://localhost:8501` to view the dashboard.

---

## 📂 Project Structure
```text
PortfolioSentinel/
├── app.py                     # Streamlit application entry point
├── config/                    # Global settings and thresholds
├── src/                       # Core analytical modules
│   ├── data_pipeline/         # Data fetching, cleaning, and SQLite logging
│   ├── market_risk/           # Returns, volatility, VaR, Monte Carlo
│   ├── credit_risk/           # PD scoring, expected loss, concentration
│   ├── alerts/                # Alert engine for threshold breaches
│   ├── explainability/        # NLP-style insights for risk factors
│   └── reporting/             # PDF/Excel generation
├── tests/                     # Unit test suite (pytest)
├── data/                      # Raw, synthetic, and SQLite databases
├── pages/                     # Streamlit multi-page UI definitions
├── assets/                    # Custom CSS styling
└── requirements.txt
```

---

## 📝 Disclaimer
*This project relies on publicly available and synthetic datasets. It is designed as a demonstration of analytics, dashboarding, and software engineering skills for quantitative finance, risk management, and fintech roles. It is not intended to provide real investment or credit advice.*
