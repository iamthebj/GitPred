"""
mocking requests calls
"""
import unittest
import mock
from fetching_data.test_data import TestData
from  ml_model.ml_model import MLModel

class TestDataTest(unittest.TestCase):
    """
    Testcase for Repository
    """
    class MockResponse:
        '''mocking the response '''
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            ''' initializing json data'''
            return self.json_data

    @mock.patch('repository.repository.Repository.watchers_count')
    @mock.patch('repository.repository.Repository.pushed_time')
    @mock.patch('repository.repository.Repository.get_forks_count')
    @mock.patch('repository.repository.Repository.open_pr_count')
    @mock.patch('repository.repository.Repository.get_repo_probability')
    @mock.patch('pulls.pulls.Pulls.test_total_contribution')
    @mock.patch('pulls.pulls.Pulls.pull_request_size')
    def test_fetcher(self, mock_open_pr_count, mock_get_forks_count,
                     mock_pushed_time, mock_watchers_count, mock_get_repo_probability,
                     mock_test_total_contribution, mock_pull_request_size):
        """test pushed_time method"""

        mock_res1 = '{"number": 1,"pull_request":{"url": "https://api.github.com/repos/sjain3097/new/pulls/1","user":{"login":"choukseyabhishek"}, "created_at":"2018-04-26 22:06:19Z","changed_files":3,"comments_url":"https://api.github.com/repos/sjain3097/new/pulls/2/commits"  , "commits":3, "head":{"repo":{"name":"sj", "url":"https://api.github.com/repos/pallets/flask", "open_issues_count":1, "watchers_count":6525, "forks_count":371, "pushed_at":54987.0, "owner":{"login":"choukseyabhishek"}}}}}'
        #type(mock_fetcher).return_value = mock.PropertyMock(return_value=mock_res)
        mock_res = {'open_pull_request': 3}
        type(mock_open_pr_count).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {"forks_count":371}
        type(mock_get_forks_count).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'pushed_time': 54987.0}
        type(mock_pushed_time).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {"watchers_count":6525}
        type(mock_watchers_count).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'pull_request_acceptance_rate': 64.77272727272727}
        type(mock_get_repo_probability).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'contributor_acceptance_rate': 0.024319066147859923}
        type(mock_test_total_contribution).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res = {'size': 35827}
        type(mock_pull_request_size).return_value = mock.PropertyMock(return_value=mock_res)

        output = {'feature_dict': {'watchers_count': 6525, 'forks_count': 371, 'commits': 3, 'changed_files': 3, 'contributor_acceptance_rate': 0.024319066147859923, 'open_issue_count': 1, 'open_pull_request': 3}, 'comment_url': 'https://api.github.com/repos/sjain3097/new/pulls/2/commits'}
        
        response_push = TestData().fetcher(mock_res1)
        self.assertDictEqual(response_push, output)
    
    @mock.patch('fetching_data.test_data.TestData.fetcher')
    def test_test_feeder(self, mock_fetcher):
        '''test for pushed time'''
        model = MLModel()
        data_frame = model.model_init()
        test = model.data_split(data_frame)
        model.train_model(model.classifier, test[0], test[2])
        #accepted
        mock_res = {'open_pull_request': 72, 'forks_count': 1, 'commits': 6, 'changed_files': 1, 'pushed_time': 21121.961954,
                     'watchers_count': 0, 'open_issue_count': 0, 'size': 52}
        ''' 
        #rejected           
        mock_res = {'open_pull_request':120, 'forks_count': 0, 'commits': 80, 'changed_files': 60, 'pushed_time': 21121.961954,
                    'watchers_count': 0, 'open_issue_count': 0, 'size': 52}
        
        mock_res = {'open_pull_request':70, 'forks_count': 0, 'commits': 1, 'changed_files': 2, 'pushed_time': 21121.961954,
                    'watchers_count': 0, 'open_issue_count': 0, 'size': 5}
        '''
        response_push = TestData().test_feeder(mock_res, model)
        self.assertEqual(response_push, 'probability of being Accepted')
if __name__ == "__main__":
    unittest.main()
