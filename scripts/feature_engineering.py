# scripts/feature_engineering.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def engineer_features(csv_path):
    df = pd.read_csv(csv_path)

    # Clean NaNs
    df.dropna(subset=["Source", "Destination", "Protocol", "Length"], inplace=True)

    # Encode Protocol
    le = LabelEncoder()
    df["Protocol_Encoded"] = le.fit_transform(df["Protocol"])

    # Count frequency of IPs and IP pairs
    df["Src_IP_Freq"] = df["Source"].map(df["Source"].value_counts())
    df["Dst_IP_Freq"] = df["Destination"].map(df["Destination"].value_counts())

    df["Src_Dst_Pair"] = df["Source"] + "-" + df["Destination"]
    df["Pair_Freq"] = df["Src_Dst_Pair"].map(df["Src_Dst_Pair"].value_counts())

    # Select features for ML
    features = df[[
        "Protocol_Encoded", "Length", "Src_IP_Freq", "Dst_IP_Freq", "Pair_Freq"
    ]]

    return features, df  # also return full df for reference

if __name__ == "__main__":
    features, original = engineer_features("logs/parsed_traffic.csv")
    print(features.head())
    features.to_csv("logs/features.csv", index=False)
