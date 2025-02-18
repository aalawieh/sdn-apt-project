#!/usr/bin/python3

import os
import sys
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

# Ensure script runs as root
if os.geteuid() != 0:
    print("[❌] Error: This script must be run as root!")
    print("[💡] Try running: sudo python3 custom_topology.py")
    sys.exit(1)

def custom_topology():
    setLogLevel("info")

    print("[🚀] Starting custom Mininet topology...")

    # Create network
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    # Add remote controller
    print("[+] Adding remote SDN controller at 127.0.0.1:6653")
    controller = net.addController("c0", controller=RemoteController, ip="127.0.0.1", port=6653)

    # Add switches
    print("[+] Adding switches...")
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    s3 = net.addSwitch("s3")

    # Add hosts
    print("[+] Adding hosts...")
    h1 = net.addHost("h1", ip="10.0.0.1")
    h2 = net.addHost("h2", ip="10.0.0.2")
    h3 = net.addHost("h3", ip="10.0.0.3")
    h4 = net.addHost("h4", ip="10.0.0.4")

    # Add links
    print("[+] Establishing links...")
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, h1)
    net.addLink(s2, h2)
    net.addLink(s3, h3)
    net.addLink(s3, h4)

    # Start network
    print("[🚀] Starting network...")
    net.start()

    # Run test connectivity
    print("[🔎] Running initial connectivity test...")
    net.pingAll()

    # Start CLI for manual control
    print("[🔹] Entering Mininet CLI. Type 'exit' to quit.")
    CLI(net)

    # Stop network after CLI exits
    print("[❌] Stopping network...")
    net.stop()

if __name__ == "__main__":
    custom_topology()
