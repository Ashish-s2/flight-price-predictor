import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import requests
from datetime import date

# Load ML model
model = joblib.load("flight_price_model.pkl")

# Load Lottie animation
@st.cache_data
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets10.lottiefiles.com/packages/lf20_touohxv0.json"  # Flight animation
lottie_json = load_lottieurl(lottie_url)

# Page config
st.set_page_config(page_title="Air India Fare Master", page_icon="🏢", layout="wide")

# Theme toggle
if 'dark' not in st.session_state:
    st.session_state.dark = False

def toggle_theme():
    st.session_state.dark = not st.session_state.dark

st.sidebar.button("🌙 Toggle Dark Mode" if not st.session_state.dark else "☀️ Light Mode", on_click=toggle_theme)

# Apply theme CSS
st.markdown(f"""
<style>
body {{
    background-color: {'#222' if st.session_state.dark else '#f4f4f9'};
    color: {'#eee' if st.session_state.dark else '#222'};
}}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://media.giphy.com/media/QXVcjhflayKw4/giphy.gif", use_container_width=True)
    st.markdown("##  Flight Info")
    passenger = st.text_input(" Passenger Name", "Ashish")
    duration = st.slider(" Duration (min)", 30, 600, 180, 10)
    stops = st.selectbox(" Stops", [0, 1, 2])
    departure = st.selectbox(" Departure Time", ["Morning", "Afternoon", "Evening", "Night"])
    travel_date = st.date_input("🗕️ Travel Date", date.today())
    source = st.selectbox(" From", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"])
    dest = st.selectbox(" To", ["Cochin", "Hyderabad", "Delhi", "Mumbai", "Kolkata"])
    submit = st.button(" Predict My Fare")

# Title
st.title("💸 Air India Fare Master")
st.write("Predict your Air India flight fare in seconds using machine learning ✈️🧠")

# Add Hero Animation
st.image("https://media.giphy.com/media/QXVcjhflayKw4/giphy.gif", use_container_width=True)


if submit:
    input_df = pd.DataFrame({"Duration_mins": [duration], "Stops_Num": [stops]})
    predicted_price = model.predict(input_df)[0]

    try:
        res = requests.get("https://api.exchangerate.host/latest?base=INR&symbols=USD")
        usd_rate = res.json()["rates"]["USD"]
        price_usd = round(predicted_price * usd_rate, 2)
    except:
        price_usd = "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Predicted Fare", f"₹ {round(predicted_price, 2)}")
    col2.metric("💵 In USD", f"$ {price_usd}")
    col3.metric("🗕️ Travel Day", travel_date.strftime("%A"))

    st.markdown(f"""
**Passenger:** {passenger}  
**Trip:** {source} → {dest} | **Stops:** {stops} | **Departs:** {departure}  
---
""")

    months = list(range(1, 13))
    seasonal_prices = [predicted_price * (0.8 + 0.4 * ((i - 6) ** 2) / 36) for i in months]
    fig = px.line(x=months, y=seasonal_prices, labels={"x": "Month", "y": "Estimated Price"},
                  title="📈 Seasonal Fare Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Smart Travel Tips")
    if stops == 0:
        st.success("✅ Non-stop: Best for saving time ⏱️")
    elif stops == 1:
        st.info("💡 1 stop: Possible layover, check airport schedule")
    else:
        st.warning("⚠️ 2+ stops: Expect delays or longer travel time.")
    if duration > 240:
        st.info("👑 Consider booking a premium seat for comfort on longer flights.")

    st.markdown("### 📄 Save Your Quote")
    st.download_button("📄 Download Fare Info (HTML)",
        data=f"""
        <h3>{source} → {dest}</h3>
        <p>Date: {travel_date}</p>
        <p>Stops: {stops} | Duration: {duration} mins</p>
        <h4>Estimated Fare: ₹ {round(predicted_price, 2)}</h4>
        """,
        file_name="fare_card.html", mime="text/html")

# Footer + About Section
st.markdown("---")
st.markdown("## 🧠 About This Project")
st.markdown("""
Built using real flight data and machine learning to predict ticket prices like a pro travel engine.  
Built by **Ashish Sahu** | NIT Rourkela  

### 📚 Highlights:
- Linear regression model trained on 5,000+ entries
- Streamlit for frontend & Plotly for visualizations
- Custom tips, multi-currency support, and download feature

### 🌟 Best For:
- Final year projects
- Portfolio display
- AI/ML internship demos
- Resume boosters

Thanks for flying with **Fare Master** ✈️
""")
