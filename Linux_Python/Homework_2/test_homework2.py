from cmd_run import run


archive = "/home/user/test.7z"


def test_step8():
    assert run("7z l {}".format(archive), "Scanning the drive for archives"), "test8 FAIL"


def test_step9():
    res1 = run("7z e {} -y".format(archive), "Everything is Ok")
    res2 = run("7z x {} -y".format(archive), "Everything is Ok")
    assert res1 and res2, "test9 FAIL"
