 Air India Flight Price Analysis & Prediction  
**EDA + Machine Learning + Streamlit App**
A smart and stylish Streamlit app that predicts flight ticket prices using machine learning — built with ❤️ by Ashish Sahu.

## Live Demo
[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen?logo=streamlit)](https://flight-price-predictor-1.streamlit.app/)

---
This project explores real flight fare data for **Air India**, covering 5,000+ domestic flights in 2019.  
We analyze trends, visualize pricing patterns, and build a machine learning model to predict flight ticket prices — all wrapped in a sleek Streamlit app 

---

##  Project Structure

 air-india-price-analysis/
├── air_india.csv # Cleaned dataset
├── Air_India.ipynb # Jupyter notebook with analysis + ML
├── flight_price_model.pkl # Saved ML model (joblib)
├── app.py # Streamlit app to predict flight price
├── README.md # This file


---

##  Project Goals

-  Explore Air India's flight fare patterns  
-  Identify how duration, stops, and routes affect pricing  
-  Build a regression model to predict ticket prices  
-  Launch a Streamlit app for real-time predictions

---

##  Features & Visuals

- Month-over-Month price trend  
- Route-wise pricing patterns  
- Price distribution histograms  
- Duration vs Price + Stops vs Price analysis  
- Prediction using Linear Regression  
- Optional Streamlit app with user input

---

##  How to Run

###  Jupyter Notebook
1. Open `Air_India_EDA.ipynb` in Jupyter  
2. Run all cells to explore visuals + ML  
3. View results and insights  

###  Streamlit Web App
1. Save your trained model:
   ```python
   import joblib  
   joblib.dump(model, "flight_price_model.pkl")
## Run the app:

bash
Copy
Edit
streamlit run app.py
Choose duration + stops → Get predicted price 

## Technologies Used
Python

Pandas, NumPy

Seaborn, Matplotlib

Scikit-learn (Linear Regression)

Streamlit

Joblib

## What I Learned
Feature engineering from raw data

Visualization techniques using Seaborn

Machine learning model training + evaluation

Building and deploying a Streamlit app

How to present insights in a business-ready format

## Future Improvements
Use more features (e.g., Source/Destination/Time) for prediction

Try advanced models like Random Forest, XGBoost

Deploy Streamlit app online via Streamlit Cloud

Create an interactive dashboard using Plotly or Dash

## Try It Yourself
Clone this repo

Open the notebook to explore insights

Run streamlit run app.py and predict your own Air India fare!

## Author
Ashish Sahu
Final Year BTech, Biomedical Engineering
NIT Rourkela
 LinkedIn |  6372671@gmail.com

