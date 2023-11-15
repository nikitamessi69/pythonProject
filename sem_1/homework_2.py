import subprocess
import string


def check_text(cmd, words):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    temp = result.stdout
    if result.returncode == 0:
        out = ''.join([' ' if p in string.punctuation else p for p in temp])
        if words in out:
            return True
        else:
            return False
    return f'wrong command: {cmd}'


if __name__ == '__main__':
    print(check_text('ls /home/home', 'snap'))
    print(check_text('rm --help', 'fooo'))

