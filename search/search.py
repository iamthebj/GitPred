'''For searching multiple repositories'''
import json
import logging
import requests
from utils.utils import Utils
logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)
class Search(object):
    '''For searching multiple repositories'''
    def __init__(self):
        pass
    @classmethod
    def search(cls, search_keyword):
        """getting multiple repositories"""
        config = Utils().get_config_file('config.ini')
        user_id = config.get('GithubCredential', 'user_id')
        password = config.get('GithubCredential', 'password')
        url = config.get('url', 'search_url')
        parameter = config.get('url', 'search_paginate')
        search_url = url + search_keyword + parameter
        res = requests.get(search_url, auth=(user_id, password))
        json_data = res.json()
        repositories = []
        for i in json_data['items']:
            owner_repository = i['full_name'].split('/')
            dict1 = {'owner_name' : owner_repository[0], 'repository_name' : owner_repository[1]}
            repositories.append(dict1)
        logging.debug("repositories :{} ".format(repositories))
        return repositories
