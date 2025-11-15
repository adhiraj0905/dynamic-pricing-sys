# File: dashboard.py

import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Dynamic Pricing Dashboard",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Dynamic Ride-Pricing Dashboard")
st.markdown("Use this dashboard to simulate a ride request and find the optimal price.")

# --- API URL ---
# This is the endpoint for our running FastAPI app
API_URL = "http://127.0.0.1:8000/optimize-price/"

# --- Input Fields ---
st.header("Ride Details")

# We use columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    distance = st.number_input("Distance (km)", min_value=1.0, max_value=100.0, value=10.5, step=0.1)
    time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"], index=1)
    weather = st.selectbox("Weather", ["Clear", "Rainy", "Snowy"], index=0)

with col2:
    base_price = st.number_input("Base Price ($)", min_value=5.0, max_value=50.0, value=15.0, step=0.5)
    weather_multiplier = st.slider("Weather Multiplier", min_value=1.0, max_value=3.0, value=1.0, step=0.1)


# --- The "Get Price" Button ---
if st.button("Get Optimal Price", type="primary"):

    # 1. Create the request payload (the JSON to send)
    ride_request = {
        "Distance": distance,
        "Time_of_Day": time_of_day,
        "Weather": weather,
        "Base_Price": base_price,
        "Weather_Multiplier": weather_multiplier
    }

    # 2. Call the FastAPI
    try:
        with st.spinner("Calling API..."):
            response = requests.post(API_URL, data=json.dumps(ride_request))

        if response.status_code == 200:
            # 3. Display the result
            result = response.json()

            st.subheader("🎉 Optimal Price Found!")

            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric(label="Optimal Price", value=f"${result['optimal_price']:.2f}")
            col_res2.metric(label="Predicted Demand", value=f"{result['predicted_demand']:.2f} rides")
            col_res3.metric(label="Estimated Revenue", value=f"${result['estimated_revenue']:.2f}")

        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Could not connect to the API.")
        st.warning("Please make sure the FastAPI server is running on 'http://127.0.0.1:8000'")