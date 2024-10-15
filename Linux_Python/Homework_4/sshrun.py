import paramiko

class Response:
    def __init__(self, status, content):
        self.status = status
        self.content = content

    def contains(self, text):
        return text in self.content and self.status == 0

    def containsError(self, text):
        return text in self.content and self.status > 0

class Ssh:
    def __init__(self, config):
        self.config = config
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
            hostname=self.config.host,
            username=self.config.user,
            password=self.config.password,
            port=self.config.port
        )
        return self

    def close(self):
        self.client.close()

    def run(self, command):
        print("\nSSH> {}".format(command))
        stdin, stdout, stderr = self.client.exec_command(command)
        status = stdout.channel.recv_exit_status()
        out = (stdout.read() + stderr.read()).decode("utf-8")
        print("\nstatus: {}\n{}".format(status, out))
        return Response(status, out)

    def run_sudo(self, command):
        return self.run("echo '{}' | sudo -S {}".format(self.config.password, command))

def ssh_run_sudo(config, cmd, text):
    ssh = Ssh(config).connect()
    try:
        return ssh.run_sudo(cmd).contains(text)
    finally:
        ssh.close()

def ssh_run(config, cmd, text):
    ssh = Ssh(config).connect()
    try:
        return ssh.run(cmd).contains(text)
    finally:
        ssh.close()

def upload_files(config, local_path, remote_path):
    print(f"Zagruzhaem file {local_path} v katalog {remote_path}")
    transport = paramiko.Transport((config.host, config.port))
    transport.connect(None, username=config.user, password=config.password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()

def download_files(config, remote_path, local_path):
    print(f"Zagruzhaem file {local_path} v katalog {remote_path}")
    transport = paramiko.Transport((config.host, config.port))
    transport.connect(None, username=config.user, password=config.password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()