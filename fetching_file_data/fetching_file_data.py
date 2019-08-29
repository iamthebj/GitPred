""" Data extraction"""
import logging
import csv
import os
import requests
import pandas as pd
from utils.utils import Utils
from fetching_data import commit_api
LOGGER = Utils().user_path()
logging.basicConfig(filename=LOGGER, level=logging.DEBUG)


class Fetch_file:
    """Class for extracting data"""
    @classmethod
    def json_to_csv(cls, owner, repository,complexity_dict):
        """for making data frame for multiple repository"""
        config = Utils().get_config_file('config.ini')
        all_state = config.get('url', 'all_state')
        parameter = config.get('url', 'pull_paginate')
        url = config.get('url', 'url')
        repos_url = url + owner + "/" + repository
        pulls_url = url + owner + "/" + repository
        last_page = Utils().pagination(owner, repository)
        config = Utils().get_config_file('config.ini')
        user = config.get('GithubCredential', 'user_id', raw=True)
        password = config.get('GithubCredential', 'password')
        list1 = []
        fieldnames = ['repository_name', 'pull_number', 'commits', 'changes',
                      'status', 'additions', 'deletions', 'filename',
                      'criticality', 'count_of_occurrence', 'commit_criticality',
                      'perc_change_files', 'cy_comp']
        filename = r'filelevelgithub.csv'
        # file = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\\' + filename
        exists = os.path.isfile(filename)
        if exists:
            filelevelgithub = open(filename, "a")
            writer = csv.DictWriter(filelevelgithub, fieldnames=fieldnames)
        else:
            filelevelgithub = open(filename, "w")
            writer = csv.DictWriter(filelevelgithub, fieldnames=fieldnames)
            writer.writeheader()

        for page_number in range(int(last_page)):
            pulls_url = repos_url + all_state + parameter + str(page_number+1)
            res = requests.get(pulls_url, auth=(user, password)).json()
            for i in res:
                number = i['number']
                pulls_url = repos_url + '/pulls/' + str(number)
                pulls_files_url = repos_url + '/pulls/' + str(number) + '/files'
                res1 = requests.get(pulls_files_url, auth=(user, password)).json()
                for j in res1:
                    feature_dict = {}
                    res2 = requests.get(pulls_url, auth=(user, password)).json()
                    repository_name = repository
                    pull_numbers = res2["number"]
                    commits = res2["commits"]
                    changes = j['changes']
                    status = j['status']
                    additions = j['additions']
                    deletions = j['deletions']
                    filename = j['filename']
                    feature_dict['repository_name'] = repository_name
                    feature_dict['pull_number'] = pull_numbers
                    feature_dict['commits'] = commits
                    feature_dict['changes'] = changes
                    feature_dict['status'] = status
                    feature_dict['additions'] = additions
                    feature_dict['deletions'] = deletions
                    feature_dict['filename'] = filename
                    filename = filename.split('/')
                    file_list = filename[-1]
                    file_list1 = file_list.split('.')
                    extension = file_list1[-1]
                    programming_extension = config.get("extension_list", "programming_extension").split(',')
                    config_extension = config.get("extension_list", "config_extension").split(',')
                    text_file = config.get("extension_list", "text_file").split(',')
                    programming_extension = list(map(lambda s: s.strip(), programming_extension))
                    config_extension = list(map(lambda s: s.strip(), config_extension))
                    text_file = list(map(lambda s: s.strip(), text_file))
                    if extension in programming_extension:
                        feature_dict["criticality"] = 'high'
                    elif extension in config_extension:
                        feature_dict["criticality"] = 'medium'
                    elif extension in text_file:
                        feature_dict["criticality"] = 'low'
                    else:
                        feature_dict["criticality"] = 'none'
                    res = requests.get(pulls_url, auth=(user, password))
                    res = res.json()
                    if res['state'] == 'closed' and not res['merged_at']:
                        filename1 = j["filename"]
                        list1.append(filename1)
                        if filename1 in list1:
                            feature_dict["count_of_occurrence"] = list1.count(filename1)
                        else:
                            list1.append(filename1)
                            feature_dict["count_of_occurrence"] = list1.count(filename1)
                    else:
                        filename1 = j["filename"]
                        if filename1 in list1:
                            feature_dict["count_of_occurrence"] = list1.count(filename1)
                        else:
                            feature_dict["count_of_occurrence"] = 0
                            items = complexity_dict.keys()
                            for item_file in items:
                                if item_file == filename1:
                                    data = complexity_dict[filename1]
                                    feature_dict['commit_criticality'] = data[0]
                                    feature_dict['perc_change_files'] = data[1]
                                    feature_dict['cy_comp'] = data[2].split(':')[1]
                                    break
                                else:
                                    feature_dict['commit_criticality'] = 'Non-critical'
                                    feature_dict['perc_change_files'] = 0
                                    feature_dict['cy_comp'] = 0
                            print(feature_dict)
                            writer.writerow(feature_dict)
        filelevelgithub.close()
        filename = r'filelevelgithub.csv'
        csv_dataframe = pd.read_csv(filename)
        logging.debug("Data Frame:{} ".format(csv_dataframe))
        return csv_dataframe


if __name__ == "__main__":
    fetchfileobj = Fetch_file()
    fetchfileobj.json_to_csv('rishab2611', 'project1')
