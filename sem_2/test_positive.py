import subprocess
import zlib

tst = "/home/gb/tst"
out = "/home/gb/out"
folder1 = "/home/gb/folder1"


def calculate_crc32(hash):
    result = subprocess.run(["crc32", hash], stdout=subprocess.PIPE, encoding='utf-8')
    crc32_hash = result.stdout.strip()
    return crc32_hash


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    # test1
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "test1 FAIL"


def test_step2():
    # test2
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "qwe")
    result3 = checkout("cd {}; ls".format(folder1), "rty")
    assert result1 and result2 and result3, "test2 FAIL"


def test_step3():
    # test3
    assert checkout("cd {}; 7z t arx2.7z".format(out, folder1), "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout("cd {}; 7z u {}/arx2.7z".format(tst, out), "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    assert checkout("cd {}; 7z d arx2.7z".format(out), "Everything is Ok"), "test5 FAIL"


def test_step6():
    # test6
    result1 = checkout("cd {}; 7z l arx2.7z".format(out), "arx2.7z")
    assert result1, "test6 FAIL"


def test_step7():
    # test7
    result1 = checkout("cd {}; 7z x arx2.7z -o{}".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "qwe")
    result3 = checkout("cd {}; ls".format(folder1), "rty")
    assert result1 and result2 and result3, "test7 FAIL"


def test_step8():
    # test8
    hash = "{}/arx2.7z".format(out)
    expected_hash = "104dfd7b"
    calculated_hash = calculate_crc32(hash)
    assert calculated_hash == expected_hash, "test8 FAIL"


def test_all_steps():
    test_step1()
    test_step2()
    test_step3()
    test_step4()
    test_step5()
    test_step6()
    test_step7()
    test_step8()


test_all_steps()
