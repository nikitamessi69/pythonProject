import subprocess
def check_output(command, text):
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        if text in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

command = "cat /etc/os-release"
text = "POLICY"
result = check_output(command, text)
print(result)