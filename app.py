import streamlit as st
import pandas as pd
import pickle

st.set_page_config("Predictive Delivery Optimizer", layout="wide")

model = pickle.load(open("delay_model.pkl", "rb"))

st.title("Predictive Delivery Optimizer")

st.sidebar.header("Order Inputs")

distance = st.sidebar.number_input("Distance (KM)", 1.0, 3000.0)
fuel = st.sidebar.number_input("Fuel Consumption (L)", 1.0, 500.0)
traffic = st.sidebar.slider("Traffic Delay (Minutes)", 0, 240)
cost = st.sidebar.number_input("Delivery Cost (INR)", 100.0, 50000.0)
order_value = st.sidebar.number_input("Order Value (INR)", 100.0, 100000.0)
fuel_cost = st.sidebar.number_input("Fuel Cost (INR)", 50.0, 20000.0)
labor_cost = st.sidebar.number_input("Labor Cost (INR)", 50.0, 20000.0)
priority = st.sidebar.selectbox("Priority", ["Economy", "Standard", "Express"])

priority_map = {"Economy": 0, "Standard": 1, "Express": 2}

input_df = pd.DataFrame([[
    distance,
    fuel,
    traffic,
    cost,
    priority_map[priority],
    order_value,
    fuel_cost,
    labor_cost
]], columns=[
    "distance_km",
    "fuel_consumption_l",
    "traffic_delay_minutes",
    "delivery_cost_inr",
    "priority",
    "order_value_inr",
    "fuel_cost",
    "labor_cost"
])

if st.button("Predict Delay Risk"):
    result = model.predict(input_df)[0]

    if result == 1:
        st.error("High Risk of Delay")
        st.markdown("""
        **Recommended Actions**
        - Upgrade delivery priority
        - Use faster carrier
        - Avoid high traffic routes
        """)
    else:
        st.success("Delivery On Track")

st.subheader("Input Overview")
st.bar_chart(input_df.T)
