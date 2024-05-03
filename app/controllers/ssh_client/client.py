"""SSH client for connecting to host clusters"""
from paramiko import SSHClient, AutoAddPolicy


class RemoteClient:
    """Paramiko based remote ssh client to connect to cluster host"""
    def __init__(self):
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.host = ""  # TODO: find out host address
        self.user = "admin"  # TODO: find out available user

    def connect(self):
        """SSH open connection call

        :return: 0 if ok
        :rtype: int
        """
        self.client.connect(hostname=self.host, username=self.user)
        return 0

    def close(self):
        """SSH close connection call

        :return: 0 if ok
        :rtype: int
        """
        self.client.close()
        return 0
