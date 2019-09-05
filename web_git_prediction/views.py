'''api module'''
import subprocess
import urllib
import os

import flask
import logging

import requests
from flask import json, Flask
import json
from flask import request as rq
from flask import Response
from fetching_data.test_data import TestData
from web_git_prediction.app import app
from fetching_file_data.fetching_file_data import Fetch_file
from fetching_file_data.test_data import TestData1
from fetching_data.fetching_data import Fetch
from search.search import Search
from comments.comment import Comment

from store_model.store_model import StoreModel
import fetching_file_data.helper
from fetching_data import commit_api
from web_git_prediction import object_file_predict

log = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    """Index page"""
    return 'Welcome'


@app.route('/github/', methods=['GET', 'POST', 'HEAD'])
def api_github_message():
    """api for sending comments"""
    global syntax_check, process
    if rq.headers['Content-Type'] == 'application/json':
        my_info = json.dumps(rq.json)
        payload = json.loads(my_info)
        if not payload['action'] == 'closed':
            url = payload['pull_request']['url']
            url = url + '/files'
            comment_url = payload['pull_request']['comments_url']
            r = requests.get(url)
            a = r.json()
            #print(a)
            print("Received Pull Request for %d Changed Files"%(len(a)))
            print("Initializing Linting Process")
            i = 0
            x = []
            filelist = []
            for i in range(len(a)):
                raw = (a[i]['raw_url'])
                #print(raw)
                filename = (a[i]['filename']).split("/")
                file = filename[-1]

                re = urllib.request.urlopen('%s' % raw)
                # returned_value = os.system("start \"\" %s" %raw)
                data = re.read()
                dst = open("%s" % file, "wb")
                dst.write(data)
                dst = open("%s" % file, "r")
                print("Checking syntax errors for File: %d. %s" %(i+1, file))

                file_ext = (file).split(".")
                print("File extension of the file: %s" % file_ext[-1])
                # HARD CODES FOR LINTERS
                lint = None
                # PHP
                if file_ext[-1] == 'php':
                    lint = 'C:/Users/biswajit_nath/Desktop/text_gitpredictions/Linters/php/php.exe -l'
                # PY
                elif file_ext[-1] == 'py':
                    lint = 'pycodestyle'
                    env_path = 'C:/Users/biswajit_nath/AppData/Local/Programs/Python/Python37-32/Lib/site-packages'
                #C
                elif file_ext[-1] == 'c':
                    env_path = 'C:/MinGW/bin'
                    lintgcc = 'gcc'
                    print("Cloned file: %s deleted" % file)
                    print("Linting file : %s" % file)
                    cmd = '%s %s' % (lintgcc, file)
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, universal_newlines=True,
                                               env=dict(os.environ, PATH=env_path)).communicate(0)
                    syntax_check = str(process).split(", b'")[-1]
                #CPP
                elif file_ext[-1] == 'cpp':
                    env_path = 'C:/MinGW/bin'
                    lintgpp = 'g++'
                    print("Cloned file: %s deleted" % file)
                    print("Linting file : %s" % file)
                    cmd = '%s %s' % (lintgpp, file)
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True,
                                               stderr=subprocess.PIPE,
                                               env=dict(os.environ, PATH=env_path)).communicate(0)
                    syntax_check = str(process).split(", b'")[-1]

                #JAVA
                elif file_ext[-1] == 'java':
                    env_path = 'C:/Program Files/Java/jdk1.7.0_80/bin'
                    lintgpp = 'javac'
                    print("Cloned file: %s deleted" % file)
                    print("Linting file : %s" % file)
                    cmd = '%s %s' % (lintgpp, file)
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               env=dict(os.environ, PATH=env_path)).communicate(0)
                    #syntax_check = str(process).replace("\\n", "")[6:-1]
                    output_string = ""
                    for i in range(len(process)):
                        output_string = output_string + process[i].decode("utf_8")

                    print(output_string)


                else:
                    print("No linter found for %s extension" % file_ext[-1])
                    s = "No linter found for %s extension" % file_ext[-1]

                if(lint!=None):
                    print("Cloned file: %s deleted" % file)
                    print("Linting file : %s" % file)
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
                    print("Syntax error found: %s" % syntax_check)
                    q = "Syntax error found"
                    filelist.append(file)

                dst.close()
                os.remove("%s" % file)
                s = "%s %s" % (q, syntax_check)
                x.append(s)
                i = i + 1
            if x is None:
                comment_body = "Git Assist Prediction : No Syntax Errors Found."
            else:
                filelist = list( dict.fromkeys(filelist) )
                filelist = ', '.join(filelist)
                comment_body = "Git Assist Prediction: To Be Rejected. Syntax Errors found in the following files: %s."%filelist

            headers = {'Content-Type': 'application/json'}
            myurl = '%s' % comment_url
            post_comment_data = '{\"body\":\"%s\"}' % comment_body
            post_comment_json = json.loads(post_comment_data)
            response = requests.post(myurl, auth=("GithubPrediction", "password4gp"), headers=headers,
                                     json=post_comment_json)
            if response.status_code == 201:
                print("Successfully posted a comment")
            else:
                print("Failed to post a response with http status code : ", response.status_code)
            return "%s" % x
        else:
            print("Closed pull request")
            return "Closed pull request"

"""         model = StoreModel().loadData()
            tdf = TestData()
            tdf1 = TestData1()
            parameter_dict = tdf.fetcher(my_info)
            extension_file = tdf1.file_fetcher(my_info)
            feature_dict = parameter_dict['feature_dict']
            comment_url = parameter_dict['comment_url']
            comment_body_pred = tdf.test_feeder(feature_dict, model)
            if comment_body_pred == 1:
                comment_body = 'GIT ASSIST PREDICTION : Probability of being Accepted'
                # git_pred = object_file_predict.predict_file_criticality(payload_json)
            else:
                comment_body = 'GIT ASSIST PREDICTION : Probability of being Rejected'
            Comment.post_comment(comment_url, comment_body)
            # For Testing 
            git_pred = object_file_predict.predict_file_criticality(payload)
            app.logger.info(comment_body)
            prediction_response = json.dumps({"state": comment_body})
            app.logger.info(comment_body)
            res = Response(prediction_response, status=200, mimetype='application.json')
            return res
        prediction_response = json.dumps({"state": "closed pull request"})
        app.logger.info("closed pull request")
        res = Response(prediction_response, status=200, mimetype='application.json')
        return res"""


@app.route('/api/connection/', methods=['GET', 'POST', 'HEAD'])
def api_getconnection():
    """api for creating connection"""
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        search_keyword = request.form['search_keyword']
        response = requests.get('https://api.github.com', auth=(user_id, password))
        status = response.headers['Status']
        if status == '401 Unauthorized' or status == 'Forbidden':
            app.logger.info('failed to log in.... Please try again')
            msg = json.dumps({"status": 401, "authorization": "False"})
            res = Response(msg, status=201, mimetype='application.json')
            return res
        else:
            owner_repositories = Search.search(search_keyword)
            owner_repositories_dict = {}
            owner_repositories_dict = owner_repositories
            connection_response = json.dumps({"status": 200, "authorization": "True",
                                              "owner_repositories_list": owner_repositories_dict})
            app.logger.info('logged in successfully')
            res = Response(connection_response, status=201, mimetype='application.json')
            return res


@app.route('/api/pulls_extract/', methods=['POST', 'GET'])
def result():
    """api for pull level features"""
    if request.method == 'POST':
        search_keyword = request.form['search_keyword']
        FETCH_OBJ = Fetch()
        owner_repositories = Search.search(search_keyword)
        for i in owner_repositories:
            owner_name = i["owner_name"]
            repository_name = i["repository_name"]
            FETCH_OBJ.json_to_csv_conversion(owner_name, repository_name)
        msg = json.dumps({"status": 200, "state": "pulls level Csv is being Constructed"})
        res = Response(msg, status=201, mimetype='application/json')
        return res


@app.route('/api/files_extract/', methods=['POST', 'GET'])
def fileresult():
    """api for file level features"""
    if request.method == 'POST':
        search_keyword = request.form['search_keyword']
        FETCH_OBJ = Fetch_file()
        owner_repositories = Search.search(search_keyword)
        for i in owner_repositories:
            owner_name = i["owner_name"]
            repository_name = i["repository_name"]
            FETCH_OBJ.json_to_csv(owner_name, repository_name)
        msg = json.dumps({"status": 200, "state": "files level Csv is being Constructed"})
        res = Response(msg, status=201, mimetype='application/json')
        return res
