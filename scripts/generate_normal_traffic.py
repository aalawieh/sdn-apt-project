from scapy.all import sendp, Ether, IP, ICMP, get_if_list
import time

# Auto-detect Mininet interface
def get_mininet_interface():
    interfaces = get_if_list()
    for iface in interfaces:
        if "eth" in iface and "lo" not in iface:
            return iface
    raise Exception("[❌] No Mininet interface detected.")

INTERFACE = get_mininet_interface()
TARGET_IP = "10.0.0.2"  # Adjust if needed
PACKET_COUNT = 1000  # Stop after 1000 packets

print(f"[🚀] Sending {PACKET_COUNT} normal ICMP packets via {INTERFACE} to {TARGET_IP}...")

sent_packets = 0
while sent_packets < PACKET_COUNT:
    packet = Ether() / IP(dst=TARGET_IP) / ICMP()
    sendp(packet, iface=INTERFACE, verbose=False)
    sent_packets += 1
    time.sleep(0.01)  # Small delay to simulate real traffic

print(f"[✅] Sent {PACKET_COUNT} normal packets on {INTERFACE}.")
