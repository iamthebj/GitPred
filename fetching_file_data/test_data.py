import requests
import json
import logging
from ml_model.ml_file_model import FileMLModel
from utils.utils import Utils
class TestData1(object):
    def __init__(self):
        pass
    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    date_format = config.get('Format', 'date_format', raw=True)
    contributor_parameter = config.get('url', 'contributor_paginate')
    def file_fetcher(self, response):
        response = json.loads(response)
        pulls_url =  response['pull_request']['url']
        file_url = pulls_url + r'/files'
        res1 = requests.get(file_url, auth=(TestData1().user_id, TestData1().password)).json()
        extension_list = []
        files = []
        for j in res1:
            filename = j['filename']
            files.append(filename)
            filename = filename.split('/')
            file_list = []
            file_list1 = []
            file_list = filename[-1]
            file_list1 = file_list.split('.')
            extension = file_list1[-1]
            extension_list.append(extension)
        #print("lllllll",extension_list)
        return (extension_list,files)

    def file_test_feeder(self, extension, file_name):
        model = FileMLModel()
        data_frame = model.model_init()
        t = model.data_split(data_frame)
        model.train_model(t[0], t[2])
        y_pred = model.test_model(extension)
        #y_pred = FileMLModel().test_model(extension)
        dict_file ={}
        state = "probability of being "
        for i in range(len(extension)):
            dict_file[file_name[i]] = state + y_pred[i]
        print(dict_file)
        return dict_file
