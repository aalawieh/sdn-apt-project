import re
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# File paths
LOG_FILE = "/home/abbas/sdn-apt-project/logs/flow_anomaly_log.txt"
GRAPH_DIR = "/home/abbas/sdn-apt-project/graphs"

# Ensure the graphs directory exists
os.makedirs(GRAPH_DIR, exist_ok=True)

# Read detection log file
with open(LOG_FILE, "r") as file:
    logs = file.readlines()

# Extract timestamps and rule modifications
timestamps = []
added_rules_count = []
removed_rules_count = []

for line in logs:
    if "[⚠] Flow Rule Changes Detected!" in line:
        timestamps.append(datetime.now().timestamp())
        added_rules_count.append(0)
        removed_rules_count.append(0)
    
    if "[+] New Rules Added:" in line:
        added_rules_count[-1] += 1

    if "[-] Rules Removed:" in line:
        removed_rules_count[-1] += 1

# Convert to DataFrame
df = pd.DataFrame({
    "Time": timestamps,
    "Added Rules": added_rules_count,
    "Removed Rules": removed_rules_count
})

# Save as CSV for reference
df.to_csv(os.path.join(GRAPH_DIR, "detection_log_summary.csv"), index=False)

# 📊 1️⃣ Plot Flow Rule Modifications Over Time
plt.figure(figsize=(10, 5))
plt.plot(df["Time"], df["Added Rules"], marker="o", label="Added Rules", color="red")
plt.plot(df["Time"], df["Removed Rules"], marker="s", label="Removed Rules", color="blue")

plt.xlabel("Time (seconds)")
plt.ylabel("Flow Rule Changes")
plt.title("Detected Flow Rule Modifications Over Time")
plt.legend()
plt.grid()

# Save the graph
plt.savefig(os.path.join(GRAPH_DIR, "flow_rule_changes_over_time.png"))
print("[✅] Graph saved: flow_rule_changes_over_time.png")
