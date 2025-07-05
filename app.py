import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Load the model
model = joblib.load("flight_price_model.pkl")

# Page config
st.set_page_config(
    page_title="Air India Fare Predictor",
    page_icon="✈️",
    layout="centered"
)

# Custom title
st.title("💸 Air India Flight Price Predictor")
st.markdown("""
Welcome aboard! 🎫  
This AI-powered app estimates Air India ticket prices based on flight duration and number of stops.  
Just adjust the controls on the left and get your price instantly!  
---
""")

# Sidebar controls
st.sidebar.header("🛫 Customize Your Flight")
duration = st.sidebar.slider("Flight Duration (minutes)", 30, 600, 180, step=10)
stops = st.sidebar.selectbox("Number of Stops", [0, 1, 2], index=1)

# Predict
sample = pd.DataFrame({
    "Duration_mins": [duration],
    "Stops_Num": [stops]
})
predicted_price = model.predict(sample)[0]

# Layout with columns
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://img.icons8.com/clouds/500/airplane-take-off.png", width=120)

with col2:
    st.metric(label="Predicted Ticket Price (INR)", value=f"₹ {round(predicted_price, 2)}")
    st.success(f"🎯 This is the estimated fare for a {duration} min flight with {stops} stop(s).")

# Optional info card
with st.expander("📊 Behind the Scenes"):
    st.markdown("""
    This prediction is powered by a **Linear Regression** model trained on 5,000+ real Air India flights.  
    Features used:
    - ⏱️ Flight Duration  
    - 🔁 Number of Stops  
    This is a simplified version — in real-world deployments, we could add source, destination, class, time of day, etc.
    """)

# Footer
st.markdown("---")
st.markdown("Made with 💙 by **Ashish Sahu** | NIT Rourkela | [LinkedIn](https://linkedin.com)")

