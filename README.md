# PortfolioSentinel

**Enterprise Market & Credit Risk Dashboard**

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![Build](https://github.com/VoidEchoes42/PortfolioSentinel/actions/workflows/ci.yml/badge.svg)

## ✨ Why PortfolioSentinel?

Banks monitor thousands of financial assets and loans every day. 

Analysts spend significant time gathering market data, calculating risk metrics, monitoring concentration, and preparing reports for stakeholders.

**PortfolioSentinel** automates this workflow by integrating market risk analytics, credit risk assessment, automated alerts, and reporting into a single, cohesive platform. Built with Python and Streamlit, it provides portfolio managers with timely visibility into potential losses, helping analysts estimate downside risk under both normal and stressed market conditions.

---

> **[TODO: Insert a 30-second GIF here showing: Filters -> Charts update -> Alert appears -> Export PDF -> Download Excel]**

---

## 🏗️ System Architecture

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

For a deeper dive into the system design, assumptions, and math, check out the `docs/` folder:
- [Architecture & Data Flow](docs/architecture.md)
- [Methodologies & Math Assumptions](docs/methodology.md)
- [Design Decisions & Trade-offs](docs/design-decisions.md)

---

## 📊 Results & Scale

- **1000** Monte Carlo simulated paths
- **15** live portfolio assets tracked via `yfinance`
- **30 years** of historical pricing data ingested
- **21-day** rolling volatility horizons
- **5** predefined macroeconomic stress scenarios
- **200+** synthetic corporate borrowers scored
- **95% and 99%** Value at Risk (VaR) confidence intervals
- **50+** automated alerts processed seamlessly
- **<2 seconds** to generate comprehensive PDF reports

---

## 🚀 Core Features

### 📈 Market Risk
Portfolio managers need timely visibility into potential losses. PortfolioSentinel automates the computation of market tail risk.
- **Value at Risk (VaR)**: Calculates both historical and parametric VaR to estimate potential downside under normal conditions.
- **Monte Carlo Simulation**:
  - 1000 simulated paths using Cholesky Decomposition for correlated assets.
  - 21-day forecast horizon.
  - 95% confidence interval outputs.
- **Stress Testing**: Assesses portfolio resilience against historical shocks (e.g., 2008 Financial Crisis) to fulfill regulatory stress-testing requirements.

### 🏦 Credit Risk
Lenders must continuously monitor borrower health to anticipate defaults. This module scores borrowers based on real-time financial ratios.
- **Credit Risk Model**:
  - Scikit-learn Logistic Regression
  - ROC-AUC performance tracking
  - Feature Importance extraction (e.g., Leverage, Interest Coverage)
  - Confusion Matrix heatmaps
  - Probability of Default (PD) scoring mapped to Expected Credit Loss (ECL).
- **Concentration Risk**: Evaluates sector-level exposure using the Herfindahl-Hirschman Index (HHI) to prevent overexposure to single industries.

### 🚨 Automation & Reporting
Manual reporting is error-prone. The Alert Engine automates surveillance.
- **Alert Engine**: Actively monitors portfolios against configurable thresholds (VaR breaches, volatility spikes) and logs them to a local SQLite database to prevent UI freezing.
- **Exportable Reports**: Generate PDF risk summaries and Excel alert logs for stakeholder reporting in under 2 seconds.

---

## 📸 Dashboard Screenshots

*(Note: Replace these placeholders with actual screenshots)*

**1. Executive Overview**
> **[TODO: Add Screenshot of Dashboard Overview]**

**2. Market Risk Analytics**
> **[TODO: Add Screenshot of Market Risk Page]**

**3. Credit Risk & Probability of Default**
> **[TODO: Add Screenshot of Credit Risk Page]**

**4. Automated Alerts Engine**
> **[TODO: Add Screenshot of Alerts Page]**

**5. PDF Report Generation**
> **[TODO: Add Screenshot of PDF Report output]**

---

## 🗺️ Roadmap

- [x] Market Risk (VaR, Volatility, Drawdowns)
- [x] Credit Risk (ML Scoring, ECL, HHI)
- [x] Automated Alert Engine
- [x] PDF & Excel Reporting Exports
- [ ] Basel III Capital Calculator
- [ ] Liquidity Coverage Ratio
- [ ] Interest Rate Risk
- [ ] Multi-Portfolio Support
- [ ] Authentication
- [ ] Cloud Deployment

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

## 📝 Disclaimer
*This project relies on publicly available and synthetic datasets. It is designed as a demonstration of analytics, dashboarding, and software engineering skills for quantitative finance, risk management, and fintech roles. It is not intended to provide real investment or credit advice.*
