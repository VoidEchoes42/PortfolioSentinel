import streamlit as st
import numpy as np
from src.utils import get_market_data, get_credit_data
from src.market_risk.returns import compute_daily_returns, portfolio_returns
from src.market_risk.volatility import rolling_volatility
from src.market_risk.var_cvar import historical_var
from src.alerts.engine import check_market_alerts, check_credit_alerts, get_top_risks
from src.credit_risk.concentration import calculate_hhi
from src.credit_risk.watchlist import generate_watchlist
from src.explainability.insights import generate_portfolio_summary
from src.data_pipeline.database import init_db, log_alerts, log_risk_snapshot

st.set_page_config(page_title="Overview - PortfolioSentinel", layout="wide")

try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError: pass

st.title("Executive Overview")

with st.spinner("Loading analytics..."):
    market_df = get_market_data()
    credit_df, _ = get_credit_data()
    
    # Calculate basic market metrics
    returns = compute_daily_returns(market_df)
    weights = np.ones(len(returns.columns)) / len(returns.columns)
    port_ret = portfolio_returns(returns, weights)
    
    current_vol = port_ret.std() * np.sqrt(252)
    var_95 = historical_var(port_ret)
    drawdown = (market_df.sum(axis=1) / market_df.sum(axis=1).cummax() - 1).min()
    
    # Calculate basic credit metrics
    total_exposure = credit_df["exposure"].sum()
    total_el = credit_df["expected_loss"].sum()
    sector_hhi = calculate_hhi(credit_df.groupby("sector")["exposure"].sum())
    watchlist = generate_watchlist(credit_df)
    
    # Generate Alerts
    mkt_metrics = {"volatility": current_vol, "drawdown": abs(drawdown), "var_95": var_95}
    cred_metrics = {"hhi": sector_hhi, "watchlist_count": len(watchlist)}
    
    all_alerts = check_market_alerts(mkt_metrics) + check_credit_alerts(cred_metrics)
    
    # Persist alerts and risk snapshot to SQLite
    init_db()
    log_alerts(all_alerts)
    log_risk_snapshot(total_exposure, var_95, total_el, len(all_alerts))
    top_risks = get_top_risks(all_alerts, 3)

# --- KPI ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Total Exposure</h3>
        <h1>${total_exposure/1e6:,.1f}M</h1>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>1-Day VaR (95%)</h3>
        <h1>{var_95:.2%}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Expected Credit Loss</h3>
        <h1>${total_el/1e6:,.2f}M</h1>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    color = "#ff4b4b" if len(all_alerts) > 0 else "#2ca02c"
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid {color};">
        <h3>Active Alerts</h3>
        <h1 style="color: {color};">{len(all_alerts)}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SUMMARY & TOP RISKS ---
colA, colB = st.columns([2, 1])

with colA:
    st.subheader("Portfolio Summary")
    summary = generate_portfolio_summary(current_vol, var_95, total_el, len(all_alerts))
    st.info(summary)
    
    st.subheader("Market Trend")
    st.line_chart((1 + port_ret).cumprod(), height=250, use_container_width=True)

with colB:
    st.subheader("Top Risk Factors")
    if not top_risks:
        st.success("No critical risks detected.")
    else:
        for alert in top_risks:
            severity = alert['severity'].lower()
            st.markdown(f"""
            <div style="background-color: #1e2129; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {'#ff4b4b' if severity=='critical' else '#ffb74d'};">
                <span class="badge-{severity}">{alert['severity']}</span> <strong>{alert['category']}</strong><br/>
                <span style="color: #ccc; font-size: 0.9em;">{alert['message']}</span>
            </div>
            """, unsafe_allow_html=True)
