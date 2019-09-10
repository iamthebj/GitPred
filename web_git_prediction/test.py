import os
import re
import subprocess
env_path = 'C:/Program Files/Java/jdk1.7.0_80/bin'
cmd = 'java -jar C:/Users/biswajit_nath/Desktop/checkstyle-5.8-all.jar -c C:/Users/biswajit_nath/Desktop/google_checks.xml demofile.java'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               env=dict(os.environ, PATH=env_path)).communicate(0)
print(process)