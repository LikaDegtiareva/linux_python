from cmd_run import run, get

EVERYTHING_IS_OK = "Everything is Ok"

folder_in = "/home/user/folder_in"
archive = "/home/user/test.7z"
folder_ext = "/home/user/folder_ext"
folder_ext2 = "/home/user/folder_ext2"


def test_step1():
    # dobavlenie faylov v arhive i proverka sozdaniya faila arhiva
    res1 = run("cd /home/user/test; 7z a {}/home/user/test.7z".format(folder_in), "Everything is Ok")
    res2 = run("ls {}".format(archive), "test.7z")
    assert res1 and res2, "test1 FAIL"


def test_step2():
    # izvlechenie faylov is arhiva -o - zadaet direktoriu v kotor budut raspakov faily + proverka sozdaniya failov
    res1 = run("cd {}; 7z e /home/user/test.7z -o{} -y".format(folder_in, folder_ext), EVERYTHING_IS_OK)
    res2 = run("ls {}".format(folder_ext), "abc.py")
    res3 = run("ls {}".format(folder_ext), "actions.py")
    assert res1 and res2 and res3, "test2 FAIL"


def test_step3():
    # tselostnost arhiva
    assert run("cd {}; 7z t /home/user/test.7z".format(folder_in), EVERYTHING_IS_OK), "test3 FAIL"


def test_step4():
    # obnovlenie arhiva
    assert run("cd {}; 7z u {}".format(folder_in, archive), EVERYTHING_IS_OK), "test4 FAIL"


def test_step5():
    # vivod soderzhimogo arhiva s proverkoy sohraneniya strukturi faylov i papok
    res1 = run("cd {}; 7z l home/user/test.7z".format(folder_in, folder_ext), "abc.py")
    res2 = run("cd {}; 7z l home/user/test.7z".format(folder_in, folder_ext), "actions.py")
    assert res1 and res2, "test5 FAIL"


def test_step6():
    # izvlechenie failov is arhiva s putymi
    res1 = run("cd {}; 7z x /home/user/test.7z -o{} -y".format(folder_in, folder_ext2), "Everything is Ok")
    res2 = run("ls {}".format(folder_ext2), "abc.py")
    res3 = run("ls {}".format(folder_ext2), "ABC.py")
    res4 = run("ls {}".format(folder_ext2), "actions.py")
    res5 = run("ls {}".format(folder_ext2), "ACTIONS.py")
    assert res1 and res2 and res3 and res4 and res5, "test6 FAIL"


def test_step7():
    # udalenie is arhiva
    assert run("cd {}; 7z d /home/user/test.7z".format(archive), EVERYTHING_IS_OK), "test7 FAIL"

def test_step8():
    # raschet hesha + proverka chto hesh sovpadaet s rasschitanym komandoi crc32
    res1 = run("cd {}; 7z h abcd.py".format(folder_in), "Everything is Ok")
    hash = get("cd {}; crc32 abcd.py".format(folder_in))
    res2 = run("cd {}; 7z h abcd.py".format(folder_in), hash.upper())
    assert res1 and res2, "test8 FAIL"






