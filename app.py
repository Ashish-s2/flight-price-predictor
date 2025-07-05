import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import requests
from datetime import date

# Load the ML model
model = joblib.load("flight_price_model.pkl")

# Page settings
st.set_page_config(page_title="Air India Fare Master", page_icon="✈️", layout="wide")

# Theme toggle with CSS
if 'dark' not in st.session_state:
    st.session_state.dark = False
def toggle_theme():
    st.session_state.dark = not st.session_state.dark
st.sidebar.button("🌙 Toggle Dark Mode" if not st.session_state.dark else "☀️ Light Mode", on_click=toggle_theme)

css = """
<style>
body {color: %s; background-color: %s;}
</style>
""" % (
    ("#EEE" if st.session_state.dark else "#444"),
    ("#222" if st.session_state.dark else "#f4f4f9")
)
st.markdown(css, unsafe_allow_html=True)

# Sidebar banner & inputs
with st.sidebar:
    st.image("https://media.giphy.com/media/QXVcjhflayKw4/giphy.gif", use_column_width=True)
    st.markdown("## 🛫 Flight Info")
    passenger = st.text_input("Name", "Ashish")
    duration = st.slider("Duration (min)", 30, 600, 180, 10)
    stops = st.selectbox("Stops", [0, 1, 2])
    departure = st.selectbox("Departure", ["Morning", "Afternoon", "Evening", "Night"])
    travel_date = st.date_input("Travel Date", date.today())
    source = st.selectbox("From", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"])
    dest = st.selectbox("To", ["Cochin", "Hyderabad", "Delhi", "Mumbai", "Kolkata"])
    submit = st.button("🔮 Predict Fare")

# Main panel
st.title("💸 Air India Fare Master")
st.write("Calculate your estimated ticket price in multiple currencies and get pro tips!")

# Predict section
if submit:
    sample = pd.DataFrame({"Duration_mins": [duration], "Stops_Num": [stops]})
    price = model.predict(sample)[0]

    # Fetch USD rate
    try:
        r = requests.get("https://api.exchangerate.host/latest?base=INR&symbols=USD")
        usd_rate = r.json()["rates"]["USD"]
        price_usd = price * usd_rate
    except:
        price_usd = None

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Price (INR)", f"₹ {round(price,2)}")
    col2.metric("💵 Price (USD)", f"$ {round(price_usd,2)}" if price_usd else "N/A")
    col3.metric("🧭 Travel Date", travel_date.strftime("%b %d, %Y"))

    st.markdown(f"**Passenger:** {passenger} | **Route:** {source} → {dest} | **Departure:** {departure}")

    # Mock historical trend for route
    months = list(range(1,13))
    hist = [price * (0.8 + 0.4*((i-6)**2)/36) for i in months]  # sim price variation
    fig_trend = px.line(x=months, y=hist, labels={"x":"Month","y":"Price INR"},
                        title="📈 Estimated Monthly Price Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

    # Shareable card with HTML & download
    card_html = f"""
    <div style="border:2px solid #ddd;padding:20px;border-radius:10px;text-align:center;
                background-color:{'#333' if st.session_state.dark else '#fff'};color:{'#eee' if st.session_state.dark else '#222'}">
      <h2>✈️ {source} → {dest}</h2>
      <h3>Estimated Fare: ₹ {round(price,2)}</h3>
      <p>{departure}, {stops} stop(s), on {travel_date.strftime('%b %d, %Y')}</p>
      <p>— Enjoy your trip, {passenger}! —</p>
    </div>
    """
    st.download_button("📤 Download Fare Card (PNG)", data=card_html, file_name="fare_card.html", mime="text/html")

    # Flight tips
    tips = []
    if stops == 0: tips.append("Non-stop flight best for time-saving 🕒")
    else: tips.append(f"{stops} stop(s) may increase connection time ⏳")
    if duration > 240: tips.append("Consider premium economy for comfort on long flights.")
    if travel_date.weekday() in [4,5]: tips.append("Weekend travel, expect higher demand — book early!")
    st.markdown("### 🧠 Travel Tips")
    for tip in tips:
        st.markdown(f"- {tip}")

# Footer
st.markdown("---")
st.markdown("<center>Built by **Ashish Sahu** 🚀 | NIT Rourkela | [LinkedIn]</center>", unsafe_allow_html=True)
