"""SSH client for connecting to host clusters"""
from paramiko import SSHClient, AutoAddPolicy


class sshClient:
    def __init__(self):
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.host = ""  # TODO: find out host address
        self.user = "admin"  # TODO: find out available user

    def connect(self):
        self.client.connect(hostname=self.host, username=self.user)
        return 0

    def close(self):
        self.client.close()
        return 0
