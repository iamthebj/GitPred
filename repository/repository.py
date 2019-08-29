'''Fetching Repository level data from github repositories'''
import datetime
import logging
import requests
from utils.utils import Utils
import traceback
import pause
logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)
class Repository(object):
    '''Fetching Pull Request related data from github repositories'''
    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    date_format = config.get('Format', 'date_format', raw=True)
    url = config.get('url', 'url')
    parameter = config.get('url', 'pull_paginate')
    open_state = config.get('url', 'open_state')
    all_state = config.get('url', 'all_state')
    msg = "'message': 'API rate limit exceeded"
    def __init__(self):
        pass
    @classmethod
    def pushed_time(cls, pushed_at):
        '''Getting the push time at repository'''
        pushed_at = pushed_at.strip('Z')
        pushed_at = pushed_at.replace('T', ' ')
        pushed_at = datetime.datetime.strptime(pushed_at, Repository.date_format)
        pushed_time = Utils().cal_time(pushed_at)
        pushed_dict = {}
        pushed_dict['pushed_time'] = pushed_time
        logging.debug("Pushed time :{} ".format(pushed_dict))
        return pushed_dict

    @classmethod
    def open_pr_count(cls, url, last_page):
        '''Getting the number of open pull request'''
        sum1 = 0
        open_pr_dict = {}
        for page in iter(range(1, int(last_page)+1)):
            pulls_url = url + Repository.open_state + Repository.parameter + str(page)
            repository = requests.get(pulls_url, auth=(Repository.user_id, Repository.password))
            open_pr_dict = {}
            repository = repository.json()
            sum1 = sum1 + len(repository)
        open_pr_dict['open_pull_request'] = sum1
        logging.debug("open pull request count :{} ".format(open_pr_dict))
        return open_pr_dict

    @classmethod
    def watchers_count(cls, watchers_count):
        '''making a method watchers_count and retrieving the data in json '''
        watchers_count_dict = {}
        watchers_count_dict['watchers_count'] = watchers_count
        logging.debug("Watchers count :{} ".format(watchers_count_dict))
        return watchers_count_dict

    @classmethod
    def get_forks_count(cls, forks_count):
        '''Getting the number of forks count'''
        forks_count_dict = {}
        forks_count_dict['forks_count'] = forks_count
        logging.debug("Forks count :{} ".format(forks_count_dict))
        return forks_count_dict

    @classmethod
    def get_open_issue_count(cls, open_issue_count):
        '''Getting the number of issue count'''
        issue_count_dict = {}
        issue_count_dict['open_issue_count'] = open_issue_count
        logging.debug("Issue count :{} ".format(issue_count_dict))
        return issue_count_dict

    @classmethod
    def get_repo_probability(cls, last_page, repos_url):
        '''Getting the pull request acceptance rate of repository'''
        acceptance_rate_dict = {}
        count = 0
        total_count = 0
        for j in range(int(last_page)):
            url = repos_url + Repository.all_state + Repository.parameter + str(j+1)
            repository = requests.get(url, auth=(Repository.user_id, Repository.password))
            reset = int(repository.headers['X-RateLimit-Reset'])
            reset_datetime = datetime.datetime.fromtimestamp(reset)
            reset_datetime = reset_datetime + datetime.timedelta(0,70)
            response = repository.json()
            if not str(response).__contains__(Repository.msg):
                for i in response:
                    if(i['state'] == 'closed' and i['merged_at']):
                        count = count + 1
                    if i['state'] == 'closed':
                        total_count = total_count + 1
            else:
                print('in sleep till :',reset_datetime)
                pause.until(reset_datetime)
        if total_count == 0:
            acceptance_rate_dict["pull_request-acceptance_rate"] = 0
        else:
            rate = (count / total_count) * 100
            acceptance_rate_dict["pull_request_acceptance_rate"] = rate
        logging.debug("pull request acceptance rate :{} ".format(acceptance_rate_dict))
        return(acceptance_rate_dict)

    @classmethod
    def total_contribution(cls, last_page, contribution_url):
        '''method for finding total number of contribution'''
        total = 0
        contributors_dict = {}
        total_contributor = {}
        for page_number in range(1, int(last_page)+1):
            contribution_link = contribution_url
            contribution_link = contribution_link + str(page_number)
            contri_response = requests.get(contribution_link, auth=(Repository.user_id, Repository.password))
            reset = int(contri_response.headers['X-RateLimit-Reset'])
            reset_datetime = datetime.datetime.fromtimestamp(reset)
            reset_datetime = reset_datetime + datetime.timedelta(0,70)
            contri_response = contri_response.json()
            if not str(contri_response).__contains__(Repository.msg):
                for i in contri_response:
                    contributors_dict[i["login"]] = i["contributions"]
                    total = total + i["contributions"]
            else:
                print('in sleep till :',reset_datetime)
                pause.until(reset_datetime)
        total_contributor['total'] = total
        total_contributor['contributors'] = contributors_dict
        logging.debug("total contribution :{} ".format(total_contributor))
        return total_contributor
