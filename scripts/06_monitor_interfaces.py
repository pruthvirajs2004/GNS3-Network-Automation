# 06_monitor_interfaces.py
# Real-time interface status monitoring for all devices
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from colorama import Fore, init
from tabulate import tabulate
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import ALL_DEVICES

init(autoreset=True)

def parse_interfaces(output):
    interfaces = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 6 and not line.startswith("Interface"):
            name = parts[0]
            ip = parts[1]
            status = parts[4]
            protocol = parts[5]
            interfaces.append({
                "interface": name,
                "ip": ip,
                "status": status,
                "protocol": protocol,
            })
    return interfaces

def monitor_interfaces():
    print("\n" + "="*65)
    print("          NETWORK INTERFACE STATUS MONITOR")
    print(f"          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*65)

    all_results = []

    for device in ALL_DEVICES:
        name = device["name"]
        print(f"\n[*] Polling {name} ({device['host']})...", end=" ")

        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
            output = conn.send_command("show ip interface brief")
            conn.disconnect()

            interfaces = parse_interfaces(output)
            print(Fore.GREEN + f"OK — {len(interfaces)} interfaces found")

            for intf in interfaces:
                all_results.append({
                    "Device": name,
                    "Interface": intf["interface"],
                    "IP Address": intf["ip"],
                    "Status": intf["status"],
                    "Protocol": intf["protocol"],
                })

        except Exception as e:
            print(Fore.RED + f"FAILED — {str(e)}")

    if all_results:
        print("\n" + "="*65)
        print("                 INTERFACE SUMMARY")
        print("="*65)

        # Color code status
        table_data = []
        for r in all_results:
            status_colored = r["Status"]
            proto_colored = r["Protocol"]
            if r["Status"] == "up" and r["Protocol"] == "up":
                status_colored = Fore.GREEN + "up" + Style.RESET_ALL
                proto_colored = Fore.GREEN + "up" + Style.RESET_ALL
            elif r["Status"] == "administratively":
                status_colored = Fore.YELLOW + "admin down" + Style.RESET_ALL
                proto_colored = Fore.YELLOW + "down" + Style.RESET_ALL
            else:
                status_colored = Fore.RED + r["Status"] + Style.RESET_ALL
                proto_colored = Fore.RED + r["Protocol"] + Style.RESET_ALL

            table_data.append([
                r["Device"],
                r["Interface"],
                r["IP Address"],
                status_colored,
                proto_colored,
            ])

        print(tabulate(
            table_data,
            headers=["Device", "Interface", "IP Address", "Status", "Protocol"],
            tablefmt="simple"
        ))

    up_count = sum(1 for r in all_results if r["Status"] == "up" and r["Protocol"] == "up")
    down_count = len(all_results) - up_count

    print("\n" + "="*65)
    print(f"  Total interfaces: {len(all_results)} | " +
          Fore.GREEN + f"Up: {up_count}" + Style.RESET_ALL + " | " +
          Fore.RED + f"Down: {down_count}" + Style.RESET_ALL)
    print("="*65 + "\n")

if __name__ == "__main__":
    monitor_interfaces()
