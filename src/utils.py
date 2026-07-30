import streamlit as st
import pandas as pd
from src.data_pipeline.market_data import fetch_market_data, load_cached_market_data
from src.data_pipeline.credit_data import load_credit_portfolio
from src.data_pipeline.cleaning import clean_market_data, clean_credit_data
from src.credit_risk.scoring import train_credit_model, predict_default_probability, assign_credit_rating
from src.credit_risk.exposure import calculate_expected_loss

@st.cache_data(show_spinner="Loading market data...")
def get_market_data():
    try:
        df = fetch_market_data()
    except Exception:
        df = load_cached_market_data()
    return clean_market_data(df)

@st.cache_data(show_spinner="Loading credit portfolio...")
def get_credit_data():
    df = load_credit_portfolio()
    df = clean_credit_data(df)
    
    # Train/load model and predict PD
    model, _ = train_credit_model(df, save_model=False) # For demo, we train on the fly or load
    df["pd"] = predict_default_probability(model, df)
    df["rating"] = df["pd"].apply(assign_credit_rating)
    df = calculate_expected_loss(df)
    return df, model
