# scripts/train_model.py

import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

def train_model(feature_csv):
    df = pd.read_csv(feature_csv)

    # Isolation Forest works best when data is normalized (but it's okay to start raw)
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(df)

    predictions = model.predict(df)  # -1 = anomaly, 1 = normal
    df['Anomaly'] = predictions

    # Save model
    joblib.dump(model, 'models/isolation_forest.pkl')

    # Save results
    df.to_csv("logs/predictions.csv", index=False)

    # Print stats
    anomaly_count = (df['Anomaly'] == -1).sum()
    print(f"Anomalies Detected: {anomaly_count} / {len(df)}")

    return df

if __name__ == "__main__":
    train_model("logs/features.csv")
