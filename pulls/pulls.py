'''Getting the open pull time of pull request in seconds'''
import datetime
import logging
import requests
from utils.utils import Utils
import pause
logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)
class Pulls(object):
    """creating class for open pull time"""
    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    date_format = config.get('Format', 'date_format', raw=True)
    url = config.get('url', 'url')
    all_state = config.get('url', 'all_state')
    open_state = config.get('url', 'open_state')
    closed_state = config.get('url', 'closed_state')
    parameter = config.get('url', 'pull_paginate')
    logging.basicConfig(filename='test.log', level=logging.DEBUG)
    msg = "'message': 'API rate limit exceeded"
    def __init__(self):
        pass
    @classmethod
    def created_time(cls, created_at, state):
        '''Getting the created time of open pull request'''
        pull_no_dict = {}
        open_time = 0
        if state == 'open':
            created_at = created_at.strip('Z')
            created_at = created_at.replace('T', ' ')
            created_at = datetime.datetime.strptime(created_at, Pulls.date_format)
            utils_obj = Utils()
            open_time = utils_obj.cal_time(created_date=created_at)
            pull_no_dict['open_pr_time'] = open_time
        else:
            pull_no_dict['open_pr_time'] = None
        logging.debug("open pull request time :{} ".format(pull_no_dict))
        return pull_no_dict


    @classmethod
    def closed_pull_request_time(cls, created_at, closed_at):
        '''Getting the created time of open pull request'''
        closed_pull_time_dict = {}
        closed_time = 0
        if closed_at is not None:
            created_at = created_at.strip('Z')
            created_at = created_at.replace('T', ' ')
            closed_at = closed_at.strip('Z')
            closed_at = closed_at.replace('T', ' ')
            created_at = datetime.datetime.strptime(created_at, Pulls.date_format)
            closed_at = datetime.datetime.strptime(closed_at, Pulls.date_format)
            closed_time = closed_at - created_at
            closed_time = closed_time.total_seconds()
            closed_pull_time_dict['open_pr_time'] = closed_time
        else:
            closed_pull_time_dict['open_pr_time'] = None
        logging.debug("closed pull request time :{} ".format(closed_pull_time_dict))
        return closed_pull_time_dict

    @classmethod
    def get_commits(cls, commit):
        '''fetching commits for a pull request'''
        commit_dict = {}
        commit_dict['commits'] = commit
        logging.debug("Number of commits :{} ".format(commit_dict))
        return commit_dict

    @classmethod
    def get_changed_files(cls, changed_file):
        '''method for getting changed files'''
        changed_file_dict = {}
        changed_file_dict['changed_files'] = changed_file
        logging.debug("Number of changed file :{} ".format(changed_file_dict))
        return changed_file_dict


    def contributor_probability_rate(self, user, parameter_dict):
        '''method for getting contributor acceptance rate'''
        total = parameter_dict["total"]
        contri_prob_dict = {}
        contribution = 0
        rate = 0
        for j in parameter_dict["contributors"]:
            if user == j:
                contribution = parameter_dict["contributors"][j]
                rate = (contribution/total)*100
        contri_prob_dict['contributor_rate'] = rate
        logging.debug("contributor pull acceptance rate :{} ".format(contri_prob_dict))
        return contri_prob_dict

    @classmethod
    def pull_request_size(cls, response):
        '''method for getting size of pull request'''
        size = 0
        size_dict = {}
        if response['head']['repo']:
            size = response['head']['repo']["size"]
        else:
            size = 0
        size_dict['size'] = size
        logging.debug("size of pull request:{} ".format(size_dict))
        return size_dict


    @classmethod
    def test_total_contribution(cls, last_page, contributor_url, user):
        '''getting total contributions in a repository'''
        total = 0
        contribution = 0
        rate_dict = {}
        for page_number in range(int(last_page)):
            contributor_url = contributor_url + str(page_number+1)
            contri_response = requests.get(contributor_url, auth=(Pulls.user_id, Pulls.password)).json()
            for i in contri_response:
                total = total + i["contributions"]
                if user == i["login"]:
                    contribution = i['contributions']
        rate = (contribution/total)*100
        rate_dict['contributor_rate'] = rate
        logging.debug("test contributor pull acceptance rate :{} ".format(rate_dict))
        return rate_dict

    @classmethod
    def changed_lines_in_file(cls, files_url):
        '''getting changed files in a pull requests'''
        total_changes = 0
        changed_lines_in_file_dict = {}
        files_response = requests.get(files_url, auth=(Pulls.user_id, Pulls.password))
        reset = int(files_response.headers['X-RateLimit-Reset'])
        reset_datetime = datetime.datetime.fromtimestamp(reset)
        reset_datetime = reset_datetime + datetime.timedelta(0,70)
        files_response = files_response.json()
        if not str(files_response).__contains__(Pulls.msg):
            for i in files_response:
                total_changes = total_changes + i['changes']
            changed_lines_in_file_dict['changes'] = total_changes
        else:
            print('in sleep till :',reset_datetime)
            pause.until(reset_datetime)
        #print(changed_lines_in_file_dict)
        return changed_lines_in_file_dict
