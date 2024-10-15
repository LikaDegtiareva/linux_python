import pytest
import random
import string
from datetime import datetime
from sshrun import Ssh, ssh_run, ssh_run_sudo
from Config import Config
import subprocess

config = Config("config.yaml")

@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pytest.fixture()
def make_folders():
    ssh_run_sudo(config, "mkdir -p {} {} {}".format(config.folder_in, config.folder_ext, config.folder_ext2), "")
    return config.folder_in, config.folder_ext, config.folder_ext2

@pytest.fixture()
def clear_folders():
    return ssh_run_sudo(config, "rm -rf {}/* {}/* {}/*".format(config.folder_in, config.folder_ext, config.folder_ext2), "")

@pytest.fixture()
def make_files():
    list_of_files = []
    ssh = Ssh(config).connect()
    try:
        for i in range(config.count):
            filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            ssh.run_sudo("dd if=/dev/urandom of={}/{} bs={} count=1 iflag=fullblock".format(config.folder_in, filename, config.bs))
            list_of_files.append(filename)
        return list_of_files
    finally:
        ssh.close()

@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    ssh = Ssh(config).connect()
    try:
        ssh.run_sudo("mkdir {}/{}".format(config.folder_in, subfoldername))
        ssh.run_sudo("dd if=/dev/urandom of={}/{}/{} bs=1M count=1 iflag=fullblock".format(config.folder_in, subfoldername, testfilename))
        return subfoldername, testfilename
    finally:
        ssh.close()

@pytest.fixture(autouse=True)
def print_time():
    print("Start time: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

    yield
    print("End time: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

@pytest.fixture()
def statistic():
    yield
    cpu = subprocess.run("cat /proc/loadavg", shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    stat = "time={}; count={}; size={}; cpu={}".format(
        datetime.now().strftime("%H:%M:%S.%f"),
        config.count,
        config.bs,
        cpu.stdout
    )
    #print(stat)
    with open("stat.txt", "a") as stat_file:
        stat_file.write(stat)
