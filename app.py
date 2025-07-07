import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import requests
from datetime import date
from streamlit.components.v1 import html

# Load ML model
model = joblib.load("flight_price_model.pkl")

# Page config
st.set_page_config(page_title="Air India Fare Master", page_icon="🏢", layout="wide")

# Inject working native canvas particle animation
html(
    '''
    <canvas id="background" style="position:fixed;top:0;left:0;z-index:-1;width:100vw;height:100vh;"></canvas>
    <script>
    const canvas = document.getElementById("background");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const particles = [];

    for (let i = 0; i < 80; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 1,
            vy: (Math.random() - 0.5) * 1,
            r: 2 + Math.random() * 2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ff4b4b";
        for (let p of particles) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, 2 * Math.PI);
            ctx.fill();
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        }
        requestAnimationFrame(draw);
    }

    draw();
    </script>
    ''',
    height=0,
    width=0
)

# Theme toggle
if 'dark' not in st.session_state:
    st.session_state.dark = False

def toggle_theme():
    st.session_state.dark = not st.session_state.dark

st.sidebar.button("🌙 Toggle Dark Mode" if not st.session_state.dark else "☀️ Light Mode", on_click=toggle_theme)

# Apply custom styling
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
body {{
    background-color: {'#111' if st.session_state.dark else '#f4f4f4'};
    color: {'#eee' if st.session_state.dark else '#111'};
    font-family: 'Poppins', sans-serif;
}}
.title-banner {{
    font-size: 3.2rem;
    font-weight: bold;
    background: linear-gradient(90deg, #FF6A00, #EE0979);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin: 2rem 0 1rem;
}}
.animated-card {{
    animation: fadeInUp 1s ease forwards;
    opacity: 0;
    transform: translateY(20px);
}}
@keyframes fadeInUp {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://media.giphy.com/media/3o7TKP0jVZQ3gH6vuQ/giphy.gif", use_container_width=True)
    st.markdown("## 🛫 Flight Info")
    passenger = st.text_input("👤 Passenger Name", "Ashish")
    duration = st.slider("⏱️ Duration (min)", 30, 600, 180, 10)
    stops = st.selectbox("🔁 Stops", [0, 1, 2])
    departure = st.selectbox("🕓 Departure Time", ["Morning", "Afternoon", "Evening", "Night"])
    travel_date = st.date_input("📅 Travel Date", date.today())
    source = st.selectbox("🛫 From", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"])
    dest = st.selectbox("🛬 To", ["Cochin", "Hyderabad", "Delhi", "Mumbai", "Kolkata"])
    submit = st.button(" Predict My Fare")

# Main Title
st.markdown("<div class='title-banner'> Air India Fare Master</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Predict your flight fare with style and AI </p>", unsafe_allow_html=True)

# Main Section
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
    col1.metric(" Predicted Fare", f"₹ {round(predicted_price, 2)}")
    col2.metric(" In USD", f"$ {price_usd}")
    col3.metric(" Travel Day", travel_date.strftime("%A"))

    st.markdown(f"""
<div class='animated-card'>
<p><strong>Passenger:</strong> {passenger}</p>
<p><strong>Trip:</strong> {source} → {dest}</p>
<p><strong>Stops:</strong> {stops} | <strong>Departs:</strong> {departure}</p>
</div>
---
""", unsafe_allow_html=True)

    months = list(range(1, 13))
    seasonal_prices = [predicted_price * (0.8 + 0.4 * ((i - 6) ** 2) / 36) for i in months]
    fig = px.line(x=months, y=seasonal_prices, labels={"x": "Month", "y": "Estimated Price"},
                  title="📈 Seasonal Fare Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("###  Smart Travel Tips")
    if stops == 0:
        st.success(" Non-stop: Best for saving time ⏱️")
    elif stops == 1:
        st.info("💡 1 stop: Possible layover, check airport schedule")
    else:
        st.warning("⚠️ 2+ stops: Expect delays or longer travel time.")
    if duration > 240:
        st.info("👑 Consider booking a premium seat for comfort on longer flights.")

    st.markdown("###  Save Your Quote")
    st.download_button("🧾 Download Fare Info (HTML)",
        data=f"""
        <h3>{source} → {dest}</h3>
        <p>Date: {travel_date}</p>
        <p>Stops: {stops} | Duration: {duration} mins</p>
        <h4>Estimated Fare: ₹ {round(predicted_price, 2)}</h4>
        """,
        file_name="fare_card.html", mime="text/html")

# Footer + About Section
st.markdown("---")
st.markdown("##  About This Project")
st.markdown("""
This web app uses real Air India flight data + machine learning to estimate ticket fares and provide real-time smart travel guidance.

###  What’s Inside:
- ML regression model trained on 5000+ flights
- Seasonality trend visualized with Plotly
- Custom travel tips + downloadable fare card
- Theme toggle for light/dark mode

###  Creator:
**Ashish Sahu**, Final Year BTech, Biomedical Engineering, NIT Rourkela
""")
