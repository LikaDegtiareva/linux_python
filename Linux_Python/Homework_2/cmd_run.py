import subprocess


def run(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def run_negative(cmd, text):
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, encoding='utf-8')
    if result.returncode != 0 and text in result.stderr:
        return True
    else:
        return False