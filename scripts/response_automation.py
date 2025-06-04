# scripts/response_automation.py

import pandas as pd
import subprocess
from slack_sdk import WebClient
import os

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Set this env var before running
SLACK_CHANNEL = "#alerts"  # Change to your Slack channel

def block_ip(ip):
    try:
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True
        )
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")

def send_slack_alert(ip):
    if not SLACK_TOKEN:
        print("No Slack token found in environment, skipping alert.")
        return
    client = WebClient(token=SLACK_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f"Alert: Intrusion detected and IP blocked - {ip}"
        )
        print(f"Slack alert sent for IP {ip}")
    except Exception as e:
        print(f"Slack alert failed: {e}")

def automate_response(predictions_csv, original_csv):
    preds = pd.read_csv(predictions_csv)
    original = pd.read_csv(original_csv)

    # Join original with predictions by index
    df = original.copy()
    df['Anomaly'] = preds['Anomaly']

    # Filter anomalous rows
    anomalies = df[df['Anomaly'] == -1]

    # Extract unique suspicious IPs (source IPs flagged)
    suspicious_ips = anomalies['Source'].unique()

    for ip in suspicious_ips:
        block_ip(ip)
        send_slack_alert(ip)

if __name__ == "__main__":
    automate_response("logs/predictions.csv", "logs/parsed_traffic.csv")
