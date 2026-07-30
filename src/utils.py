import streamlit as st

from src.credit_risk.exposure import calculate_expected_loss
from src.credit_risk.scoring import (
    assign_credit_rating,
    predict_default_probability,
    train_credit_model,
)
from src.data_pipeline.cleaning import clean_credit_data, clean_market_data
from src.data_pipeline.credit_data import load_credit_portfolio
from src.data_pipeline.market_data import fetch_market_data, load_cached_market_data


@st.cache_data(show_spinner="Loading market data...")
def get_market_data():
    try:
        df = fetch_market_data()
    except Exception:  # noqa: BLE001
        df = load_cached_market_data()
    return clean_market_data(df)


@st.cache_resource(show_spinner="Loading credit portfolio...")
def get_credit_data():
    df = load_credit_portfolio()
    df = clean_credit_data(df)

    # Train/load model and predict PD
    model, _ = train_credit_model(
        df, save_model=False
    )  # For demo, we train on the fly or load
    df["pd"] = predict_default_probability(model, df)
    df["rating"] = df["pd"].apply(assign_credit_rating)
    df = calculate_expected_loss(df)
    return df, model
