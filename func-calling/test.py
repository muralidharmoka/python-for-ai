#this programs demonstrates how a shell command is executed.
import subprocess

#second LLM Call
def run_shell(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

result = run_shell("dir")
print("RESULT: ", result)
