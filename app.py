import streamlit as st

st.set_page_config(
    page_title="PortfolioSentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load CSS
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css()

st.title("🛡️ PortfolioSentinel")
st.subheader("Market & Credit Risk Dashboard")

st.markdown("""
Welcome to **PortfolioSentinel**, an end-to-end risk analytics platform.
Please use the sidebar to navigate through the different risk modules.

### Modules:
1. **Overview**: Executive summary and high-level KPIs.
2. **Market Risk**: Volatility, VaR, correlations, and drawdowns.
3. **Credit Risk**: PD modeling, expected loss, and concentration.
4. **Stress Testing**: Scenario analysis on the portfolio.
5. **Alerts**: Active threshold breaches and warnings.
6. **Data Explorer**: Raw data access and quality checks.
""")

st.sidebar.info("Select a page above to begin.")
st.sidebar.markdown("---")
st.sidebar.text("© 2026 PortfolioSentinel")
