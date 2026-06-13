# 03_configure_hostname.py
# Change hostnames on GNS3 devices via Python
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from colorama import Fore, init
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import ALL_DEVICES

init(autoreset=True)

# Define new hostnames for each device
HOSTNAME_MAP = {
    "R1":  "R1-CORE",
    "SW1": "SW1-ACCESS",
}

def configure_hostnames():
    print("\n" + "="*55)
    print("         HOSTNAME CONFIGURATION")
    print("="*55)

    for device in ALL_DEVICES:
        name = device["name"]
        new_hostname = HOSTNAME_MAP.get(name)

        if not new_hostname:
            print(Fore.YELLOW + f"[!] No hostname defined for {name}, skipping.")
            continue

        print(f"\n[*] Configuring {name} ({device['host']}) → {new_hostname}...", end=" ")

        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
            old_hostname = conn.find_prompt().strip("#>")
            conn.send_config_set([f"hostname {new_hostname}"])
            conn.send_command("write memory")
            conn.disconnect()
            print(Fore.GREEN + f"SUCCESS — {old_hostname} → {new_hostname}")

        except Exception as e:
            print(Fore.RED + f"FAILED — {str(e)}")

    print("\n" + "="*55)
    print("  Hostname configuration complete!")
    print("="*55 + "\n")

if __name__ == "__main__":
    configure_hostnames()
