import subprocess

def run(command, text):
    result = subprocess.run(command, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False

def test_run():
    assert True == run("ls", "pythonProject"), "Test Failed"
