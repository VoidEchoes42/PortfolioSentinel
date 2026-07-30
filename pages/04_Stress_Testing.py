import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.utils import get_market_data
from src.market_risk.stress_testing import SCENARIOS, apply_stress_scenario
from config.settings import SECTOR_MAPPING

st.set_page_config(page_title="Stress Testing - PortfolioSentinel", layout="wide")

st.title("⚡ Stress Testing Engine")
st.markdown("Simulate the impact of extreme historical and hypothetical market events on the portfolio.")

market_df = get_market_data()
weights = {ticker: 1/len(market_df.columns) for ticker in market_df.columns}

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select Scenario")
    scenario_name = st.selectbox("Scenario", list(SCENARIOS.keys()))
    
    st.markdown("### Scenario Shocks")
    shocks = SCENARIOS[scenario_name]
    shock_df = pd.DataFrame(list(shocks.items()), columns=["Sector", "Shock Applied"])
    shock_df["Shock Applied"] = shock_df["Shock Applied"].apply(lambda x: f"{x:.1%}")
    st.dataframe(shock_df, hide_index=True)

with col2:
    st.subheader("Portfolio Impact")
    results = apply_stress_scenario(weights, SECTOR_MAPPING, scenario_name)
    
    loss_val = results["total_portfolio_return"]
    color = "red" if loss_val < 0 else "green"
    
    st.markdown(f"""
    <div style="padding: 20px; background-color: #1e2129; border-radius: 10px; text-align: center;">
        <h2 style="margin: 0; color: #a0aab5;">Estimated Portfolio Impact</h2>
        <h1 style="margin: 10px 0 0 0; color: {color}; font-size: 3rem;">{loss_val:.2%}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Asset-Level Attribution")
    detail_df = pd.DataFrame.from_dict(results["asset_details"], orient="index").reset_index()
    detail_df.rename(columns={"index": "Ticker"}, inplace=True)
    
    fig = px.bar(detail_df, x="Ticker", y="Contribution to Portfolio Return", color="Sector", 
                 template="plotly_dark", title="P&L Contribution by Asset")
    st.plotly_chart(fig, use_container_width=True)
