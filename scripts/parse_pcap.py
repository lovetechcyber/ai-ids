# scripts/parse_pcap.py

import pyshark
import pandas as pd

def extract_features(pcap_file):
    capture = pyshark.FileCapture(pcap_file, only_summaries=True)
    
    packets = []
    for pkt in capture:
        try:
            packets.append({
                "No": pkt.no,
                "Time": float(pkt.time),
                "Source": pkt.source,
                "Destination": pkt.destination,
                "Protocol": pkt.protocol,
                "Length": int(pkt.length),
                "Info": pkt.info
            })
        except Exception:
            continue

    df = pd.DataFrame(packets)
    return df

if __name__ == "__main__":
    df = extract_features("data/sample.pcap")
    print(df.head())
    df.to_csv("logs/parsed_traffic.csv", index=False)
