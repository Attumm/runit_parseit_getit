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
        }, {
            "hostname": "processing",
            "ip": "172.31.136.59",
            "username": "mbijman",
            "password": password,
            "port": 22,
            "type": "linux",
            "transport": "ssh",
        }
]
# test only on device
from list_of_observer_ip import ips
dev_ips = [i for i in ips if i['use'] == "DEV"]
devices = [
        {
            "hostname": i["hostname"],
            "ip": i["ip"],
            "username": "mbijman",
            "password": password,
            "port": 22,
            "type": "linux",
            "transport": "netmiko",
            } for i in dev_ips
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
def command(title, command, fact=None):
    return locals()


COMMANDS = {
        "linux": [{
            "hostname": [
                command("hostname", "hostname"),
                #command("hostname from dns", "dnsdomainname"),
                #command("distrubtion", "cat /etc/*-release"),
            ], 
            "network": [
                command("network information", "`which ip` addr show"), 
                command("ipv4 addresses", "hostname -I"),
                #command("ip addr on eht0", "ip addr show lo"),
                #command("ipv4", "hostname -I"),
                #command("hosts file dns", "cat /etc/hosts"),
                #command("neighbours", "ip neigh"),
                #command("show routing table", "ip route show"),
            ],
            "health": [
                command("display memory in kb", "cat /proc/meminfo"),
                #command("top ten processes by memory consumption", "ps -aux |sort -nrk 4| head -10 "),
                #command("top ten proceses by cpu consumtpion", "ps -aux |sort -nrk 3| head -10 "),
                command("cpu model", """cat /proc/cpuinfo | grep 'model name' | tail -n 1 | awk '{ print $4,$5,$6,$7 }'"""),
                command("cpu core", "cat /proc/cpuinfo | grep 'model name' | wc -l"),
                command("disk space", "df -h --total"),
                #command("current runlevel", "runlevel"),
                #command("display input", "echo 'hello world'")
            ],
        },
        #{"users": [command("current logged in users", "w"),]}
        ],
}


total = []
for device in devices:
    results = {}
    facts = {}
    transport = get_transport(device.get('transport'))
    try:
        with transport.connection(device):
            for round_, available_commands in enumerate(COMMANDS[device['type']]):
                for available_gather, commands in available_commands.items():
                    for command in commands:
                        result = transport.run_command(command['command'], results)
                        results[f'{command["title"]}'] = {
                            'command': command['command'],
                            'result': result,
                            'formatted': parse(device["type"], command['command'], result, results),
                        }

    except FailedDevice as e:
        print("device failed reason: ", e)

    total.append(results.copy())

import json
print(json.dumps(total))
