'''api module'''
import os
import subprocess
import urllib

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
    if rq.headers['Content-Type'] == 'application/json':
        print("Received Pull Request")
        my_info = json.dumps(rq.json)
        payload = json.loads(my_info)
        if not payload['action'] == 'closed':
            url = payload['pull_request']['url']
            url = url + '/files'
            print("Initializing Linting Process")
            r = requests.get(url)
            a = r.json()
            print(a)
            raw = (a[0]['raw_url'])
            print(raw)
            filename = (a[0]['filename']).split("/")
            file = filename[-1]


            re = urllib.request.urlopen('%s' % raw)
            # returned_value = os.system("start \"\" %s" %raw)
            data = re.read()
            dst = open("%s" % file, "wb")
            dst.write(data)
            dst = open("%s" % file, "r")
            print ("Changed Files fecthed, %s"%file)

            file_ext = (file).split(".")
            print ("File extension of the file: %s"%file_ext[-1])
            if file_ext[-1] == 'py':
                print("Cloned file: %s deleted"%file)
                print("Linting file : %s" % file)
                cmd = 'pycodestyle %s' % file
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate(0)
                syntax_check = str(process[0])[2:-1]
                # p = str(p)
                # p = p[2:-1]
                if process == "b''" :
                    q = "No syntax error found"
                    print(q)

                else:
                    print("Syntax error found: %s" %syntax_check)
                    q = "Syntax error found"

                dst.close()
                os.remove("%s" % file)
                return "%s %s" % (q, syntax_check)

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
