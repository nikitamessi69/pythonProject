import string
import random
from datetime import time, datetime
import pytest
import yaml

from sem_3.checkers import checkout, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return checkout(
        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]),
        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename,
                                                                                           data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"],
                                                        data["folder_ext2"]), "")


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/bad_arx -t{}".format(data["folder_in"], data["folder_out"], data["archive_type"]),
             "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["archive_type"]), "Everything is Ok")
    yield "bad_arx"
    checkout("rm -f {}/bad_arx.{}".format(data["folder_out"], data["archive_type"]), "")


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                            data["count"], data["bs"], stat), "")
