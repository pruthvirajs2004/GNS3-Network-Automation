# 04_configure_ospf.py
# Pushes OSPF Area 0 configuration to R1 and R2
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from colorama import Fore, init
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import ROUTERS

init(autoreset=True)

OSPF_CONFIG = {
    "R1": [
        "router ospf 1",
        "router-id 1.1.1.1",
        "network 192.168.100.0 0.0.0.255 area 0",
        "network 10.0.0.0 0.0.0.255 area 0",
        "passive-interface GigabitEthernet0/1",
    ],
    "R2": [
        "router ospf 1",
        "router-id 2.2.2.2",
        "network 10.0.0.0 0.0.0.255 area 0",
        "network 192.168.10.0 0.0.0.255 area 0",
        "network 192.168.20.0 0.0.0.255 area 0",
    ],
}

def configure_ospf():
    print("\n" + "="*55)
    print("           OSPF CONFIGURATION")
    print("="*55)

    for device in ROUTERS:
        name = device["name"]
        commands = OSPF_CONFIG.get(name)

        if not commands:
            print(Fore.YELLOW + f"[!] No OSPF config defined for {name}, skipping.")
            continue

        print(f"\n[*] Configuring OSPF on {name} ({device['host']})...", end=" ")

        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
            conn.send_config_set(commands)
            conn.send_command("write memory")
            ospf_output = conn.send_command("show ip ospf")
            conn.disconnect()

            if "Routing Process" in ospf_output:
                print(Fore.GREEN + "SUCCESS — OSPF process running")
            else:
                print(Fore.YELLOW + "WARNING — Check OSPF manually")

        except Exception as e:
            print(Fore.RED + f"FAILED — {str(e)}")

    print("\n" + "="*55)
    print("  Verifying OSPF neighbors...")
    print("="*55)

    for device in ROUTERS:
        name = device["name"]
        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
            neighbors = conn.send_command("show ip ospf neighbor")
            conn.disconnect()
            print(f"\n--- {name} OSPF Neighbors ---")
            print(neighbors if neighbors.strip() else "  No neighbors yet")
        except Exception as e:
            print(Fore.RED + f"[!] Could not verify {name}: {str(e)}")

    print("\n" + "="*55 + "\n")

if __name__ == "__main__":
    configure_ospf()
