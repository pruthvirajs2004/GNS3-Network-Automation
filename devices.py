# devices.py — Central device inventory for all automation scripts

ROUTERS = [
    {
        "name": "R1",
        "device_type": "cisco_ios",
        "host": "192.168.100.200",
        "username": "admin",
        "password": "cisco",
        "port": 22,
        "role": "Gateway Router",
    },
]

SWITCHES = [
    {
        "name": "SW1",
        "device_type": "cisco_ios",
        "host": "192.168.100.201",
        "username": "admin",
        "password": "cisco",
        "port": 22,
        "role": "Access Switch",
    },
]

ALL_DEVICES = ROUTERS + SWITCHES
