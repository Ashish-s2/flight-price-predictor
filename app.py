import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Load trained model (you must save it from your notebook first)
model = joblib.load("flight_price_model.pkl")

# App Title
st.title("✈️ Air India Flight Fare Predictor")

# User Inputs
duration = st.slider("Flight Duration (minutes)", min_value=30, max_value=600, value=180, step=10)
stops = st.selectbox("Number of Stops", [0, 1, 2])

# Predict button
if st.button("Predict Fare"):
    sample = pd.DataFrame({
        "Duration_mins": [duration],
        "Stops_Num": [stops]
    })
    predicted_price = model.predict(sample)[0]
    st.success(f"💰 Estimated Ticket Price: ₹ {round(predicted_price, 2)}")
