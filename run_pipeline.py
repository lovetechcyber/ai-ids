import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_pipeline():

    print("🚀 Starting AI IDS Pipeline...\n")

    # =========================
    # STEP 1: CAPTURE + PARSE
    # =========================
    print("Step 1: Capturing & parsing live traffic...")

    result = subprocess.run(
        ["python", os.path.join(BASE_DIR, "scripts", "parse_pcap.py")],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    # 🔥 Extract filename from output
    # Expect: "FILENAME: capture_20260505_123000"
    filename = None
    for line in result.stdout.splitlines():
        if line.startswith("FILENAME:"):
            filename = line.split("FILENAME:")[1].strip()

    if not filename:
        raise Exception("❌ Failed to get filename from parse_pcap.py")

    print(f"📁 Using file: {filename}\n")

    # =========================
    # STEP 2: FEATURE ENGINEERING
    # =========================
    print("Step 2: Feature engineering...")

    subprocess.run([
        "python",
        os.path.join(BASE_DIR, "scripts", "feature_engineering.py"),
        filename
    ], check=True)

    # =========================
    # STEP 3: MODEL
    # =========================
    print("Step 3: Train & detect anomalies...")

    subprocess.run([
        "python",
        os.path.join(BASE_DIR, "scripts", "train_model.py"),
        filename
    ], check=True)

    # =========================
    # STEP 4: RESPONSE
    # =========================
    print("Step 4: Sending to dashboard...")

    subprocess.run([
        "python",
        os.path.join(BASE_DIR, "scripts", "response_automation.py"),
        filename
    ], check=True)

    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()