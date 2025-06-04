# run_pipeline.py

import subprocess

def run_pipeline():
    print("Step 1: Parsing pcap...")
    subprocess.run(["python", "scripts/parse_pcap.py"], check=True)

    print("Step 2: Feature engineering...")
    subprocess.run(["python", "scripts/feature_engineering.py"], check=True)

    print("Step 3: Train and predict anomalies...")
    subprocess.run(["python", "scripts/train_model.py"], check=True)

    print("Step 4: Automated response & alerting...")
    subprocess.run(["sudo", "python", "scripts/response_automation.py"], check=True)

if __name__ == "__main__":
    run_pipeline()
