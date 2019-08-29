"""
mocking requests calls
"""
import unittest
import mock
import pandas as pd
from fetching_data.fetching_data import Fetch
from utils.utils import Utils
from search.search import Search

class FetchingDataTest(unittest.TestCase):
    """
    Testcase for Repository
    """
    @mock.patch('pulls.pulls.Pulls.created_time')
    @mock.patch('pulls.pulls.Pulls.closed_pull_request_time')
    @mock.patch('repository.repository.Repository.open_pr_count')
    @mock.patch('pulls.pulls.Pulls.get_commits')
    @mock.patch('pulls.pulls.Pulls.get_changed_files')
    @mock.patch('repository.repository.Repository.get_forks_count')
    @mock.patch('repository.repository.Repository.pushed_time')
    @mock.patch('repository.repository.Repository.watchers_count')
    @mock.patch('repository.repository.Repository.get_open_issue_count')
    @mock.patch('repository.repository.Repository.get_repo_probability')
    @mock.patch('labels.label.Label.get_label')
    def test_fetching_data(self, mock_get_label, mock_get_repo_probability,mock_get_open_issue_count, mock_watchers_count, mock_pushed_time,
                           mock_get_forks_count, mock_get_changed_files,
                           mock_get_commits, mock_open_pr_count, mock_closed_pull_request_time,
                           mock_created_time):
        """test fetching_data method"""
        config = Utils().get_config_file('config.ini')
        owner = config.get('Repository', 'owner')
        repository_name = config.get('Repository', 'repository_name')

        mock_res = {'open_pr_time': 119576.0}
        type(mock_created_time).return_value = mock.PropertyMock(return_value=mock_res)
        mock_res = {'closed_pr_time': 44010646.0}
        type(mock_closed_pull_request_time).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'open_pull_request': 3}
        type(mock_open_pr_count).return_value = mock.PropertyMock(return_value=mock_res)
        mock_res = {'commits': 4}
        type(mock_get_commits).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'changed_files': 4}
        type(mock_get_changed_files).return_value = mock.PropertyMock(return_value=mock_res)


        mock_res = {"forks_count":371}
        type(mock_get_forks_count).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'pushed_time': 54987.0}
        type(mock_pushed_time).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {"watchers_count":6525}
        type(mock_watchers_count).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'state': 'Accepted'}
        type(mock_get_label).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'pull_request-acceptance_rate': 66.66666}
        type(mock_get_repo_probability).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res2 = {'open_issue_count': 556}
        type(mock_get_open_issue_count).return_value = mock.PropertyMock(return_value=mock_res2)
        input_dict = {'last_page':3, 'repository':'d3', 'number':17, 
        'repos_url':'https://api.github.com/repos/pallets/flask', 
        'pulls_url':'https://api.github.com/repos/d3/d3/pulls/3301',
        'contributor_url':'https://api.github.com/repos/d3/d3/contributors?per_page=100&page=',
        'files_url':'https://api.github.com/repos/d3/d3/pulls/3301/files'}
        response_push = Fetch().fetching_data(input_dict)
        self.assertEqual(response_push, {'repository_name': 'pallets/flask', 'pull_numbers': 17, 'open_pr_time': 119576.0, 'open_pull_request': 3, 'forks_count': 371, 'commits': 4, 'changed_files': 4, 'pushed_time': 54987.0, 'watchers_count': 6525, 'open_issue_count': 556, 'pull_request-acceptance_rate': 66.66666, 'contributor_rate': 0.024177949709864605, 'size': 36000, 'changes': 2, 'state': 'Accepted'})
    

    @mock.patch("fetching_data.fetching_data.Fetch.fetching_data")
    @mock.patch("search.search.Search.search")
    def test_json_to_csv_conversion(self, mock_search, mock_fetching_data):
        '''testing multiple_repository_to_dataframe'''
        mock_res1 = [{'owner_name': 'd3', 'repository_name': 'd3'}]
        type(mock_search).return_value = mock.PropertyMock(return_value=mock_res1)

        mock_res2 =  {'repository_name': 'd3', 'pull_numbers': 17, 'open_pr_time': 119576.0,
                                         'open_pull_request': 3,
                                         'forks_count': 371, 'commits': 4, 'changed_files': 4,
                                         'pushed_time': 54987.0, 'watchers_count': 6525,
                                         'open_issue_count': 556, 'pull_request_acceptance_rate': 66.66666,
                                         'contributor_acceptance_rate':20.5,'size':2,'changes':2, 'state': 'Accepted'}
        type(mock_fetching_data).return_value = mock.PropertyMock(return_value=mock_res2)

        mock_res3 = [{'owner_name': 'd3', 'repository_name': 'd3'}]
        type(mock_search).return_value = mock.PropertyMock(return_value=mock_res3)
        response_push = None
        config = Utils().get_config_file('config.ini')
        search_keyword = config.get('Search', 'search_keyword')
        owner_repositories = Search.search(search_keyword)
        for i in owner_repositories:
            owner_name = i["owner_name"]
            repository_name = i["repository_name"]
            response_push = Fetch().json_to_csv_conversion(owner_name, repository_name)
        self.assertListEqual(list(response_push.columns), list(mock_res2))



if __name__ == "__main__":
    unittest.main()
