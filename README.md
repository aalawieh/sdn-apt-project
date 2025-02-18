# **Advanced Persistent Threat (APT) Attack in SDN and Mitigation**

## **📌 Overview**

This research investigates Advanced Persistent Threat (APT) attacks in a **Software-Defined Networking (SDN)** environment, focusing on exploiting SDN controllers, manipulating flow rules, and implementing mitigation strategies. The study demonstrates how an attacker can hijack flow rules and how a defender can detect and neutralize the attack.

## **🎯 Objectives**

- Simulate an APT attack by modifying OpenFlow rules on an SDN network.
- Measure the attack's impact on SDN traffic and connectivity.
- Develop and deploy a **defender module** to mitigate the attack.
- Analyze the results using real-time **traffic and flow rule modification graphs**.

## **🛠️ Setup & Requirements**

### **🔧 Prerequisites**

- **OS**: Ubuntu 20.04+ (or any Linux-based system)
- **Tools**:
  - Mininet
  - Ryu SDN Controller
  - Python 3.9+
  - Git
  - Wireshark/tcpdump
  - Matplotlib, Pandas, PyShark, Scapy (for analysis)

### **📂 Project Structure**

```
~/sdn-apt-project/
├── scripts/                # Attack, mitigation, and monitoring scripts
│   ├── flow_rule_hijacking.py  # Attack script
│   ├── restore_flow_rules.py   # Defender script
│   ├── track_flow_changes.py   # Flow rule tracking
│   ├── analyze_traffic.py      # Traffic & flow modification analysis
├── captures/               # Network traffic captures (.pcap)
├── graphs/                 # Graph outputs
└── README.md               # Project documentation
```

## **🚀 Execution Steps**

### **1️⃣ Start SDN Network & Capture Baseline Data**

```bash
cd ~/sdn-apt-project/scripts
source ~/sdn-apt-project/ryu-env-py39/bin/activate
ryu-manager --ofp-tcp-listen-port 6653 ryu.app.rest_conf_switch ryu.app.ofctl_rest ryu.app.simple_switch_13 &
sudo python3 custom_topology.py
sudo tcpdump -i s1-eth1 -w ~/sdn-apt-project/captures/baseline.pcap -c 1000
```

### **2️⃣ Launch APT Attack**

```bash
python3 flow_rule_hijacking.py
```

- The attack will inject malicious flow rules and evade detection.

### **3️⃣ Track Flow Rule Changes**

```bash
python3 track_flow_changes.py
```

- This script logs unauthorized flow rule modifications.

### **4️⃣ Measure Attack Impact**

```bash
pingall # Run in Mininet CLI
sudo tcpdump -i s1-eth1 -w ~/sdn-apt-project/captures/attack.pcap -c 1000
```

### **5️⃣ Deploy Defender & Mitigate Attack**

```bash
python3 restore_flow_rules.py
```

- The defender removes malicious flow rules and restores legitimate rules.
- Uses **RBAC (Role-Based Access Control) principles** to restrict admin access.

### **6️⃣ Capture Post-Mitigation Traffic**

```bash
sudo tcpdump -i s1-eth1 -w ~/sdn-apt-project/captures/mitigation.pcap -c 1000
```

### **7️⃣ Generate Graphs for Analysis**

```bash
python3 analyze_traffic.py
```

- Generates traffic and flow modification graphs for:
  - **Baseline Traffic vs Attack Traffic vs Mitigation Traffic**
  - **Flow Rule Modifications Over Time**
  - **Inter-Arrival Time & Packet Timing Analysis**

## **📊 Results & Findings**

| Phase      | Packet Drop Rate | Flow Rule Changes | Attack Impact         |
| ---------- | ---------------- | ----------------- | --------------------- |
| Baseline   | \~0%             | Minimal           | Normal Traffic        |
| Attack     | \~50-90%         | Frequent          | Severe disruption     |
| Mitigation | \~0-5%           | Stabilized        | Restored connectivity |

### **📈 Example Graphs**

1. **Flow Rule Modifications Over Time** (Baseline vs Attack vs Mitigation)
2. **Inter-Arrival Time Distribution** (Baseline vs Attack vs Mitigation)
3. **Traffic Volume Comparison**

## **🌍 Repository & Contribution**

- **GitHub Repository**: [https://github.com/aalawieh/sdn-apt-project](https://github.com/aalawieh/sdn-apt-project)

## **📩 Contact**

Reach out at [**abbas.alawieh@telecom-sudparis.eu**](mailto\:abbas.alawieh@telecom-sudparis.eu).

---

🚀 **Final Thoughts**: This research provides insights into **APT attacks on SDN**, demonstrating the feasibility of exploiting flow rules and the effectiveness of mitigation techniques.

