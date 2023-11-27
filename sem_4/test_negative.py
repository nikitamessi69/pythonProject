import yaml

from sem_4.sshcheckers import ssh_checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_files, make_folders, clear_folders, make_bad_arx):
        # test1
        result1 = ssh_checkout_negative("0.0.0.0", "user2", "assoll1987",
                                        "cd {}; 7z e bad_arx.7z -o{} -y -t{}".format(data["folder_out"],
                                                                                     data["folder_ext"],
                                                                                     data["archive_type"]),
                                        "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, make_bad_arx):
        # test2
        assert ssh_checkout_negative("0.0.0.0", "user2", "assoll1987",
                                     "cd {}; 7z t bad_arx.7z -t{}".format(data["folder_out"], data["archive_type"]),
                                     "ERRORS"), "test2 FAIL"
