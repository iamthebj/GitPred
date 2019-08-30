import subprocess
cmd = 'g++ test.cpp'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE).communicate(0)
print (process)