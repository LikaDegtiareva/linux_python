from cmd_run import run_negative
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestNegative:

    def test_negstep1(self, make_error_arhive):
        assert run_negative("cd {}; 7z e {} -o{} -y".format(data["folder_in"], data["archive_error"], data["folder_ext"]), "ERROR"), "test1 FAIL"


    def test_negstep2(self, make_error_arhive):
        assert run_negative("cd {}; 7z t {}".format(data["folder_in"], data["archive_error"]), "ERROR"), "test2 FAIL"
