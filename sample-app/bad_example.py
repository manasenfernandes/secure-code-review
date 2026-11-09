import subprocess

def run(cmd_list):
    return subprocess.call(cmd_list, shell=False)