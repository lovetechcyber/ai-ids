import pyshark
import pandas as pd
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PCAP_DIR = os.path.join(BASE_DIR, "data")
CSV_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(PCAP_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)


def generate_filename():
    return datetime.now().strftime("capture_%Y%m%d_%H%M%S")


# =========================
# LIVE CAPTURE
# =========================
def capture_live_packets(packet_count=50, interface="Wi-Fi"):

    filename = generate_filename()
    pcap_path = os.path.join(PCAP_DIR, f"{filename}.pcap")

    print(f"📡 Capturing {packet_count} packets on {interface}...")

    try:
        capture = pyshark.LiveCapture(
            interface=interface,
            output_file=pcap_path
        )

        capture.sniff(packet_count=packet_count)

        print(f"✅ Saved PCAP: {pcap_path}")
        return pcap_path, filename

    except Exception as e:
        print(f"❌ Capture failed: {e}")
        return None, None


# =========================
# FEATURE EXTRACTION (FIXED)
# =========================
def extract_features(pcap_file, filename):

    if not pcap_file:
        return None

    packets = []
    capture = pyshark.FileCapture(pcap_file)

    try:
        for pkt in capture:
            try:

                # safer field extraction
                src = getattr(pkt, "ip", None)
                dst = getattr(pkt, "ip", None)

                packets.append({
                    "No": getattr(pkt, "number", 0),
                    "Time": str(getattr(pkt, "sniff_time", "")),
                    "Source": getattr(src, "src", "unknown") if src else "unknown",
                    "Destination": getattr(dst, "dst", "unknown") if dst else "unknown",
                    "Protocol": getattr(pkt, "highest_layer", "unknown"),
                    "Length": int(getattr(pkt, "length", 0)),
                    "Info": pkt.highest_layer if hasattr(pkt, "highest_layer") else "unknown"
                })

            except Exception:
                continue

    finally:
        capture.close()

    df = pd.DataFrame(packets)

    csv_path = os.path.join(CSV_DIR, f"{filename}.csv")
    df.to_csv(csv_path, index=False)

    print(f"📄 Saved CSV: {csv_path}")

    return csv_path


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    pcap_path, filename = capture_live_packets(
        packet_count=50,
        interface="Wi-Fi"   # Windows: confirm via tshark -D
    )

    extract_features(pcap_path, filename)