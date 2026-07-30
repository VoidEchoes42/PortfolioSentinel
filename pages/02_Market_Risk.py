import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.utils import get_market_data
from src.market_risk.returns import compute_daily_returns, compute_cumulative_returns, compute_drawdown
from src.market_risk.volatility import rolling_volatility, compute_correlation_matrix
from src.market_risk.var_cvar import historical_var, parametric_var, historical_cvar
from src.market_risk.monte_carlo import run_monte_carlo_simulation

st.set_page_config(page_title="Market Risk - PortfolioSentinel", layout="wide")

st.title("📈 Market Risk Analytics")

with st.spinner("Loading market data..."):
    market_df = get_market_data()
    returns = compute_daily_returns(market_df)
    weights = np.ones(len(returns.columns)) / len(returns.columns)

st.sidebar.header("Market Controls")
mc_sims = st.sidebar.slider("Monte Carlo Simulations", 500, 5000, 1000, step=500)

tab1, tab2, tab3 = st.tabs(["Performance & Drawdown", "Volatility & Correlation", "VaR & Monte Carlo"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cumulative Returns")
        cum_ret = compute_cumulative_returns(returns)
        fig = px.line(cum_ret, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Drawdown Analysis")
        drawdown = compute_drawdown(market_df)
        fig2 = px.area(drawdown, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rolling Volatility (21-Day)")
        roll_vol = rolling_volatility(returns)
        fig_vol = px.line(roll_vol, template="plotly_dark")
        st.plotly_chart(fig_vol, use_container_width=True)
        
    with col2:
        st.subheader("Asset Correlation Matrix")
        corr = compute_correlation_matrix(returns)
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto", template="plotly_dark", color_continuous_scale="RdBu_r")
        st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.subheader("Value at Risk (VaR)")
    port_ret = returns.dot(weights)
    
    colA, colB, colC = st.columns(3)
    colA.metric("Historical VaR (95%)", f"{historical_var(port_ret):.2%}")
    colB.metric("Parametric VaR (95%)", f"{parametric_var(port_ret):.2%}")
    colC.metric("Expected Shortfall (CVaR)", f"{historical_cvar(port_ret):.2%}")
    
    st.markdown("---")
    st.subheader("Monte Carlo Simulation (21-Day Horizon)")
    
    with st.spinner("Running Monte Carlo..."):
        mc_results = run_monte_carlo_simulation(returns, weights, num_simulations=mc_sims)
        
    colX, colY = st.columns([2, 1])
    with colX:
        fig_mc = px.histogram(mc_results["final_returns"], nbins=50, template="plotly_dark", 
                              title="Distribution of Simulated Portfolio Returns")
        fig_mc.add_vline(x=-mc_results["var_95"], line_dash="dash", line_color="red", annotation_text="95% VaR")
        st.plotly_chart(fig_mc, use_container_width=True)
        
    with colY:
        st.metric("Simulated 95% VaR", f"{mc_results['var_95']:.2%}")
        st.metric("Simulated 99% VaR", f"{mc_results['var_99']:.2%}")
        st.metric("Simulated CVaR", f"{mc_results['cvar_95']:.2%}")
        st.info("The Monte Carlo simulation projects potential portfolio outcomes over the next 21 trading days assuming multivariate normal distributions.")
