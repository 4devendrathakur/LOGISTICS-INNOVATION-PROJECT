import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Delivery Risk Intelligence",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #e5e7eb;
    }
    h1, h2, h3 {
        color: #38bdf8;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    section[data-testid="stSidebar"] {
        background-color: #020617;
    }
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------

# Load model
model = pickle.load(open("delay_model.pkl", "rb"))

st.title("🚚 Delivery Risk Intelligence Dashboard")
st.caption("AI-powered prediction for logistics delay management")

st.sidebar.header("📦 Order Parameters")

distance = st.sidebar.number_input("Distance (KM)", 1.0, 3000.0)
fuel = st.sidebar.number_input("Fuel Usage (Liters)", 1.0, 500.0)
traffic = st.sidebar.slider("Traffic Impact (Minutes)", 0, 240)
cost = st.sidebar.number_input("Delivery Cost (INR)", 100.0, 50000.0)
order_value = st.sidebar.number_input("Order Value (INR)", 100.0, 100000.0)
fuel_cost = st.sidebar.number_input("Fuel Cost (INR)", 50.0, 20000.0)
labor_cost = st.sidebar.number_input("Labor Cost (INR)", 50.0, 20000.0)
priority = st.sidebar.selectbox(
    "Delivery Priority",
    ["Economy", "Standard", "Express"]
)

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

st.markdown("---")

if st.button("🔍 Analyze Delivery Risk"):
    result = model.predict(input_df)[0]

    if result == 1:
        st.error("⚠️ High Probability of Delivery Delay")
        st.markdown("""
        **Suggested Optimization Steps**
        - Increase delivery priority
        - Reroute via low-traffic paths
        - Assign high-speed carrier
        """)
    else:
        st.success("✅ Delivery is Operating Within Expected Time")

st.subheader("📊 Order Feature Snapshot")
st.bar_chart(input_df.T)
