import streamlit as st
import pandas as pd
from src.data_pipeline.database import load_alert_history, init_db
from src.reporting.export import export_alerts_to_excel

st.set_page_config(page_title="Alerts - PortfolioSentinel", layout="wide")

st.title("🚨 Alert Center")
st.markdown("Monitor and audit system-generated risk alerts. All alerts are permanently logged in the SQLite database.")

# Ensure DB exists
try:
    init_db()
    history_df = load_alert_history()
except Exception as e:
    st.error(f"Database error: {e}")
    history_df = pd.DataFrame()

if history_df.empty:
    st.success("No alerts found in the database. Risk levels are within normal bounds.")
else:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Historical Alerts Log")
        
        # Filtering
        sev_filter = st.multiselect("Filter by Severity", ["Critical", "Warning", "Watch"], default=["Critical", "Warning"])
        filtered_df = history_df[history_df["severity"].isin(sev_filter)]
        
        # Apply conditional formatting
        def highlight_severity(val):
            if val == 'Critical': return 'background-color: #4a1515'
            elif val == 'Warning': return 'background-color: #4a3615'
            return ''
            
        st.dataframe(filtered_df.style.map(highlight_severity, subset=['severity']), 
                     use_container_width=True, hide_index=True)
                     
    with col2:
        st.subheader("Actions")
        st.metric("Total Alerts Logged", len(history_df))
        st.metric("Critical Alerts", len(history_df[history_df["severity"] == "Critical"]))
        
        st.markdown("---")
        
        excel_data = export_alerts_to_excel(filtered_df.to_dict('records'))
        st.download_button(
            label="📊 Download Excel Report",
            data=excel_data,
            file_name="active_alerts.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
