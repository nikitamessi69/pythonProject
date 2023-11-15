#import subprocess

#if __name__ == '__main__':
#    def check_output(command, text):
 #       output = subprocess.check_output(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
  #  if text in output:
   #     return True
    #else:
     #   return False

#command = "ls -l"
#text = "file.txt"
#result = check_output(command, text)
#print(result)


import subprocess
def check_text(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0:
        out = result.stdout
        if text in out:
            return True
        else:
            return False
    return f'wrong command: {cmd}'

if __name__ == '__main__':
    print(check_text('ls /home/gb', 'Страница справки по GNU'))
    print(check_text('rm --help', 'Страница справки по GNU'))
    print(check_text('cat /etc/os-release', 'Страница'))