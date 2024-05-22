"""Remote Operations Handler class for ssh connection and scp file transfer"""
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient


class RemoteHandler:
    """Paramiko and scp based remote handler class"""

    def __init__(self):
        self.stdin = ""
        self.stdout = ""
        self.stderr = ""

        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def connect(self,  host, user, passwd):
        """Connect to SSH host
        """
        self.client.connect(
            hostname=host, username=user, password=passwd)

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

    def send_file(self, filename):
        """Send file via scp

        :param filename: name of the file to be sent
        :type filename: str
        """
        scp = SCPClient(self.client.get_transport())
        scp.put(filename, f"/tmp/{filename}")
        scp.close()
