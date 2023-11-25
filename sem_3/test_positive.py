import subprocess
import yaml
from sem_3.checkers import checkout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def calculate_crc32(hash):
    result = subprocess.run(["crc32", hash], stdout=subprocess.PIPE, encoding='utf-8')
    crc32_hash = result.stdout.strip()
    return crc32_hash


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        result1 = checkout(
            "cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["archive_type"]),
            "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        result1 = checkout(
            "cd {}; 7z e arx2.7z -o{} -y -t{}".format(data["folder_out"], data["folder_ext"], data["archive_type"]),
            "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["folder_ext"]), make_files[0])
        assert result1 and result2, "test2 FAIL"

    def test_step3(self, clear_folders, make_files):
        # test3
        assert checkout("cd {}; 7z t arx2.7z -t{}".format(data["folder_out"], data["archive_type"]),
                        "Everything is Ok"), "test3 FAIL"

    def test_step4(self, clear_folders, make_files):
        # test4
        assert checkout(
            "cd {}; 7z u {}/arx2.7z -t{}".format(data["folder_in"], data["folder_out"], data["archive_type"]),
            "Everything is Ok"), "test4 FAIL"

    def test_step5(self):
        # test5
        assert checkout("cd {}; 7z d arx2.7z -t{}".format(data["folder_out"], data["archive_type"]),
                        "Everything is Ok"), "test5 FAIL"

    def test_step6(self):
        # test6
        result1 = checkout("cd {}; 7z l arx2.7z -t{}".format(data["folder_out"], data["archive_type"]), "arx2.7z")
        assert result1, "test6 FAIL"

    def test_step7(self):
        # test7
        result1 = checkout(
            "cd {}; 7z x arx2.7z -o{} -t{}".format(data["folder_out"], data["folder_ext"], data["archive_type"]),
            "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["folder_ext"]), "qwe")
        result3 = checkout("cd {}; ls".format(data["folder_ext"]), "rty")
        assert result1 and result2 and result3, "test7 FAIL"

    def test_step8(self):
        # test8
        hash = "{}/arx2.7z".format(data["folder_out"])
        expected_hash = "104dfd7b"
        calculated_hash = calculate_crc32(hash)
        assert calculated_hash == expected_hash, "test8 FAIL"
