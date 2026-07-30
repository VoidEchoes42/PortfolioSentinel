import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import get_credit_data
from src.credit_risk.concentration import sector_concentration
from src.explainability.insights import generate_credit_insight

st.set_page_config(page_title="Credit Risk - PortfolioSentinel", layout="wide")

st.title("🏦 Credit Risk Analytics")

with st.spinner("Loading credit data and models..."):
    credit_df, model = get_credit_data()

tab1, tab2, tab3 = st.tabs(["Portfolio Exposure", "Concentration Risk", "Borrower Drilldown"])

with tab1:
    st.subheader("Expected Loss & Exposure by Rating")
    summary = credit_df.groupby("rating").agg({
        "exposure": "sum",
        "expected_loss": "sum",
        "borrower_id": "count"
    }).reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_exp = px.bar(summary, x="rating", y="exposure", text_auto=".2s", 
                         title="Total Exposure by Rating", template="plotly_dark")
        st.plotly_chart(fig_exp, use_container_width=True)
    with col2:
        fig_el = px.bar(summary, x="rating", y="expected_loss", text_auto=".2s", 
                        title="Expected Loss by Rating", template="plotly_dark", color_discrete_sequence=["#d62728"])
        st.plotly_chart(fig_el, use_container_width=True)

with tab2:
    st.subheader("Sector Concentration")
    conc = sector_concentration(credit_df)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Sector HHI", f"{conc['hhi']:.3f}", 
                  help="Values > 0.25 indicate high concentration.")
        st.dataframe(conc['exposures'].sort_values(ascending=False).to_frame().style.format("${:,.0f}"))
        
    with col2:
        fig_pie = px.pie(values=conc['exposures'].values, names=conc['exposures'].index, 
                         hole=0.4, template="plotly_dark", title="Exposure Breakdown by Sector")
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("Borrower Intelligence")
    selected_borrower = st.selectbox("Select a Borrower ID to investigate", credit_df["borrower_id"].tolist())
    
    borrower_data = credit_df[credit_df["borrower_id"] == selected_borrower].iloc[0]
    
    b_col1, b_col2, b_col3 = st.columns(3)
    b_col1.metric("Rating", borrower_data["rating"])
    b_col2.metric("Exposure", f"${borrower_data['exposure']:,.0f}")
    b_col3.metric("Probability of Default", f"{borrower_data['pd']:.2%}")
    
    st.markdown("### AI Insight")
    st.info(generate_credit_insight(borrower_data))
    
    st.markdown("### Financial Ratios")
    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("Leverage Ratio", f"{borrower_data['leverage_ratio']:.2f}x")
    r_col2.metric("Interest Coverage", f"{borrower_data['interest_coverage']:.2f}x")
    r_col3.metric("Revenue Growth", f"{borrower_data['revenue_growth']:.2%}")
