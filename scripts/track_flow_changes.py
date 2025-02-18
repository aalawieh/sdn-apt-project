import requests
import json
import time

# Ryu REST API endpoint
RYU_REST_URL = "http://127.0.0.1:8080"

# Store legitimate baseline flows
baseline_flows = {}

# Ryu default rule threshold (avoid flagging defaults)
LOW_PRIORITY_THRESHOLD = 10  # Default Ryu rules often have low priority (0 or 1)

# Get active switches dynamically
def get_switches():
    response = requests.get(f"{RYU_REST_URL}/stats/switches")
    if response.status_code == 200:
        return response.json()
    return []

# Get flow rules from a switch
def get_flows(switch_id):
    response = requests.get(f"{RYU_REST_URL}/stats/flow/{switch_id}")
    if response.status_code == 200:
        return response.json()
    return {}

# Normalize flow rules (remove dynamic fields like packet count and duration)
def normalize_flow(flow):
    ignore_keys = {"packet_count", "byte_count", "duration_sec", "duration_nsec"}
    return {k: v for k, v in flow.items() if k not in ignore_keys}

# Capture the initial baseline of flow rules
def initialize_baseline():
    global baseline_flows
    print("[🚀] Capturing baseline flow rules (ignoring Ryu default behavior)...")
    switches = get_switches()

    for switch in switches:
        flows = get_flows(switch).get(str(switch), [])
        
        # Store only flows that meet normal criteria
        baseline_flows[switch] = [
            normalize_flow(flow) for flow in flows if flow.get("priority", 0) <= LOW_PRIORITY_THRESHOLD
        ]

    print("[✔] Baseline established. Tracking unauthorized changes...")

# Detect unauthorized modifications
def detect_changes():
    global baseline_flows
    switches = get_switches()

    for switch in switches:
        current_flows = get_flows(switch).get(str(switch), [])
        
        # Normalize current flow rules
        current_set = {json.dumps(normalize_flow(flow), sort_keys=True) for flow in current_flows}
        baseline_set = {json.dumps(flow, sort_keys=True) for flow in baseline_flows.get(switch, [])}

        # Detect suspicious modifications
        new_rules = current_set - baseline_set
        removed_rules = baseline_set - current_set

        if new_rules or removed_rules:
            print(f"\n[⚠] Unauthorized Flow Rule Changes Detected on Switch {switch}!")

            if new_rules:
                print("\n[+] **Potentially Malicious Rules Added:**")
                for rule in new_rules:
                    rule_data = json.loads(rule)
                    print(json.dumps(rule_data, indent=4))

            if removed_rules:
                print("\n[-] **Flow Rules Unexpectedly Removed:**")
                for rule in removed_rules:
                    rule_data = json.loads(rule)
                    print(json.dumps(rule_data, indent=4))

            print("[!] Possible APT Attack Detected - Flow Integrity Compromised!")

        # Update baseline only if rules were expected modifications
        baseline_flows[switch] = [normalize_flow(flow) for flow in current_flows]

# Main function for tracking flow rule changes
def track_flow_changes():
    initialize_baseline()
    while True:
        detect_changes()
        time.sleep(5)  # Poll every 5 seconds

if __name__ == "__main__":
    print("[🚀] Tracking SDN Flow Rule Changes... (Press CTRL+C to stop)")
    track_flow_changes()
