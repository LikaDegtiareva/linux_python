from sshrun import Ssh
from Config import Config
from deploy import deploy, remove

config = Config("config.yaml")

package_name = "p7zip-full"

_7z_a = "7z a {}/{} {}".format(config.folder_in, config.archive_error, config.folder_in)
_7z_e = "7z e {}/{} -o{} -y".format(config.folder_in, config.archive_error, config.folder_ext)
_7z_t = "7z t {}/{}".format(config.folder_in, config.archive_error)
truncate_file = "truncate -s 1 {}/{}".format(config.folder_in, config.archive_error)

class TestNegative:

    def test_negstep1(self):
        ssh = Ssh(config).connect()
        try:
            deploy(package_name)
            ssh.run_sudo(_7z_a)
            ssh.run_sudo(truncate_file)
            success = ssh.run_sudo(_7z_e).containsError("ERROR")
            remove(package_name)
            assert success, "test1 FAIL"
        finally:
            ssh.close()

    def test_negstep2(self):
        ssh = Ssh(config).connect()
        try:
            deploy(package_name)
            ssh.run_sudo(_7z_a)
            ssh.run_sudo(truncate_file)
            success = ssh.run_sudo(_7z_t).containsError("ERROR")
            remove(package_name)
            assert success, "test1 FAIL"
        finally:
            ssh.close()
