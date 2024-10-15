from sshrun import Ssh, ssh_run_sudo, upload_files
from Config import Config

config = Config("config.yaml")

def deploy(package_name):
    success = []
    upload_files(config, "/home/user/PycharmProjects/pythonProject/GB/tests/{}.deb".format(package_name),
                 "{}/{}.deb".format(config.user_home, package_name))
    ssh = Ssh(config).connect()

    response = ssh.run_sudo("dpkg -i {}/{}.deb".format(config.user_home, package_name))
    success.append(response.contains("Настраивается пакет"))

    response = ssh.run_sudo("dpkg -s {}".format(package_name))
    success.append(response.contains("Status: install ok installed"))

    ssh.close()
    return all(success)


def remove(package_name):
    return ssh_run_sudo(config=config, cmd=("dpkg -r %s" % package_name), text="Удаляется")