
#import telnetlib
import paramiko
from contextlib import contextmanager

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
            self.client.connect(device['hostname'], port=device['port'],
                    username=device['username'], password=device['password'])
            yield
        except KeyError as e:#Exception as e:
            raise FailedDevice(e)

        finally:
            self.client.close()

    def run_command(self, command, gathered_results):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')


import telnetlib
class TelNetTransport(Transport):
    def __init__(self):
        self.client = None

    def to_bytes(self, s):
        return bytes(s, 'ascii')

    @contextmanager
    def connection(self, device):
        # TODO device should refer but not contain credentials from db.
        try:
            self.client = telnetlib.Telnet(self.to_bytes(device['hostname']))
            self.client.read_until(self.to_bytes("login: "))
            self.client.write(self.to_bytes(device['username'] + "\n"))
            self.client.read_until(self.to_bytes("Password: "))
            self.client.write(self.to_bytes(device['password'] + "\n"))
            yield
        except KeyError as e:#Exception as e:
            raise FailedDevice(e)

        finally:
            self.client.write(self.to_bytes("exit\n"))
            self.client.close()

    def run_command(self, command, gathered_results):
        self.client.write(self.to_bytes(command + "\n"))
        result = self.client.read_until(self.to_bytes('<will not be found'), timeout=0.1)
        result = result.decode('utf-8')[len(command)+1:]
        return result, None

TRANSPORT = {
        "ssh": SSHTransport,
        "telnet": TelNetTransport,
    }

def get_transport(transport):
    return TRANSPORT.get(transport, SSHTransport)()

class FailedDevice(Exception):
    """Device Failed for any reason"""
