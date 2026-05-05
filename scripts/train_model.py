# scripts/train_model.py

import sys
import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_DIR = os.path.join(BASE_DIR, "models")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(MODEL_DIR, exist_ok=True)


def train_model(feature_csv):

    df = pd.read_csv(feature_csv)

    # =========================
    # MODEL TRAINING
    # =========================
    model = IsolationForest(
        n_estimators=100,
        contamination=0.01,   # adjust later based on real data
        random_state=42
    )

    model.fit(df)

    # =========================
    # PREDICTION
    # =========================
    predictions = model.predict(df)  # -1 anomaly, 1 normal
    scores = model.decision_function(df)  # anomaly score

    df["Anomaly"] = predictions
    df["Score"] = scores

    # Convert anomaly to binary (clean for API/dashboard)
    df["Anomaly"] = df["Anomaly"].apply(lambda x: 1 if x == -1 else 0)

    # =========================
    # SAVE MODEL
    # =========================
    model_path = os.path.join(MODEL_DIR, "isolation_forest.pkl")
    joblib.dump(model, model_path)

    # =========================
    # SAVE OUTPUT (IMPORTANT FIX)
    # =========================
    output_path = feature_csv.replace("_features.csv", "_predictions.csv")
    df.to_csv(output_path, index=False)

    # =========================
    # STATS
    # =========================
    anomaly_count = df["Anomaly"].sum()

    print(f"Anomalies Detected: {anomaly_count} / {len(df)}")
    print(f"📄 Saved predictions: {output_path}")
    print(f"🧠 Model saved: {model_path}")

    return df


# =========================
# PIPELINE ENTRY POINT
# =========================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ No feature file provided")
        sys.exit(1)

    filename = sys.argv[1]

    feature_path = os.path.join(BASE_DIR, "logs", f"{filename}_features.csv")

    train_model(feature_path)