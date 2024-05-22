"""Remote operations using the Remote Handler class"""
import hashlib
from .handler import RemoteHandler


def send_file(hostname, filename):
    if hostname == "atena02":
        host = "slurmmanager"
        user = "admin"
        passwd = "admin"
    remote = RemoteHandler()
    remote.connect(host, user, passwd)
    remote.send_file(filename)


def assert_integrity(remote, filename):
    """Assert local and remote file integrity

    :param remote: remote handler instance
    :type remote: RemoteHandler
    :param filename: _description_
    :type filename: _type_
    :return: _description_
    :rtype: _type_
    """
    with open(filename, 'r', encoding='utf-8') as f:
        local_hash = hashlib.md5(str(f.read()).encode('utf-8')).hexdigest()
    remote.exec(f"md5sum /tmp/{filename}")
    remote_hash = remote.get_output()
    print(f"Local hash: {local_hash}")
    print(f"Remote hash: {remote_hash}")
    if local_hash == remote_hash:
        return True
    return False
