""" Data extraction"""
import logging
import json
import csv
import datetime
import os
import requests
import pause
import pandas as pd
from pulls.pulls import Pulls
from labels.label import Label
from repository.repository import Repository
from utils.utils import Utils
import traceback
logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)
class Fetch:
    """Class for extracting data"""
    repo = 'new'
    dict_open_pull_request_count = None
    dict_forks_count = None
    dict_push_time = None
    dict_watchers_count = None
    dict_issue_count = None
    dict_acceptance_rate = None
    dict_contributor_rate = None
    dict_total_contribution = None
    dict_pull_request_size = None
    repository_name = None
    dict_changes_in_file = None
    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    #user_url = 'https://api.github.com/users/' + user_id
    #user_response = requests.get(user_url, auth=(user_id, password)).json()
    #print(user_response)
    #ID = user_response['id']
    #rate_limit ="{'message': 'API rate limit exceeded for user ID" + id +".', 'documentation_url': 'https://developer.github.com/v3/#rate-limiting'}"
    
    #print(rate_limit)
    file_name = config.get('file', 'csv_file_name', raw=True)
    column = ['repository_name', 'pull_numbers', 'open_pr_time',
                  'open_pull_request', 'forks_count', 'commits', 'changed_files',
                  'pushed_time', 'watchers_count', 'open_issue_count',
                  'pull_request_acceptance_rate', 'contributor_acceptance_rate', 'size', 'changes', 'state']
    msg = "'message': 'API rate limit exceeded"
    def __init__(self):
        pass
    @classmethod
    def fetching_data(cls, parameters_dict):
        """for extracting data"""
        pulls = Pulls()
        repository = Repository()
        labels = Label()
        last_page = parameters_dict['last_page']
        contributor_url = parameters_dict['contributor_url']
        if cls.repo == "new":
            repos_url = parameters_dict['repos_url']
            repos_response = requests.get(repos_url, auth=(Fetch.user_id, Fetch.password))
            reset = int(repos_response.headers['X-RateLimit-Reset'])
            reset_datetime = datetime.datetime.fromtimestamp(reset)
            reset_datetime = reset_datetime + datetime.timedelta(0,70)
            repos_response = repos_response.json()
            if not str(repos_response).__contains__(Fetch.msg):
                pushed_at = repos_response['pushed_at']
                watchers_count = repos_response['watchers_count']
                forks_count = repos_response['forks_count']
                open_issues_count = repos_response['open_issues_count']
                last_page = parameters_dict['last_page']
                cls.dict_total_contribution = Repository.total_contribution(last_page, contributor_url)
                cls.dict_open_pull_request_count = Repository.open_pr_count(repos_url, last_page)
                cls.dict_forks_count = repository.get_forks_count(forks_count)
                cls.dict_push_time = repository.pushed_time(pushed_at)
                cls.dict_watchers_count = repository.watchers_count(watchers_count)
                cls.dict_issue_count = repository.get_open_issue_count(open_issues_count)
                cls.dict_acceptance_rate = repository.get_repo_probability(last_page, repos_url)
                cls.repository_name = repos_response['full_name']
            else:
                print('in sleep till :',reset_datetime)
                print(cls.repository_name)
                pause.until(reset_datetime)
        pulls_url = parameters_dict['pulls_url']
        pulls_response = requests.get(pulls_url, auth=(Fetch.user_id, Fetch.password))
        reset = int(pulls_response.headers['X-RateLimit-Reset'])
        reset_datetime = datetime.datetime.fromtimestamp(reset)
        reset_datetime = reset_datetime + datetime.timedelta(0,70)
        pulls_response = pulls_response.json()
        feature_dict = {}
        if not str(pulls_response).__contains__(Fetch.msg):
            created_at = pulls_response['created_at']
            closed_at = pulls_response['closed_at']
            state = pulls_response['state']
            commit = pulls_response['commits']
            changed_file = pulls_response['changed_files']
            merged_at = pulls_response['merged_at']
            user = {}
            user = pulls_response["user"]["login"]
            dict_created_time = pulls.created_time(created_at, state)
            dict_closed_pull_request_time = pulls.closed_pull_request_time(created_at, closed_at)
            dict_get_commits = pulls.get_commits(commit)
            dict_changed_files = pulls.get_changed_files(changed_file)
            dict_labels = labels.get_label(state, merged_at)
            cls.dict_contributor_rate = pulls.contributor_probability_rate(user, cls.dict_total_contribution)
            cls.dict_pull_request_size = pulls.pull_request_size(pulls_response)
            files_url = parameters_dict['files_url']
            dict_changes_in_file = pulls.changed_lines_in_file(files_url)

            feature_dict = {}
            feature_dict['repository_name'] = cls.repository_name
            feature_dict['pull_numbers'] = parameters_dict['number']
            if dict_created_time['open_pr_time']:
                feature_dict.update(dict_created_time)
            else:
                feature_dict.update(dict_closed_pull_request_time)
            feature_dict.update(cls.dict_open_pull_request_count)
            feature_dict.update(cls.dict_forks_count)
            feature_dict.update(dict_get_commits)
            feature_dict.update(dict_changed_files)
            feature_dict.update(cls.dict_push_time)
            feature_dict.update(cls.dict_watchers_count)
            feature_dict.update(cls.dict_issue_count)
            feature_dict.update(cls.dict_acceptance_rate)
            feature_dict.update(cls.dict_contributor_rate)
            feature_dict.update(cls.dict_pull_request_size)
            feature_dict.update(dict_changes_in_file)
            feature_dict.update(dict_labels)
            logging.debug("Extracted features :{} ".format(feature_dict))
        else:
            print('in sleep till :',reset_datetime)
            print(cls.repository_name)
            pause.until(reset_datetime)
        return feature_dict
    @classmethod
    def json_to_csv_conversion(cls, owner, repository):
        """for making data frame for multiple repository"""
        fetch = Fetch()
        config = Utils().get_config_file('config.ini')
        csv_path = config.get('path', 'csv_path')
        csv_path = csv_path + '/' + owner
        data_frame = pd.DataFrame(columns=cls.column)
        if not os.path.isdir(os.path.join(csv_path)):
            os.makedirs(csv_path)
        if not os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', csv_path+'/'+repository+".csv"))):
            data_frame.to_csv(csv_path + '/' + repository+".csv", index=False)
        config = Utils().get_config_file('config.ini')
        all_state = config.get('url', 'all_state')
        parameter = config.get('url', 'pull_paginate')
        contributor_parameter = config.get('url', 'contributor_paginate')
        url = config.get('url', 'url')
        repos_url = url + owner + "/" + repository
        pulls_url = url + owner + "/" + repository
        contributor_url = repos_url + contributor_parameter
        #last_page = 1
        last_page = Utils().pagination(owner, repository)
        config = Utils().get_config_file('config.ini')
        user = config.get('GithubCredential', 'user_id', raw=True)
        password = config.get('GithubCredential', 'password')
        cls.repo = 'new'
        print(last_page, ' ',repository)
        for page_number in range(int(last_page)):
            pulls_url = repos_url + all_state + parameter + str(page_number+1)
            res1 = requests.get(pulls_url, auth=(user, password))
            print(res1)
            try:
                reset = int(res1.headers['X-RateLimit-Reset'])
                reset_datetime = datetime.datetime.fromtimestamp(reset)
                reset_datetime = reset_datetime + datetime.timedelta(0,70)
                res = res1.json()
                if not str(res).__contains__(Fetch.msg):
                    for i in res:
                        logging.debug("preparing csv for process: {} ".format(os.getpid()))
                        number = i['number']
                        pulls_url = repos_url + '/pulls/' + str(number)
                        files_url = pulls_url + '/files'
                        parameters_dict = {'last_page':last_page, 'repository':repository,
                                        'number':number, 'repos_url':repos_url,
                                        'pulls_url':pulls_url, 'contributor_url':contributor_url, 'files_url':files_url}
                        feature_dict = fetch.fetching_data(parameters_dict)
                        github = open(csv_path + '/' + repository+".csv", 'a', newline='')
                        csvwriter = csv.writer(github)
                        feature_dict = json.dumps(feature_dict)
                        feature_dict = json.loads(feature_dict)
                        csvwriter.writerow(feature_dict.values())
                        cls.repo = 'old'
                        logging.debug("Features dictionary:{} ".format(feature_dict))
                        github.close()
                else:
                    print('in sleep till :',reset_datetime)
                    print(owner,' ',repository)
                    pause.until(reset_datetime)
            except :
                print(res1.json())
                traceback.print_exc()
            '''
            except TypeError as e:
                print(res)
                traceback.print_exc()
            except KeyError as e:
                print(res1.headers)
                traceback.print_exc()
            '''
            '''
            except TypeError as msg:
                logging.debug("Response:{} ".format(res))
                logging.debug("Error message:{} ".format(str(msg)))
            except KeyError as msg:
                logging.debug("Response:{} ".format(res))
                logging.debug("Error message:{} ".format(str(msg)))
                print('in sleep till :',reset_datetime)
                print(owner,' ',repository)
                pause.until(reset_datetime)
        '''
        csv_dataframe = pd.read_csv(csv_path + '/' + repository+".csv")
        traceback.print_exc()
        logging.debug("Data Frame:{} ".format(csv_dataframe))
        return csv_dataframe

    @classmethod
    def csv_append(cls):
        '''function for appending all the csv's'''
        logging.debug("appending csv for process:{} ".format( os.getpid()))
        data_frame = pd.DataFrame(columns=cls.column)
        config = Utils().get_config_file('config.ini')
        csv_path = config.get('path', 'csv_path')
        for root, dirs, files in os.walk(csv_path):
            for f in files:
                csv = root+'/'+f
                repo_csv = pd.read_csv(csv)
                data_frame = pd.concat([data_frame, repo_csv], sort=False)
        logging.debug("final dataframe :{} ".format(data_frame))
        print('appending all the csv')
        print(data_frame)
        data_frame.to_csv(cls.file_name, index=False)
