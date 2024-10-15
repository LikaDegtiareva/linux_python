import yaml

from cmd_run import run, get

with open('config.yaml') as f:
    data = yaml.safe_load(f)

EVERYTHING_IS_OK = "Everything is Ok"

class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files, statistic):
        # dobavlenie faylov v arhive i proverka sozdaniya faila arhiva
        res1 = run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK)
        res2 = run("ls {}".format(data["folder_in"]), data["archive"])
        assert res1 and res2, "test1 FAIL"


    def test_step2(self, make_folders, clear_folders, make_files, statistic):
        # vse result dobavim v odny peremennyu - res, dobavlenie failov v arhive, izvlechenie faylov is arhiva -o - zadaet direktoriu v kotor budut raspakov faily + proverka sozdaniya failov
        res = []
        res.append(run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK))
        res.append(run("cd {}; 7z e {} -o{} -y".format(data["folder_in"], data["archive"], data["folder_ext"]), EVERYTHING_IS_OK))
        for item in make_files:
            res.append(run("ls {}".format(data["folder_ext"]), item))
        assert all(res), "test2 FAIL"


    def test_step3(self, make_folders, clear_folders, make_files, statistic):
        # tselostnost arhiva
        run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK)
        assert run("cd {}; 7z t {}".format(data["folder_in"], data["archive"]), EVERYTHING_IS_OK), "test3 FAIL"


    def test_step4(self, make_folders, clear_folders, make_files, statistic):
        # obnovlenie arhiva
        run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK)
        assert run("cd {}; 7z u {}".format(data["folder_in"], data["archive"]), EVERYTHING_IS_OK), "test4 FAIL"


    def test_step5(self, make_folders, clear_folders, make_files, statistic):
        # vivod soderzhimogo arhiva s proverkoy sohraneniya strukturi faylov i papok
        res = []
        res.append(run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK))
        for item in make_files:
            res.append(run("cd {}; 7z l {}".format(data["folder_in"], data["archive"]), item))
        assert all(res), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder, statistic):
        # izvlechenie failov is arhiva s putymi
        res = []
        res.append(run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK))
        res.append(run("cd {}; 7z x {} -o{} -y".format(data["folder_in"], data["archive"], data["folder_ext2"]), EVERYTHING_IS_OK))

        for item in make_files:
            res.append(run("ls {}".format(data["folder_ext2"]), item))

        res.append(run("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(run("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"


    def test_step7(self, make_folders, clear_folders, make_files, statistic):
        # udalenie is arhiva
        run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK)
        assert run("cd {}; 7z d {}".format(data["folder_in"], data["archive"]), EVERYTHING_IS_OK), "test7 FAIL"

    def test_step8(self, make_folders, clear_folders, make_files, statistic):
        # raschet hesha + proverka chto hesh sovpadaet s rasschitanym komandoi crc32
        res = []
        run("cd {}; 7z a {} -t{}".format(data["folder_in"], data["archive"], data["type"]), EVERYTHING_IS_OK)
        for item in make_files:
            res.append(run("cd {}; 7z h {}".format(data["folder_in"], item), EVERYTHING_IS_OK))
            hash = get("cd {}; crc32 {}".format(data["folder_in"], item))
            res.append(run("cd {}; 7z h {}".format(data["folder_in"], item), hash.upper()))
        assert all(res), "test8 FAIL"






