import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_pipeline():
    print("Step 1: Parsing pcap...")
    subprocess.run(["python", os.path.join(BASE_DIR, "scripts", "parse_pcap.py")], check=True)

    print("Step 2: Feature engineering...")
    subprocess.run(["python", os.path.join(BASE_DIR, "scripts", "feature_engineering.py")], check=True)

    print("Step 3: Train and predict anomalies...")
    subprocess.run(["python", os.path.join(BASE_DIR, "scripts", "train_model.py")], check=True)

    print("Step 4: Automated response & alerting...")
    subprocess.run(["python", os.path.join(BASE_DIR, "scripts", "response_automation.py")], check=True)

if __name__ == "__main__":
    run_pipeline()