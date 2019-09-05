import os
import re
import subprocess
env_path = 'C:/Program Files/Java/jdk1.7.0_80/bin'
cmd = 'javac demofile.java'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               env=dict(os.environ, PATH=env_path)).communicate(0)
output_string = ""
for i in range(len(process)):
    output_string = output_string + process[i].decode("utf_8")
    output_string = output_string.replace(":", "-")
    print(output_string)