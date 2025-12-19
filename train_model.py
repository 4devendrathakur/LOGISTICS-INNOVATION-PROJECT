import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# ---------------- LOAD DATA ----------------
orders = pd.read_csv("data/orders.csv")
delivery = pd.read_csv("data/delivery_performance.csv")
routes = pd.read_csv("data/routes_distance.csv")
costs = pd.read_csv("data/cost_breakdown.csv")

# ---------------- CLEAN COLUMNS ----------------
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

orders = clean_columns(orders)
delivery = clean_columns(delivery)
routes = clean_columns(routes)
costs = clean_columns(costs)

# ---------------- MERGE DATA ----------------
df = orders.merge(delivery, on="order_id", how="inner")
df = df.merge(routes, on="order_id", how="inner")
df = df.merge(costs, on="order_id", how="inner")

# ---------------- HANDLE MISSING VALUES ----------------
df.fillna(df.median(numeric_only=True), inplace=True)
df.fillna("none", inplace=True)

# ---------------- TARGET VARIABLE ----------------
df["delayed"] = (
    df["actual_delivery_days"] > df["promised_delivery_days"]
).astype(int)

# ---------------- ENCODE PRIORITY ----------------
df["priority"] = df["priority"].map({
    "economy": 0,
    "standard": 1,
    "express": 2
})

# ---------------- FEATURE SELECTION ----------------
features = [
    "distance_km",
    "fuel_consumption_l",
    "traffic_delay_minutes",
    "delivery_cost_inr",
    "priority",
    "order_value_inr",
    "fuel_cost",
    "labor_cost"
]

X = df[features]
y = df["delayed"]

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL TRAINING ----------------
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)
model.fit(X_train, y_train)

# ---------------- SAVE MODEL ----------------
MODEL_PATH = os.path.join("model", "delay_model.pkl")
pickle.dump(model, open(MODEL_PATH, "wb"))

print("✅ Logistics Delay Prediction Model Trained Successfully")
