# 01_connectivity_test.py
# Tests SSH connectivity to all GNS3 devices
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from colorama import Fore, Style, init
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import ALL_DEVICES

init(autoreset=True)

def test_connectivity():
    print("\n" + "="*55)
    print("       GNS3 NETWORK CONNECTIVITY TEST")
    print("="*55)

    results = []

    for device in ALL_DEVICES:
        name = device["name"]
        host = device["host"]
        print(f"\n[*] Testing {name} ({host})...", end=" ")

        try:
            conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
            hostname = conn.find_prompt().strip("#>")
            conn.disconnect()
            print(Fore.GREEN + f"SUCCESS — Hostname: {hostname}")
            results.append({"device": name, "host": host, "status": "REACHABLE", "hostname": hostname})

        except NetmikoTimeoutException:
            print(Fore.RED + "FAILED — Connection timed out")
            results.append({"device": name, "host": host, "status": "TIMEOUT", "hostname": "N/A"})

        except NetmikoAuthenticationException:
            print(Fore.YELLOW + "FAILED — Authentication error")
            results.append({"device": name, "host": host, "status": "AUTH ERROR", "hostname": "N/A"})

        except Exception as e:
            print(Fore.RED + f"FAILED — {str(e)}")
            results.append({"device": name, "host": host, "status": "ERROR", "hostname": "N/A"})

    print("\n" + "="*55)
    print("                   SUMMARY")
    print("="*55)
    print(f"{'Device':<10} {'IP':<20} {'Status':<15} {'Hostname'}")
    print("-"*55)
    for r in results:
        color = Fore.GREEN if r["status"] == "REACHABLE" else Fore.RED
        print(color + f"{r['device']:<10} {r['host']:<20} {r['status']:<15} {r['hostname']}")

    reachable = sum(1 for r in results if r["status"] == "REACHABLE")
    print("\n" + "="*55)
    print(f"  Result: {reachable}/{len(results)} devices reachable")
    print("="*55 + "\n")

if __name__ == "__main__":
    test_connectivity()
