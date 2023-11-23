import yaml
from sem_3.checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self):
        # test1
        result1 = checkout_negative(
            "cd {}; 7z e bad_arx.7z -o{} -y -t{}".format(data["folder_out"], data["folder_ext"], data["archive_type"]),
            "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self):
        # test2
        assert checkout_negative("cd {}; 7z t bad_arx.7z -t{}".format(data["folder_out"], data["archive_type"]),
                                 "ERRORS"), "test2 FAIL"
