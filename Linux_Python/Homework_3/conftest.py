import random
import string
import subprocess

import pytest
import yaml
from datetime import datetime

from cmd_run import run

with open('config.yaml') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    run("mkdir -p {} {} {}".format(data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")
    return data["folder_in"], data["folder_ext"], data["folder_ext2"]


@pytest.fixture()
def clear_folders():
    return run("rm -rf {}/* {}/* {}/*".format(data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if run("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not run("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not run("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start time: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

    yield
    print("End time: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

@pytest.fixture()
def make_error_arhive():
    run("cd {}; 7z a {}".format(data["folder_in"], data["archive_error"]), "")
    run("cd {}; truncate -s 1 {}".format(data["folder_in"], data["archive_error"]), "")

    yield
    run(" rm {}".format(data["archive_error"]), "")

@pytest.fixture()
def statistic():
    yield
    cpu = subprocess.run("cat /proc/loadavg", shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    stat = "time={}; count={}; size={}; cpu={}".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], cpu.stdout)
    #print(stat)
    with open("stat.txt", "a") as stat_file:
        stat_file.write(stat)




    #run("cd {}; echo {} >> stat.txt".format("/home/user/PycharmProjects/pythonProject/GB/lesson3", stat), "")