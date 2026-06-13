# Troubleshooting Guide

## Issue: Destination host unreachable

**Cause:** Cloud node not bridged correctly to VMnet1  
**Fix:**
1. Right-click Cloud node → Configure → Ethernet interfaces → Add `eth0`
2. Ensure Cloud node is on GNS3 VM (not Buddy)
3. Verify Router1 G0/1 IP is in `192.168.100.x` subnet

---

## Issue: NAT node not responding (ping 192.168.122.1 fails)

**Cause:** NAT node on wrong server or GNS3 VM NAT service not running  
**Fix:** Use Cloud node with eth0 instead of NAT node (see SETUP.md)

---

## Issue: SSH connection refused

**Cause:** SSH not configured on router  
**Fix:** Run these on Router1 console:
```
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 transport input ssh
 login local
```

---

## Issue: Netmiko authentication error

**Cause:** Wrong username/password in `devices.py`  
**Fix:** Verify credentials match what's configured on the router:
```
username admin privilege 15 secret cisco
```

---

## Issue: GNS3 VM CPU 100%

**Cause:** Insufficient resources allocated to GNS3 VM  
**Fix:** 
1. Edit → Preferences → GNS3 VM
2. Increase vCPUs to 2+
3. Increase RAM to 4GB+
4. Restart GNS3 VM

---

## Issue: ARP entry missing for gateway

**Cause:** Cloud node eth0 not connected to correct VMnet interface  
**Fix:** 
1. Check `ipconfig` on laptop — VMnet1 should be `192.168.100.1`
2. Verify Cloud node is using `eth0` (which maps to VMnet1 in GNS3 VM)
3. Ping from router: `ping 192.168.100.1`

---

## Issue: Python script import error

**Cause:** Running script from wrong directory  
**Fix:** Always run scripts from the project root:
```
cd gns3-network-automation
python scripts/01_connectivity_test.py
```
