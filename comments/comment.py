'''Fetching Repository level data from github repositories'''
import logging
import json
import requests
from utils.utils import Utils
Logger = Utils().user_path()
logging.basicConfig(filename=Logger, level=logging.DEBUG)
class Comment(object):
    '''Fetching Pull Request related data from github repositories'''
    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    def __init__(self):
        pass
    @classmethod
    def post_comment(cls, comment_url, comment_body):
        '''giving comment in repositiory regarding the prediction'''
        comment_body = json.dumps({"body": comment_body})
        response = requests.post(comment_url, auth=(Comment.user_id, Comment.password),
                                 data=comment_body).json()
        return response
