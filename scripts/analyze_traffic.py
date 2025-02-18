import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend

from scapy.all import rdpcap, IP, Ether, TCP, UDP, ICMP
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

# Set correct file paths
BASE_DIR = "/home/abbas/sdn-apt-project"
CAPTURES_DIR = os.path.join(BASE_DIR, "captures")
GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

BASELINE_PCAP = os.path.join(CAPTURES_DIR, "baseline.pcap")
ATTACK_PCAP = os.path.join(CAPTURES_DIR, "attack.pcap")
MITIGATION_PCAP = os.path.join(CAPTURES_DIR, "mitigation.pcap")

# Ensure the graphs directory exists
os.makedirs(GRAPH_DIR, exist_ok=True)

# Load packet capture files
baseline_packets = rdpcap(BASELINE_PCAP)
attack_packets = rdpcap(ATTACK_PCAP)
mitigation_packets = rdpcap(MITIGATION_PCAP)

# Extract timestamps, protocols, and packet sizes
def extract_packet_data(packets):
    timestamps, inter_arrival_times, packet_sizes = [], [], []
    last_timestamp = None

    for pkt in packets:
        if pkt.haslayer(Ether):
            timestamps.append(pkt.time)
            packet_sizes.append(len(pkt))
            if last_timestamp:
                inter_arrival_times.append(pkt.time - last_timestamp)
            last_timestamp = pkt.time

    return timestamps, inter_arrival_times, packet_sizes

# Extract data from each phase
baseline_data = extract_packet_data(baseline_packets)
attack_data = extract_packet_data(attack_packets)
mitigation_data = extract_packet_data(mitigation_packets)

# Convert to DataFrames
df_baseline = pd.DataFrame({"timestamp": baseline_data[0], "size": baseline_data[2]})
df_attack = pd.DataFrame({"timestamp": attack_data[0], "size": attack_data[2]})
df_mitigation = pd.DataFrame({"timestamp": mitigation_data[0], "size": mitigation_data[2]})

# 🔹 Traffic Volume Over Time
plt.figure(figsize=(10, 5))
plt.plot(df_baseline["timestamp"], df_baseline["size"], label="Baseline Traffic", alpha=0.7, color="blue")
plt.plot(df_attack["timestamp"], df_attack["size"], label="Attack Traffic", alpha=0.7, color="red")
plt.plot(df_mitigation["timestamp"], df_mitigation["size"], label="Mitigation Traffic", alpha=0.7, color="green")
plt.xlabel("Time (seconds)")
plt.ylabel("Packet Size (bytes)")
plt.title("Traffic Volume Over Time (Baseline vs Attack vs Mitigation)")
plt.legend()
plt.savefig(os.path.join(GRAPH_DIR, "traffic_volume_all.png"))

# 🔹 Inter-Arrival Time Analysis
plt.figure(figsize=(10, 5))
plt.hist(baseline_data[1], bins=100, alpha=0.5, label="Baseline", color="blue", log=True)
plt.hist(attack_data[1], bins=100, alpha=0.5, label="Attack", color="red", log=True)
plt.hist(mitigation_data[1], bins=100, alpha=0.5, label="Mitigation", color="green", log=True)
plt.xlabel("Inter-Arrival Time (seconds)")
plt.ylabel("Packet Count (log scale)")
plt.title("Inter-Arrival Time Distribution (Baseline vs Attack vs Mitigation)")
plt.legend()
plt.savefig(os.path.join(GRAPH_DIR, "inter_arrival_all.png"))

# 🔹 Flow Rule Modifications Over Time
baseline_mod_times = np.array(baseline_data[0]) if baseline_data[0] else []
attack_mod_times = np.array(attack_data[0]) if attack_data[0] else []
mitigation_mod_times = np.array(mitigation_data[0]) if mitigation_data[0] else []

plt.figure(figsize=(10, 5))
plt.vlines(baseline_mod_times, ymin=0, ymax=1, color="blue", alpha=0.5, linewidth=2, label="Baseline Mods")
plt.vlines(attack_mod_times, ymin=0, ymax=1, color="red", alpha=0.5, linewidth=2, label="Attack Mods")
plt.vlines(mitigation_mod_times, ymin=0, ymax=1, color="green", alpha=0.5, linewidth=2, label="Mitigation Mods")
plt.xlabel("Time (seconds)")
plt.ylabel("Flow Rule Modifications")
plt.title("Flow Rule Modifications Over Time (Baseline vs Attack vs Mitigation)")
plt.legend()
plt.savefig(os.path.join(GRAPH_DIR, "flow_mods_all.png"))

print("[+] All graphs generated in 'graphs/' directory.")
