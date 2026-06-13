# GNS3 Network Automation with Python

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Netmiko](https://img.shields.io/badge/Netmiko-4.x-green)
![GNS3](https://img.shields.io/badge/GNS3-2.2.59-orange)
![Cisco IOS](https://img.shields.io/badge/Cisco-IOS-red?logo=cisco)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **Enterprise-grade Python network automation framework for Cisco IOS devices in GNS3 — covering device configuration, backup, monitoring, and reporting.**

---

## 📌 Project Overview

This project demonstrates real-world network automation skills using Python and Netmiko to manage Cisco IOS routers and switches inside a GNS3 lab environment. The automation scripts cover tasks that network engineers perform daily in enterprise environments.

**Key Skills Demonstrated:**
- Python scripting for network automation
- SSH connectivity to Cisco IOS devices via Netmiko
- Automated device configuration and backup
- Network monitoring and report generation
- GNS3 lab integration with physical host machine

---

## 🖧 Lab Topology

```
Laptop (192.168.100.1 - VMnet1)
         |
    [VMware VMnet1]
         |
    GNS3 VM (192.168.100.130)
         |
    Cloud1 (eth0 bridge)
         |
    R1 G0/1 (192.168.100.200)
         |
    SW1 (192.168.1.0/24)
    /    |    \
  PC1   PC2   PC3
```

| Device | Interface | IP Address       | Role            |
|--------|-----------|------------------|-----------------|
| Laptop | VMnet1    | 192.168.100.1    | Automation Host |
| R1     | G0/1      | 192.168.100.200  | Gateway Router  |
| R1     | G0/0      | 192.168.1.1      | LAN Interface   |
| SW1    | VLAN1     | 192.168.1.2      | Access Switch   |
| PC1    | eth0      | 192.168.1.10     | End Device      |
| PC2    | eth0      | 192.168.1.11     | End Device      |
| PC3    | eth0      | 192.168.1.12     | End Device      |

---

## 📁 Project Structure

```
gns3-network-automation/
├── README.md
├── requirements.txt
├── devices.py                  # Device inventory
├── scripts/
│   ├── 01_connectivity_test.py     # Ping and reachability check
│   ├── 02_backup_configs.py        # Backup all device configs
│   ├── 03_configure_hostname.py    # Change hostnames via Python
│   ├── 04_configure_ospf.py        # Push OSPF config to all routers
│   ├── 05_configure_vlans.py       # Automate VLAN setup on switches
│   ├── 06_monitor_interfaces.py    # Monitor interface status
│   └── 07_generate_report.py       # Generate HTML network report
├── configs/
│   └── base_config.txt             # Base router configuration template
├── backups/                        # Auto-generated device config backups
├── reports/                        # Auto-generated HTML reports
├── docs/
│   ├── SETUP.md                    # Lab setup guide
│   └── TROUBLESHOOTING.md          # Common issues and fixes
└── topology/
    └── topology_diagram.png        # GNS3 topology screenshot
```

---

## ⚙️ Prerequisites

- Python 3.x
- GNS3 2.2+ with GNS3 VM (VMware)
- Cisco IOS images (IOSvL2 or similar)
- VMware Workstation

---

## 🚀 Quick Start

**1. Clone the repository:**
```bash
git clone https://github.com/pruthvirajs2004/gns3-network-automation.git
cd gns3-network-automation
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Start GNS3 lab and verify connectivity:**
```bash
python scripts/01_connectivity_test.py
```

**4. Run full automation:**
```bash
python scripts/02_backup_configs.py
python scripts/04_configure_ospf.py
python scripts/07_generate_report.py
```

---

## 📋 Scripts Overview

| Script | Description |
|--------|-------------|
| `01_connectivity_test.py` | Tests SSH reachability to all devices |
| `02_backup_configs.py` | Backs up running configs to `/backups` folder |
| `03_configure_hostname.py` | Changes hostnames on all devices |
| `04_configure_ospf.py` | Configures OSPF Area 0 on all routers |
| `05_configure_vlans.py` | Creates and assigns VLANs on switches |
| `06_monitor_interfaces.py` | Shows real-time interface status |
| `07_generate_report.py` | Generates a full HTML network status report |

---

## 🎯 Skills Demonstrated

| Skill | Tool/Technology |
|-------|----------------|
| Network Automation | Python, Netmiko |
| Device Management | Cisco IOS CLI |
| SSH Connectivity | Paramiko/Netmiko |
| Lab Virtualization | GNS3, VMware |
| Config Management | Automated backup & restore |
| Reporting | HTML report generation |
| Version Control | Git, GitHub |

---

## 👤 Author

**Pruthvi Raj S**  
Network Engineer | Bengaluru, Karnataka  
[![GitHub](https://img.shields.io/badge/GitHub-pruthvirajs2004-black?logo=github)](https://github.com/pruthvirajs2004)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/pruthvirajs2004)

---

## 📄 License

MIT License — feel free to use and modify for your own lab environment.
