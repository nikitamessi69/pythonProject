import subprocess
import string

def check_output(command, text, word_mode=False):
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        if not word_mode:
            if text in output:
                return True
            else:
                return False
        else:
            output_words = output.split()
            cleaned_words = [word.strip(string.punctuation) for word in output_words]
            if text in cleaned_words:
                return True
            else:
                return False
    except subprocess.CalledProcessError:
        return False

command = "rm --help"
text = "verbose"
result = check_output(command, text, word_mode=True)
print(result)
