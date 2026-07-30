import streamlit as st
import pandas as pd
from src.utils import get_market_data, get_credit_data
from src.data_pipeline.market_data import fetch_fred_rates

st.set_page_config(page_title="Data Explorer - PortfolioSentinel", layout="wide")

st.title("🗄️ Data Explorer")
st.markdown("Inspect raw data pipelines, export datasets, and view macroeconomic indicators.")

tab1, tab2, tab3 = st.tabs(["Market Data", "Credit Portfolio", "Macro Indicators (FRED)"])

with tab1:
    market_df = get_market_data()
    st.subheader(f"Market Data ({market_df.index.min().date()} to {market_df.index.max().date()})")
    st.dataframe(market_df.tail(100), use_container_width=True)
    
    csv = market_df.to_csv().encode('utf-8')
    st.download_button("Download Market Data CSV", data=csv, file_name="market_prices.csv", mime="text/csv")

with tab2:
    credit_df, _ = get_credit_data()
    st.subheader(f"Synthetic Credit Portfolio ({len(credit_df)} Borrowers)")
    st.dataframe(credit_df, use_container_width=True)
    
    csv2 = credit_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Credit Data CSV", data=csv2, file_name="credit_portfolio.csv", mime="text/csv")

with tab3:
    st.subheader("FRED Macroeconomic Indicators")
    st.markdown("Tracking **DGS10**: 10-Year Treasury Constant Maturity Rate")
    
    with st.spinner("Fetching from Federal Reserve Economic Data (FRED)..."):
        fred_df = fetch_fred_rates("DGS10")
        
    st.line_chart(fred_df, height=300)
    st.dataframe(fred_df.tail(10), use_container_width=True)
