import random
import string
from datetime import datetime

import pytest
import yaml

from sem_4.checkers import getout
from sem_4.sshcheckers import upload_files, ssh_checkout, ssh_getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "assoll1987",
                        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"],
                                                      data["folder_ext2"]),
                        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "assoll1987",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 "
                        "iflag=fullblock".format(data["folder_in"], filename,
                                                 data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "assoll1987",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"],
                                                            data["folder_ext2"]), "")


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "assoll1987",
                 "cd {}; 7z a {}/bad_arx -t{}".format(data["folder_in"], data["folder_out"], data["archive_type"]),
                 "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "assoll1987",
                 "truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["archive_type"]), "Everything is Ok")
    yield "bad_arx"
    ssh_checkout("0.0.0.0", "user2", "assoll1987",
                 "rm -f {}/bad_arx.{}".format(data["folder_out"], data["archive_type"]), "")


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    ssh_getout("0.0.0.0", "user2", "assoll1987",
               "echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                              data["count"], data["bs"], stat), "")


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "assoll1987", "/home/gb/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "assoll1987", "echo 'assoll1987' | sudo -S dpkg -i "
                                                              "/home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "assoll1987", "echo 'assoll1987' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok. installed"))
    return all(res)


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def journalctl(start_time):
    cmd = f"journalctl --since '{start_time}'"
    output = getout(cmd)
    with open("stat.txt", "a") as f:
        f.write(output)
    return output
