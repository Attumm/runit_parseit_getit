from transport import get_transport, FailedDevice
from parsing import parse

# get devices from invetory system
devices = [ 
        {
            "hostname": "processing",
            "ip": "192.168.33.11",
            "username": "vagrant",
            "password": "vagrant",
            "port": 23,
            "type": "linux",
            "transport": "telnet",
        }, {
            "hostname": "processing",
            "ip": "127.0.0.1",
            "username": "vagrant",
            "password": "vagrant",
            "port": 2222,
            "type": "linux",
            "transport": "ssh",
        }, {
            "hostname": "processing",
            "ip": "127.0.0.1",
            "username": "vagrant",
            "password": "vagrant",
            "port": 2222,
            "type": "linux",
            "transport": "netmiko",
        }
]

# set Commands for type,
# for each type there is an list of dictonaries
# name of the command as key, and commands to run second
# each dictionary in list counts as an round, there is no limit to rounds
# rounds are needed when previous data, is needed for subsequent commands

# this is place where we should add special cases.
# run one command
# run a list of commands
# run a list of commands with input from older commands

from collections import namedtuple
command = namedtuple('Command', 'title command')
COMMANDS = {
        "linux": [{
            "hostname": [
                command("hostname", "hostname"),
                command("hostname from dns", "dnsdomainname"),
            ], 
            "network": [
                command("network information", "ip addr show"), 
                command("ip addr on eht0", "ip addr show lo"),
                command("ipv4", "hostname -I"),
                command("hosts file dns", "cat /etc/hosts"),
                command("neighbours", "ip neigh"),
                command("show routing table", "ip route show"),
            ],
            "health": [
                command("display memory in megabytes", "free -m"),
                command("top ten processes by memory consumption", "ps -aux |sort -nrk 4| head -10 "),
                command("top ten proceses by cpu consumtpion", "ps -aux |sort -nrk 3| head -10 "),
                command("disk space", "df -h "),
                command("current runlevel", "runlevel"),
                command("display input", "echo 'hello world'")
            ],
        },{"users": [command("current logged in users", "w"),]}],
}


total = []
for device in devices:
    results = {}
    transport = get_transport(device.get('transport'))
    try:
        with transport.connection(device):
            for round_, available_commands in enumerate(COMMANDS[device['type']]):
                for available_gather, commands in available_commands.items():
                    for title, command in commands:
                        stdout, stderr = transport.run_command(command, results)
                        results[f'{title}'] = {
                            'command': command,
                            'stdout': stdout,
                            'stderr': stderr,
                            'formatted': parse(device["type"], command, stdout, stderr, results),
                        }

    except FailedDevice as e:
        print("device failed reason: ", e)

    total.append(results.copy())

import json
print(json.dumps(total))
