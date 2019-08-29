import requests
import json
import pprint
import numpy as np
import pandas as pd
from utils.utils import Utils
from pulls .pulls import Pulls
import datetime
from repository.repository import Repository
from ml_model.ml_model import MLModel
import logging
logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)
class TestData(object):
    def __init__(self):
        pass
    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    date_format = config.get('Format', 'date_format', raw=True)
    contributor_parameter = config.get('url', 'contributor_paginate')
    def fetcher(self, response):
        feature_dict = {}
        response = json.loads(response)
        comment_url = response['pull_request']['comments_url']
        repository = Repository()
        pulls = Pulls()
        repos_url = response['pull_request']['head']['repo']['url']
        pulls_url = response['pull_request']['url']
        files_url = pulls_url + '/files'
        #user = response["pull_request"]["user"]["login"]
        #contributor_url =repos_url + TestData.contributor_parameter
        repo_name = response['pull_request']['head']['repo']['name']
        owner_name = response['pull_request']['head']['repo']['owner']['login']
        last_page = Utils().pagination(owner_name, repo_name)
        feature_dict.update(Repository().open_pr_count(repos_url, last_page))
        #print(pulls.changed_lines_in_file(files_url))
        feature_dict['forks_count'] = response['pull_request']['head']['repo']['forks_count']
        feature_dict['commits'] = response['pull_request']['commits']
        feature_dict['changed_files'] = response['pull_request']['changed_files']
        feature_dict.update(repository.pushed_time(response['pull_request']['head']['repo']['pushed_at']))
        feature_dict['watchers_count'] = response['pull_request']['head']['repo']['watchers_count']
        feature_dict['open_issue_count'] = response['pull_request']['head']['repo']['open_issues_count']
        feature_dict.update(Pulls().pull_request_size(response["pull_request"]))
        parameter_dict = {}
        parameter_dict['feature_dict'] = feature_dict
        parameter_dict['comment_url'] = comment_url
        return parameter_dict
    
    def test_feeder(self, feature_dict, model):
        #model = MLModel()
        state = None
        column_name = []
        print(feature_dict)
        for i in feature_dict:
            column_name.append(i)
        data_frame = pd.DataFrame(columns=column_name,index=[1])
        for i in feature_dict:
            data_frame.loc[1,i] = feature_dict[i]
        test_data = data_frame.values
        y_pred = model.test_model(test_data)
        if y_pred == [0]:
            state = "probability of being Accepted"
        else:
            state = "probability of being Rejected"
        logging.debug(state)
        print(state)
        return state
        