import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle


# Load datasets
orders = pd.read_csv("data/orders.csv")
delivery = pd.read_csv("data/delivery_performance.csv")
routes = pd.read_csv("data/routes_distance.csv")
costs = pd.read_csv("data/cost_breakdown.csv")

# Clean column names

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

# Merge datasets on order_id
df = orders.merge(delivery, on="order_id", how="inner")
df = df.merge(routes, on="order_id", how="inner")
df = df.merge(costs, on="order_id", how="inner")

# Handle missing values
df.fillna(df.median(numeric_only=True), inplace=True)
df.fillna("none", inplace=True)

# Target variable

df["delayed"] = (
    df["actual_delivery_days"] > df["promised_delivery_days"]
).astype(int)

# Encode Priority
df["priority"] = df["priority"].map({
    "economy": 0,
    "standard": 1,
    "express": 2
})

# Feature selection
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

# Train-test split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)
model.fit(X_train, y_train)

# Save model
MODEL_PATH = os.path.join("model", "delay_model.pkl")
model = pickle.load(open(MODEL_PATH, "rb"))


print("Model trained successfully with real logistics data")
