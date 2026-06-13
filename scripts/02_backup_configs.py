# 02_backup_configs.py
# Backs up running configurations from all GNS3 devices
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from colorama import Fore, init
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import ALL_DEVICES

init(autoreset=True)

BACKUP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backups")

def backup_configs():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n" + "="*55)
    print("         GNS3 DEVICE CONFIG BACKUP")
    print("="*55)
    print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backup Dir: {BACKUP_DIR}")
    print("="*55)

    success = 0
    failed = 0

    for device in ALL_DEVICES:
        name = device["name"]
        print(f"\n[*] Backing up {name} ({device['host']})...", end=" ")

        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
            config = conn.send_command("show running-config")
            conn.disconnect()

            filename = f"{name}_{timestamp}.txt"
            filepath = os.path.join(BACKUP_DIR, filename)

            with open(filepath, "w") as f:
                f.write(f"! Backup of {name}\n")
                f.write(f"! Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"! Device IP: {device['host']}\n")
                f.write("!"*50 + "\n\n")
                f.write(config)

            print(Fore.GREEN + f"SUCCESS — Saved to backups/{filename}")
            success += 1

        except Exception as e:
            print(Fore.RED + f"FAILED — {str(e)}")
            failed += 1

    print("\n" + "="*55)
    print(f"  Backup complete: {success} success, {failed} failed")
    print("="*55 + "\n")

if __name__ == "__main__":
    backup_configs()
