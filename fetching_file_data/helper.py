"""
creates a csv of files in all branches
"""
import requests
from utils.utils import Utils
import fetching_file_data
from fetching_data import commit_api
from fetching_file_data.fetching_file_data import Fetch_file

class Helper:
    """
    for returning branch list
    """

    config = Utils().get_config_file('config.ini')
    user_id = config.get('GithubCredential', 'user_id', raw=True)
    password = config.get('GithubCredential', 'password')
    requests_commit = config.get('commit_api', 'commit_url')
    branches_repo = config.get('commit_api', 'branches_repo')
    branches_repos = requests.get(branches_repo, auth=(user_id, password)).json()
    working_branches = config.get('branches', 'branch').split(',')
    owner = 'rishab2611'
    repository = 'project1'

    @staticmethod
    def branches():
        """
        :return:
        """
        branches_list = []
        url_list = []
        working_branches = []
        for branch_name in Helper.branches_repos:
            branches_list.append(branch_name['name'])
        branches_list = branches_list[1:]
        for branch in branches_list:
            if branch in Helper.working_branches or Helper.working_branches[0] == '':
                url = Helper.requests_commit + branch
                url_list.append(url)
                working_branches.append(branch)
        return url_list, working_branches
    @staticmethod
    def data_output(fetch_obj):
        critical_dict = {}

        url_list, branches_list = Helper.branches()
        for urls in range(len(url_list)):
            print("\nProcessing for branch : " + branches_list[urls] + '\n')
            complexity_dict = commit_api.main(url_list[urls])
            fetch_obj.json_to_csv(Helper.owner, Helper.repository, complexity_dict)
            critical_dict[branches_list[urls]] = complexity_dict
        critical_dict = str(critical_dict)
        return critical_dict
