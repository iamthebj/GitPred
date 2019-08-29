'''for utilities purposes'''
import datetime
import os
import configparser
import requests
import pandas as pd
class Utils:
    """class for utility functions"""
    @staticmethod
    def cal_time(created_date):
        '''calculating the difference between the time pull request created and the time till now'''
        tday = datetime.datetime.now()
        till_time = tday - created_date
        return till_time.total_seconds()
    @staticmethod
    def get_config_file(file_name):
        """function for configuration file"""
        config = configparser.ConfigParser()
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), r'..', 'config'))
        config_path = path + "\\" + file_name
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def pagination(self, owner, repository_name):
        '''Pagination function '''
        config = Utils().get_config_file('config.ini')
        url = config.get('url', 'url')
        user_id = config.get('GithubCredential', 'user_id', raw=True)
        password = config.get('GithubCredential', 'password')
        all_state = config.get('url', 'all_state')
        url = config.get('url', 'url')
        parameter = config.get('url', 'pull_paginate')
        url = url + owner + "/" + repository_name + all_state + parameter
        res = requests.get(url, auth=(user_id, password))
        url = None
        last_page = 1
        key_list = list(res.links)
        if 'last' in key_list:
            url = res.links['last']['url']
            page_list = url.split('&page=')
            last_page = page_list[1]
        return last_page

    def remove_duplicate(self, file_name):
        '''removes duplicate row from the csv file'''
        new_data_frame = pd.read_csv(file_name)
        new_data_frame = new_data_frame.drop_duplicates(subset=['repository_name', 'pull_numbers'],
                                                        keep='last')
        new_data_frame.to_csv(file_name, index=False)


    def user_path(self):
        '''pathn for log file'''
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), r'..'))
        user_config = Utils().get_config_file('user_config.ini')
        logger_path = user_config.get('logger', 'logger_path')
        logger_file = user_config.get('logger', 'logger_file')
        logger = path + logger_path
        if not os.path.exists(logger):
            os.mkdir(logger)
        logger = logger + '' + logger_file
        return logger
