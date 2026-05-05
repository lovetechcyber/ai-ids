# scripts/feature_engineering.py

import sys
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def engineer_features(csv_path):
    df = pd.read_csv(csv_path)

    # =========================
    # DATA CLEANING
    # =========================
    required_cols = ["Source", "Destination", "Protocol", "Length"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df.dropna(subset=required_cols, inplace=True)

    # =========================
    # ENCODING
    # =========================
    le = LabelEncoder()
    df["Protocol_Encoded"] = le.fit_transform(df["Protocol"].astype(str))

    # =========================
    # FREQUENCY FEATURES
    # =========================
    df["Src_IP_Freq"] = df["Source"].map(df["Source"].value_counts())
    df["Dst_IP_Freq"] = df["Destination"].map(df["Destination"].value_counts())

    df["Src_Dst_Pair"] = df["Source"].astype(str) + "-" + df["Destination"].astype(str)
    df["Pair_Freq"] = df["Src_Dst_Pair"].map(df["Src_Dst_Pair"].value_counts())

    # =========================
    # FINAL FEATURES
    # =========================
    features = df[[
        "Protocol_Encoded",
        "Length",
        "Src_IP_Freq",
        "Dst_IP_Freq",
        "Pair_Freq"
    ]]

    return features, df


# =========================
# PIPELINE ENTRY POINT
# =========================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ No filename provided")
        sys.exit(1)

    filename = sys.argv[1]

    input_path = os.path.join(BASE_DIR, "logs", f"{filename}.csv")
    output_path = os.path.join(BASE_DIR, "logs", f"{filename}_features.csv")

    print(f"📥 Reading: {input_path}")

    features, original = engineer_features(input_path)

    print("✅ Feature engineering completed")
    print(features.head())

    features.to_csv(output_path, index=False)

    print(f"💾 Saved features: {output_path}")