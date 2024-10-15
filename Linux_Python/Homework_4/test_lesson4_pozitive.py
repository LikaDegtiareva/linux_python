import subprocess

from Config import Config
from deploy import deploy, remove
from sshrun import Ssh

package_name = "p7zip-full"
config = Config("config.yaml")

EVERYTHING_IS_OK = "Everything is Ok"
_7z_a = "7z a -t{} {}/{} {}".format(config.type, config.folder_in, config.archive, config.folder_in)
_7z_e = "7z e {}/{} -o{} -y".format(config.folder_in, config.archive, config.folder_ext)
_7z_x = "7z x {}/{} -o{} -y".format(config.folder_in, config.archive, config.folder_ext2)
_7z_l = "7z l {}/{}".format(config.folder_in, config.archive)
_7z_t = "7z t {}/{}".format(config.folder_in, config.archive)
_7z_u = "7z u {}/{}".format(config.folder_in, config.archive)
_7z_d = "7z d {}/{}".format(config.folder_in, config.archive)

class TestPositive:

    def test_deploy(self, start_time):
        success_deploy = deploy(package_name)
        self.save_log(start_time, "journal.txt")
        success_remove = remove(package_name)
        assert success_deploy and success_remove, "test_deploy FAIL"

    def test_step1(self, make_folders, clear_folders, make_files, statistic):
        # dobavlenie faylov v arhive i proverka sozdaniya faila arhiva
        deploy(package_name)
        ssh = Ssh(config).connect()
        try:
            res1 = ssh.run_sudo(_7z_a).status == 0
            res2 = ssh.run("ls {}".format(config.folder_in)).contains(config.archive)
            remove(package_name)
            assert res1 and res2, "test1 FAIL"
        finally:
            ssh.close()

    def test_step2(self, make_folders, clear_folders, make_files, statistic):
        # vse result dobavim v odny peremennyu - success, dobavlenie failov v arhive, izvlechenie faylov is arhiva -o - zadaet direktoriu v kotor budut raspakov faily + proverka sozdaniya failov
        deploy(package_name)
        ssh = Ssh(config).connect()
        try:
            success = []
            success.append(ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK))
            success.append(ssh.run_sudo(_7z_e).contains(EVERYTHING_IS_OK))
            for item in make_files:
                success.append(ssh.run("ls {}".format(config.folder_ext)).contains(item))
            remove(package_name)
            assert all(success), "test2 FAIL"
        finally:
            ssh.close()

    def test_step3(self, make_folders, clear_folders, make_files, statistic):
        # tselostnost arhiva
        deploy(package_name)
        ssh = Ssh(config).connect()
        try:
            ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK)
            success = ssh.run_sudo(_7z_t).contains(EVERYTHING_IS_OK)
            remove(package_name)
            assert success, "test3 FAIL"
        finally:
            ssh.close()

    def test_step4(self, make_folders, clear_folders, make_files, statistic):
        # obnovlenie arhiva
        deploy(package_name)
        ssh = Ssh(config).connect()
        try:
            success1 = ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK)
            success2 = ssh.run_sudo(_7z_u).contains(EVERYTHING_IS_OK)
            remove(package_name)
            assert success1 and success2, "test4 FAIL"
        finally:
            ssh.close()

    def test_step5(self, make_folders, clear_folders, make_files, statistic):
        # vivod soderzhimogo arhiva s proverkoy sohraneniya strukturi faylov i papok
        deploy(package_name)
        ssh = Ssh(config).connect()
        success = []
        try:
            success.append(ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK))
            for item in make_files:
                success.append(ssh.run_sudo(_7z_l).contains(item))
            remove(package_name)
            assert all(success), "test5 FAIL"
        finally:
            ssh.close()

    def test_step6(self, make_folders, clear_folders, make_files, make_subfolder, statistic):
        # izvlechenie failov is arhiva s putymi
        deploy(package_name)
        ssh = Ssh(config).connect()
        success = []
        try:
            success.append(ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK))
            success.append(ssh.run_sudo(_7z_x).contains(EVERYTHING_IS_OK))

            response = ssh.run("ls {}/{}".format(config.folder_ext2, config.working_folder))
            success.append(response.contains(make_subfolder[0]))
            for item in make_files:
                success.append(response.contains(item))

            ls_subfolder = "ls {}/{}/{}".format(config.folder_ext2, config.working_folder, make_subfolder[0])
            success.append(ssh.run(ls_subfolder).contains(make_subfolder[1]))
            remove(package_name)
            assert all(success), "test6 FAIL"
        finally:
            ssh.close()

    def test_step7(self, make_folders, clear_folders, make_files, statistic):
        # udalenie is arhiva
        deploy(package_name)
        ssh = Ssh(config).connect()
        try:
            success1 = ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK)
            success2 = ssh.run_sudo(_7z_d).contains(EVERYTHING_IS_OK)
            remove(package_name)
            assert success1 and success2, "test7 FAIL"
        finally:
            ssh.close()

    def test_step8(self, make_folders, clear_folders, make_files, statistic):
        # raschet hesha + proverka chto hesh sovpadaet s rasschitanym komandoi crc32
        deploy(package_name)
        ssh = Ssh(config).connect()
        success = []
        try:
            success.append(ssh.run_sudo(_7z_a).contains(EVERYTHING_IS_OK))
            for item in make_files:
                success.append(ssh.run_sudo("7z h {}/{}".format(config.folder_in, item)).contains(EVERYTHING_IS_OK))
                hash = ssh.run("crc32 {}/{}".format(config.folder_in, item)).content
                success.append(ssh.run_sudo("7z h {}/{}".format(config.folder_in, item)).contains(hash.upper()))
            assert all(success), "test8 FAIL"
        finally:
            ssh.close()

    def save_log(self, since, to_filename):
        log = subprocess.run("journalctl --since '{}'".format(since), shell=True, stdout=subprocess.PIPE,
                             encoding='utf-8')

        with open(to_filename, "a") as file:
            file.write(log.stdout)
