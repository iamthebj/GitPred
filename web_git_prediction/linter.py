import os
import subprocess
import urllib
import logging

import requests

log = logging.getLogger(__name__)

def lint(payload):
    global syntax_check, process, cmd, comment_body
    if not payload['action'] == 'closed':
        url = payload['pull_request']['url']
        url = url + '/files'
        r = requests.get(url)
        a = r.json()
        # print(a)
        print("Received Pull Request for %d Changed Files" % (len(a)))
        print("Initializing Linting Process")
        i = 0
        x = []
        filelist = []
        for i in range(len(a)):
            raw = (a[i]['raw_url'])
            # print(raw)
            filename = (a[i]['filename']).split("/")
            file = filename[-1]

            re = urllib.request.urlopen('%s' % raw)
            # returned_value = os.system("start \"\" %s" %raw)
            data = re.read()
            dst = open("%s" % file, "wb")
            dst.write(data)
            dst = open("%s" % file, "r")
            #print("Checking syntax errors for File: %d. %s" % (i + 1, file))

            file_ext = (file).split(".")
            #print("File extension of the file: %s" % file_ext[-1])
            # HARD CODES FOR LINTERS
            lint = None
            # PHP
            if file_ext[-1] == 'php':
                lint = 'D:/biswajit/gitpred/Linters/php/php.exe -l'
            # PY
            elif file_ext[-1] == 'py':
                lintpy = 'pycodestyle'
                env_path = 'D:/biswajit/gitpred/web_git_prediction/'
                cmd = '%s %s' % (lintpy, file)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           env=dict(os.environ, PATH=env_path)).communicate(0)
                syntax_check = ""
                for i in range(len(process)):
                    syntax_check = syntax_check + process[i].decode("utf_8")
            # C
            elif file_ext[-1] == 'c':
                env_path = 'D:/biswajit/gitpred/MinGW/bin'
                lintgcc = 'gcc'
                #print("Cloned file: %s deleted" % file)
                #print("Linting file : %s" % file)
                cmd = '%s %s' % (lintgcc, file)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, universal_newlines=True,
                                           env=dict(os.environ, PATH=env_path)).communicate(0)
                syntax_check = str(process).split(", b'")[-1]
            # CPP
            elif file_ext[-1] == 'cpp':
                env_path = 'D:/biswajit/gitpred/MinGW/bin'
                lintgpp = 'g++'
                #print("Cloned file: %s deleted" % file)
                #print("Linting file : %s" % file)
                cmd = '%s %s' % (lintgpp, file)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True,
                                           stderr=subprocess.PIPE,
                                           env=dict(os.environ, PATH=env_path)).communicate(0)
                syntax_check = str(process).split(", b'")[-1]

            # JAVA
            #elif file_ext[-1] == 'java':
                #env_path = 'C:/Program Files/Java/jdk1.7.0_80/bin'
                #lintgpp = 'javac'
                #print("Cloned file: %s deleted" % file)
                #print("Linting file : %s" % file)
                #cmd = '%s %s' % (lintgpp, file)
                #process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           #stderr=subprocess.PIPE,
                                           #env=dict(os.environ, PATH=env_path)).communicate(0)
                # syntax_check = str(process).replace("\\n", "")[6:-1]
                #syntax_check = ""
                #for i in range(len(process)):
                    #syntax_check = syntax_check + process[i].decode("utf_8")


            else:
                print("No linter found for %s extension" % file_ext[-1])
                s = "No linter found for %s extension" % file_ext[-1]

            if (lint != None):
                #print("Cloned file: %s deleted" % file)
                #print("Linting file : %s" % file)
                cmd = '%s %s' % (lint, file)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE).communicate(0)
                syntax_check = ""
                for i in range(len(process)):
                    syntax_check = syntax_check + process[i].decode("utf_8")
            # p = str(p)
            # p = p[2:-1]
            if process == "b''":
                q = "No syntax error found"
                print(q)

            else:
                #print("Syntax error found: %s" % syntax_check)
                #app.logger.info("Syntax Error Found: %s", syntax_check)
                q = "Syntax error found"
                filelist.append(file)

            dst.close()
            os.remove("%s" % file)
            s = "%s %s" % (q, syntax_check)
            x.append(s)
            i = i + 1
        if x is None:
            comment_body = "Git Assist Prediction : No Syntax Errors Found."
            x = []
        else:
            filelist = list(dict.fromkeys(filelist))
            filelist = ', '.join(filelist)
            comment_body = "Git Assist Prediction: To Be Rejected." \
                           "Syntax Errors found in the following files: %s." % filelist
            x = []
        return comment_body