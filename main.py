#import telnetlib
import paramiko
from contextlib import contextmanager

devices =[ 
        {
            "hostname": "127.0.0.1",
            "username": "vagrant",
            "password": "vagrant",
            "port": 2222,
            "type": "linux",
            "gather": ["hostname", "network"],
            "transport": "ssh",
        }
]

COMMANDS = {
        "linux": [{
            "hostname": ["hostname", "dnsdomainname"],
            "network": ["ip addr show"]#, "ip addr {eth0}"],
        }]
}

PARSING = {
    "linux": {
        "hostname": lambda x: str(x),
        "network": lambda x: str(x),
        }
    }


class Transport(object):

    def connection(self, device):
        """Setup the connection with context manager"""
        raise NotImplemented

    def run_command(self, command, gathered_results):
        """Get command, and prevouis results,
        that may be needed to create new command"""
        raise NotImplemented

class SSHTransport(Transport):
    def __init__(self):
        self.client = None

    @contextmanager
    def connection(self, device):
        # TODO device should refer but not contain credentials from db.
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.WarningPolicy)
            self.client.connect(device['hostname'], port=device['port'], username=device['username'], password=device['password'])
            yield
        finally:
            self.client.close()

    def run_command(self, command, gathered_results):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read(), stderr.read()

TRANSPORT = {
        "ssh": SSHTransport,
    }
from pprint import pprint as pp
for device in devices:
    results = {}
    transport = TRANSPORT[device.get('transport', 'ssh')]()
    with transport.connection(device):
        for round_, available_commands in enumerate(COMMANDS[device['type']]):
            for available_gather, commands in available_commands.items():
                for command in commands:
                    if available_gather not in device['gather']:
                        continue
                    stdout, stderr = transport.run_command(command, results) 
                    results['round {},{}'.format(round_, command)] = {'formatted': , 'stdout': stdout.read(), 'stderr': stderr.read()}

    pp(results)
