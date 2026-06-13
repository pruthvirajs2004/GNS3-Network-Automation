# Lab Setup Guide

## Prerequisites

- Windows 10/11 laptop
- VMware Workstation 16+
- GNS3 2.2.59 with GNS3 VM
- Cisco IOSvL2 image
- Python 3.x installed

---

## Step 1 — GNS3 VM Setup

1. Download GNS3 VM from [gns3.com](https://gns3.com)
2. Import OVA into VMware Workstation
3. Start GNS3 VM — note the IP shown on screen (e.g. `192.168.100.130`)
4. Open GNS3 on your laptop → Edit → Preferences → GNS3 VM → connect to the VM

---

## Step 2 — Network Bridge Setup

The automation uses VMware VMnet1 (Host-Only) to connect your laptop to GNS3:

```
Laptop VMnet1 (192.168.100.1)
        ↕
GNS3 VM (192.168.100.130)
        ↕
Cloud node (eth0) in GNS3
        ↕
Router1 G0/1 (192.168.100.200)
```

**Verify VMnet1 IP on your laptop:**
```
ipconfig
```
Look for `VMware Network Adapter VMnet1` — should show `192.168.100.1`

---

## Step 3 — GNS3 Topology

1. Open GNS3
2. Add devices: Cloud node, Router1, Switch1, PC1
3. Configure Cloud node:
   - Right-click → Configure → Ethernet interfaces → Add **eth0** → OK
4. Connect: `Cloud1 (eth0) → Router1 G0/1`
5. Connect: `Router1 G0/0 → Switch1 → PC1`
6. Start all devices (green Play button)

---

## Step 4 — Router1 Initial Config

Open Router1 console and paste:

```
enable
configure terminal
hostname R1
ip domain-name lab.local
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret cisco
line vty 0 4
 login local
 transport input ssh
interface GigabitEthernet0/1
 ip address 192.168.100.200 255.255.255.0
 no shutdown
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
ip route 0.0.0.0 0.0.0.0 192.168.100.1
end
write memory
```

---

## Step 5 — Windows Firewall Rule

Allow ICMP only from GNS3 subnet (run as Administrator):

```
netsh advfirewall firewall add rule name="Allow ICMP GNS3" protocol=icmpv4 dir=in action=allow remoteip=192.168.100.0/24
```

---

## Step 6 — Test Connectivity

From your laptop CMD:
```
ping 192.168.100.200
```

Should get replies. Then run:
```
python scripts/01_connectivity_test.py
```

---

## Step 7 — Run Automation Scripts

```bash
# Test connectivity
python scripts/01_connectivity_test.py

# Backup configs
python scripts/02_backup_configs.py

# Monitor interfaces
python scripts/06_monitor_interfaces.py

# Generate HTML report
python scripts/07_generate_report.py
```
