"""SSH client for connecting to host clusters"""
import socket
from paramiko import SSHClient, AutoAddPolicy


class RemoteClient:
    """Paramiko based remote ssh client to connect to cluster host"""

    def __init__(self):
        self.host = "slurmmanager"
        self.user = "admin"
        self.passwd = "admin"
        self.stdin = ""
        self.stdout = ""
        self.stderr = ""

        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def connect(self):
        """Connect to SSH host
        """
        self.client.connect(
            hostname=self.host, username=self.user, password=self.passwd)

    def close(self):
        """SSH close connection call
        """
        self.client.close()

    def exec(self, command):
        """Execute command given

        :param command: command to be executed at host
        :type command: str
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def get_output(self):
        """Get standard output of latest command executed

        :return: stdout of latest command
        :rtype: str
        """
        return self.stdout.read().decode('utf8')
