from cmd_run import run

EVERYTHING_IS_OK = "Everything is Ok"

folder_in = "/home/user/test"
archive = "/home/user/test.7z"
folder_ext = "/home/user/test"

def test_step1():
    assert run("7z a /home/user/test", EVERYTHING_IS_OK), "test1 FAIL"


def test_step2():
    assert run("7z e /home/user/test.7z -o/home/user/test -y", EVERYTHING_IS_OK), "test2 FAIL"


def test_step3():
    assert run("7z t /home/user/test.7z", EVERYTHING_IS_OK), "test3 FAIL"


def test_step4():
    assert run("7z u {}".format(folder_in), EVERYTHING_IS_OK), "test4 FAIL"


def test_step5():
    assert run("7z d {}".format(archive), EVERYTHING_IS_OK), "test5 FAIL"
