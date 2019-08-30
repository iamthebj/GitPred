import subprocess
import os

cmd = 'g++ test.cpp'
path = 'C:/MinGW/bin'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, env=dict(os.environ, PATH=path)).communicate(0)
print (process)