import requests
import json
import pandas as pd
import ast
from utils.utils import Utils
from fetching_data import commit_api
from ml_model.ml_filelevel_model import FileMLModel


class file_predict_comment:

    def __init__(self):
        config = Utils().get_config_file('config.ini')
        self.comments_url = config.get('url', 'comments_url', raw=True)
        self.git_username = config.get('GithubCredential', 'user_id', raw=True)
        self.git_password = config.get('GithubCredential', 'password')
        self.requests_commit = config.get('commit_api', 'commit_url')

    def predict_file_criticality(self, payload_json):
        branch_name = payload_json['pull_request']['head']['ref']
        branch_url = self.requests_commit + branch_name
        complexity_dict = str(commit_api.main(branch_url))
        complexity_dict = complexity_dict.replace("'", "\"")
        critical_dict = json.loads(complexity_dict)
        test_data = {}
        columns=['extension_name', 'perc_change_files', 'cy_comp']
        comment_text= ''
        for file in critical_dict.keys():
            file_param = []
            data_line=[1]
            ext = file.split('.')[-1]
            file_param.append(ext)
            percent_files = critical_dict[file][1]
            file_param.append(percent_files)
            cycom = critical_dict[file][2].split(' : ')[-1]
            file_param.append(int(cycom))
            data_line.append(tuple(file_param))
            frame_test = pd.DataFrame([file_param],columns=['extension_name', 'perc_change_files', 'cy_comp'])
            print(frame_test)
            transform_data = FileMLModel.data_transform(frame_test)
            print(transform_data)
            critical_state = str(FileMLModel.test_model(transform_data))
            critical_state = ast.literal_eval(critical_state)
            if "Not-Critical" in critical_state[0]:
                user_instruction= 'Please check the file manually'
            else:
                user_instruction= 'No need to check as the prediction declared it critical'
            comment_text = comment_text + "Prediction for " + file + " is "+ critical_state[0]  + ". " + user_instruction + "<br> "
            # test_data[file] = prediction
        pull_req_project_id = payload_json['pull_request']['number']
        post_comment = "GIT ASSIST PREDICTION : <br> %s" %comment_text
        post_comment_data = '{\"body\":\"%s\"}' % post_comment
        print(post_comment_data)
        post_comment_json = json.loads(post_comment_data)
        self.post_comment(pull_req_project_id, post_comment_json)
        return test_data
        

    def post_comment(self, pull_req_project_id, comment_data):
        headers = {'Content-Type': 'application/json'}
        myUrl = self.comments_url % pull_req_project_id
        response = requests.post(myUrl, auth=(self.git_username, self.git_password), headers=headers, json=comment_data)
        if response.status_code == 201:
            print("Successfully posted a comment")
        else:
            print("Failed to post a response with http status code : ", response.status_code)
