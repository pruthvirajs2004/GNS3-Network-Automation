# 05_configure_vlans.py
# Automates VLAN creation and port assignment on SW1
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from colorama import Fore, init
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import SWITCHES

init(autoreset=True)

VLANS = [
    {"id": 10, "name": "MANAGEMENT"},
    {"id": 20, "name": "USERS"},
]

PORT_CONFIG = {
    "SW1": {
        "GigabitEthernet0/2": {"mode": "access", "vlan": 10},
        "GigabitEthernet0/3": {"mode": "access", "vlan": 20},
    }
}

def configure_vlans():
    print("\n" + "="*55)
    print("           VLAN CONFIGURATION")
    print("="*55)

    for device in SWITCHES:
        name = device["name"]
        print(f"\n[*] Configuring VLANs on {name} ({device['host']})...")

        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})

            vlan_commands = []
            for vlan in VLANS:
                vlan_commands.append(f"vlan {vlan['id']}")
                vlan_commands.append(f"name {vlan['name']}")
            conn.send_config_set(vlan_commands)
            print(Fore.GREEN + f"  [+] VLANs created: {[v['id'] for v in VLANS]}")

            ports = PORT_CONFIG.get(name, {})
            for port, config in ports.items():
                port_commands = [
                    f"interface {port}",
                    "switchport mode access",
                    f"switchport access vlan {config['vlan']}",
                    "no shutdown",
                ]
                conn.send_config_set(port_commands)
                print(Fore.GREEN + f"  [+] {port} → VLAN {config['vlan']}")

            conn.send_command("write memory")
            vlan_output = conn.send_command("show vlan brief")
            conn.disconnect()

            print(f"\n--- {name} VLAN Table ---")
            print(vlan_output)

        except Exception as e:
            print(Fore.RED + f"FAILED — {str(e)}")

    print("="*55 + "\n")

if __name__ == "__main__":
    configure_vlans()
