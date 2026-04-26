import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("final_dataset_1000.csv")

print("\nColumns in dataset:\n", df.columns)

# =========================
# ENCODE CATEGORICAL DATA
# =========================
le_location = LabelEncoder()
le_loc_type = LabelEncoder()
le_context = LabelEncoder()

df["location_enc"] = le_location.fit_transform(df["location_name"])
df["location_type_enc"] = le_loc_type.fit_transform(df["location_type"])
df["context_type_enc"] = le_context.fit_transform(df["context_type"])

# =========================
# FEATURES & TARGET
# =========================
X = df[[
    "location_enc",
    "location_type_enc",
    "context_type_enc",
    "hour",
    "weekday",
    "month",
    "is_weekend",
    "is_holiday",
    "is_sunset_time",
    "is_nightlife_time",
    "is_office_rush",
    "season_factor"
]]

y = df["crowd_density"]

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL COMPARISON
# =========================
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(random_state=42)
}

best_model = None
best_score = -1
results = []

print("\n===== MODEL COMPARISON =====\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)

    results.append({
        "Model": name,
        "R2 Score": round(r2, 3),
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3)
    })

    print(f"{name}")
    print(f"R2 Score : {r2:.3f}")
    print(f"MAE      : {mae:.3f}")
    print(f"RMSE     : {rmse:.3f}")
    print("-" * 35)

    if r2 > best_score:
        best_score = r2
        best_model = model

# =========================
# SAVE METRICS
# =========================
metrics_df = pd.DataFrame(results)
metrics_df.to_csv("model_metrics.csv", index=False)

print("\n📊 Metrics saved to model_metrics.csv")

# =========================
# FINAL MODEL INFO
# =========================
print("\n===== BEST MODEL =====")
print(f"Selected Model: {type(best_model).__name__}")
print(f"Best R2 Score: {best_score:.3f}")

# =========================
# SAVE MODEL + ENCODERS
# =========================
joblib.dump(best_model, "model.pkl")
joblib.dump(le_location, "location_encoder.pkl")
joblib.dump(le_loc_type, "location_type_encoder.pkl")
joblib.dump(le_context, "context_type_encoder.pkl")

print("\n✅ Model and encoders saved successfully!")