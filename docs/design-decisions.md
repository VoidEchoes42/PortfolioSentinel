# Design Decisions & Trade-offs

Building a production-grade risk application requires balancing performance, accuracy, and engineering velocity. Below are the key technical decisions made for PortfolioSentinel and the reasoning behind them.

## 1. Why Streamlit for the Frontend?
**Decision**: Use Streamlit instead of React/Vue + FastAPI.
**Reasoning**: 
- **Velocity**: Streamlit allows for the rapid development of data-heavy dashboards entirely in Python.
- **Data Locality**: The frontend code runs in the same process as the backend data science libraries (Pandas, Scikit-learn), eliminating the need for complex serialization and REST API overhead.
- **Trade-off**: Streamlit's state-driven re-render execution model can be sluggish for highly interactive, consumer-facing web apps. However, for internal B2B dashboards used by analysts, the tradeoff is overwhelmingly positive.

## 2. Why SQLite for Persistence?
**Decision**: Use SQLite instead of PostgreSQL or MongoDB.
**Reasoning**:
- **Simplicity**: SQLite is file-based, requiring zero infrastructure or network configuration, making the project highly portable and easy to run locally.
- **Workload**: The application primarily performs batch writes (daily risk snapshots and periodic alert logging) rather than high-frequency transactional (OLTP) workloads.
- **Trade-off**: SQLite struggles with high concurrent write loads (database locking). We mitigated this by aggregating alerts at the portfolio level before writing to the database, drastically reducing the volume of concurrent `INSERT` operations.

## 3. Why NumPy Vectorization over Pandas/Loops?
**Decision**: Write core mathematical engines (like the Monte Carlo simulator) using native NumPy arrays rather than Pandas DataFrames or standard Python loops.
**Reasoning**:
- **Performance**: Python `for` loops are notoriously slow. By dropping down to NumPy (which runs optimized C/C++ and Fortran under the hood), we achieved a massive performance boost.
- **Result**: During stress testing, the application successfully computed 450,000 Monte Carlo simulations across 15 assets and a 21-day horizon (over 140 million floating-point operations) in a fraction of a second without throwing an Out-of-Memory (OOM) error or freezing the UI.

## 4. Why Logistic Regression for Credit Risk?
**Decision**: Use `LogisticRegression` instead of complex ensemble methods (like XGBoost) or Deep Learning.
**Reasoning**:
- **Explainability**: In financial risk management, regulatory compliance (e.g., Basel III) requires models to be strictly explainable. Logistic Regression allows us to extract exact coefficients for feature importance, meaning we can precisely explain *why* a borrower was flagged for default (e.g., "due to a 6.5x leverage ratio").
- **Trade-off**: Deep learning might capture non-linear relationships slightly better, but the loss of interpretability (the "black box" problem) makes it unsuitable for this specific regulatory context.
