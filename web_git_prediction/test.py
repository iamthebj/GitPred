import subprocess
import os

cmd = 'g++ test.cpp'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, env=dict(os.environ, PATH="C:/MinGW/bin")).communicate(0)
print (process)