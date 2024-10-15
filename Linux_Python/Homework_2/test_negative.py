from cmd_run import run_negative

folder_in = "/home/user/test"
archive_error = "/home/user/test-error.7z"
folder_ext = "/home/user/test_1"

def test_negstep1():
    # esli raspakovat isporcheniy arxiv, to budet oshibka
    assert run_negative("7z e {} -o{} -y".format(archive_error, folder_ext), "ERROR"), "test1 FAIL"


def test_negstep2():
    # esli proverit isporcheniy arhive, to budet oshibka
    assert run_negative("7z t {}".format(archive_error), "ERROR"), "test2 FAIL"
