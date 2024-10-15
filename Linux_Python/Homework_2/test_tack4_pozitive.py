from cmd_run import run

folder_in = "/home/user/test"
archive = "/home/user/test.7z"
folder_ext = "/home/user/test"

def test_step6():
    res1 = run("7z a {}/home/user/test.7z".format(folder_in), "Everything is Ok")
    res2 = run("ls {}".format(archive), "/home/user/test.7z")
    assert res1 and res2, "test6 FAIL"

def test_step7():
    res1 = run("7z e /home/user/test.7z -o{} -y".format(folder_ext), "Everything is Ok")
    res2 = run("ls {}".format(folder_ext), "abc.py")
    res3 = run("ls {}".format(folder_ext), "actions.py")
    assert res1 and res2 and res3, "test7 FAIL"