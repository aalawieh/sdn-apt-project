import requests
import json
import time
import os
import signal
import subprocess
import getpass

# Ryu REST API endpoint
RYU_REST_URL = "http://127.0.0.1:8080"

# Thresholds to detect malicious flow rules
MALICIOUS_PRIORITY_THRESHOLD = 50  # Attack rules typically use high priority
ATTACK_ACTIONS = ["DROP", "OUTPUT"]  # Look for suspicious modifications

# Admin users allowed to execute mitigation
AUTHORIZED_USERS = ["abbas", "root"]  # Modify this list as needed

def check_rbac():
    current_user = getpass.getuser()
    if current_user not in AUTHORIZED_USERS:
        print(f"[⛔] Unauthorized access attempt by {current_user}. Terminating execution.")
        exit(1)
    print(f"[✔] Access granted to {current_user}. Running defender script.")

# Get active switches dynamically
def get_switches():
    response = requests.get(f"{RYU_REST_URL}/stats/switches")
    return response.json() if response.status_code == 200 else []

# Get flow rules from a switch
def get_flows(switch_id):
    response = requests.get(f"{RYU_REST_URL}/stats/flow/{switch_id}")
    return response.json().get(str(switch_id), []) if response.status_code == 200 else []

# Delete a flow rule
def delete_flow_rule(rule):
    requests.post(f"{RYU_REST_URL}/stats/flowentry/delete", data=json.dumps(rule), headers={'Content-Type': 'application/json'})

# Restore default rules
def restore_default_rules(switch_id):
    default_rule = {
        "dpid": switch_id,
        "priority": 1,
        "match": {},
        "actions": [{"type": "OUTPUT", "port": "CONTROLLER"}]  # Forward to controller
    }
    requests.post(f"{RYU_REST_URL}/stats/flowentry/add", data=json.dumps(default_rule), headers={'Content-Type': 'application/json'})

# Identify and kill the attack process dynamically
def detect_and_kill_attacker():
    try:
        process_list = subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout.split("\n")
        attacker_pid = None

        for process in process_list:
            if ("python" in process and "flow" in process and "hijack" in process.lower()) or ("attack" in process.lower()):
                parts = process.split()
                attacker_pid = parts[1]  # PID is the second column
                break

        if attacker_pid:
            print(f"[🔥] Detected attack process (PID: {attacker_pid}). Terminating it...")
            os.kill(int(attacker_pid), signal.SIGKILL)
        else:
            print("[✔] No active attack process found.")

    except Exception as e:
        print(f"[⚠] Failed to detect and kill attack process: {e}")

# Main defender function
def monitor_and_restore():
    check_rbac()  # Ensure only authorized users execute the script
    print("[🛡] Monitoring for malicious flow rules... (Press CTRL+C to stop)")

    while True:
        switches = get_switches()
        if not switches:
            print("[-] No switches detected. Exiting.")
            return

        for switch in switches:
            flows = get_flows(switch)

            for flow in flows:
                priority = flow.get("priority", 0)
                actions = flow.get("actions", [])

                # Detect suspicious modifications
                if priority >= MALICIOUS_PRIORITY_THRESHOLD and any(act in str(actions) for act in ATTACK_ACTIONS):
                    print(f"[⚠] Detected malicious flow rule on Switch {switch}! Removing...")
                    delete_flow_rule({"dpid": switch, "priority": priority, "match": flow["match"]})
                    restore_default_rules(switch)

        # Identify and kill the attacker process
        detect_and_kill_attacker()

        time.sleep(1)  # Faster reaction to mitigate attacks quickly

if __name__ == "__main__":
    monitor_and_restore()
