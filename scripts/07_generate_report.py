# 07_generate_report.py
# Generates a professional HTML network status report
# Author: Pruthvi Raj S

from netmiko import ConnectHandler
from colorama import Fore, init
from datetime import datetime
from jinja2 import Template
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from devices import ALL_DEVICES

init(autoreset=True)

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Network Status Report</title>
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
  h1 { color: #58a6ff; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
  h2 { color: #79c0ff; margin-top: 30px; }
  .meta { color: #8b949e; font-size: 0.9em; margin-bottom: 30px; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
  .badge-up { background: #1a4731; color: #56d364; }
  .badge-down { background: #4a1515; color: #f85149; }
  .badge-warn { background: #3a2a00; color: #e3b341; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; }
  th { background: #161b22; color: #58a6ff; padding: 10px 14px; text-align: left; border-bottom: 2px solid #21262d; }
  td { padding: 8px 14px; border-bottom: 1px solid #21262d; }
  tr:hover { background: #161b22; }
  .device-card { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 16px; margin-bottom: 20px; }
  .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 30px; }
  .summary-box { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 16px; text-align: center; }
  .summary-box .number { font-size: 2em; font-weight: bold; color: #58a6ff; }
  .summary-box .label { color: #8b949e; font-size: 0.85em; margin-top: 4px; }
  footer { margin-top: 40px; color: #8b949e; font-size: 0.85em; border-top: 1px solid #21262d; padding-top: 16px; }
</style>
</head>
<body>
<h1>🖧 Network Status Report</h1>
<div class="meta">
  Generated: {{ timestamp }} &nbsp;|&nbsp; 
  Devices Polled: {{ total_devices }} &nbsp;|&nbsp;
  Author: Pruthvi Raj S
</div>

<div class="summary-grid">
  <div class="summary-box">
    <div class="number">{{ total_devices }}</div>
    <div class="label">Total Devices</div>
  </div>
  <div class="summary-box">
    <div class="number" style="color:#56d364">{{ reachable }}</div>
    <div class="label">Reachable</div>
  </div>
  <div class="summary-box">
    <div class="number" style="color:#f85149">{{ unreachable }}</div>
    <div class="label">Unreachable</div>
  </div>
</div>

{% for device in devices %}
<div class="device-card">
  <h2>{{ device.name }} 
    {% if device.reachable %}
    <span class="badge badge-up">ONLINE</span>
    {% else %}
    <span class="badge badge-down">OFFLINE</span>
    {% endif %}
  </h2>
  <p style="color:#8b949e; margin:4px 0 12px">IP: {{ device.host }} &nbsp;|&nbsp; Role: {{ device.role }}</p>

  {% if device.reachable %}
  <table>
    <tr><th>Interface</th><th>IP Address</th><th>Status</th><th>Protocol</th></tr>
    {% for intf in device.interfaces %}
    <tr>
      <td>{{ intf.name }}</td>
      <td>{{ intf.ip }}</td>
      <td>
        {% if intf.status == 'up' %}
        <span class="badge badge-up">up</span>
        {% elif 'admin' in intf.status %}
        <span class="badge badge-warn">admin down</span>
        {% else %}
        <span class="badge badge-down">{{ intf.status }}</span>
        {% endif %}
      </td>
      <td>
        {% if intf.protocol == 'up' %}
        <span class="badge badge-up">up</span>
        {% else %}
        <span class="badge badge-down">{{ intf.protocol }}</span>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </table>
  {% else %}
  <p style="color:#f85149">⚠ Device unreachable — could not collect interface data.</p>
  {% endif %}
</div>
{% endfor %}

<footer>
  GNS3 Network Automation Project &nbsp;|&nbsp; 
  GitHub: <a href="https://github.com/pruthvirajs2004" style="color:#58a6ff">pruthvirajs2004</a>
</footer>
</body>
</html>
"""

def collect_device_data(device):
    data = {
        "name": device["name"],
        "host": device["host"],
        "role": device.get("role", "Unknown"),
        "reachable": False,
        "interfaces": [],
    }

    try:
        conn = ConnectHandler(**{k: v for k, v in device.items() if k != "name" and k != "role"})
        output = conn.send_command("show ip interface brief")
        conn.disconnect()
        data["reachable"] = True

        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 6 and not line.startswith("Interface"):
                data["interfaces"].append({
                    "name": parts[0],
                    "ip": parts[1],
                    "status": parts[4],
                    "protocol": parts[5],
                })
    except Exception:
        pass

    return data

def generate_report():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"network_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(REPORTS_DIR, filename)

    print("\n" + "="*55)
    print("         GENERATING NETWORK STATUS REPORT")
    print("="*55)

    devices_data = []
    for device in ALL_DEVICES:
        print(f"[*] Collecting data from {device['name']}...", end=" ")
        data = collect_device_data(device)
        devices_data.append(data)
        if data["reachable"]:
            print(Fore.GREEN + f"OK — {len(data['interfaces'])} interfaces")
        else:
            print(Fore.RED + "UNREACHABLE")

    reachable = sum(1 for d in devices_data if d["reachable"])
    unreachable = len(devices_data) - reachable

    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        timestamp=timestamp,
        total_devices=len(devices_data),
        reachable=reachable,
        unreachable=unreachable,
        devices=devices_data,
    )

    with open(filepath, "w") as f:
        f.write(html_content)

    print(Fore.GREEN + f"\n[+] Report saved: reports/{filename}")
    print(f"[+] Open in browser: file:///{filepath}")
    print("="*55 + "\n")

if __name__ == "__main__":
    generate_report()
