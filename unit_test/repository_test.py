"""
mocking requests calls
"""
import unittest
from freezegun import freeze_time
import mock
from repository.repository import Repository

class RepositoryTest(unittest.TestCase):
    """
    Testcase for Repository
    """
    repos_url = 'https://api.github.com/repos/d3/d3/pulls'
    class MockResponse:
        '''class for creating a mock response'''
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.headers = {"X-RateLimit-Reset": '1372700873'}

        def json(self):
            '''for converting response into json form'''
            return self.json_data
    @mock.patch("unit_test.repository_test.RepositoryTest.MockResponse", autospec=True)
    @mock.patch('repository.repository.requests.get')
    def test_pushed_time(self, mock_get, mock_response):
        """test pushed_time method"""
        #json_str = json.dumps({"pushed_at":"2018-07-26 22:06:19",'status_code':200})
        mock_res = RepositoryTest.MockResponse({"pushed_at":"2018-07-26 22:06:19",
                                                'status_code':200}, 200)
        pushed_at = '2018-07-26 22:06:19'
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        freezer = freeze_time("2018-07-27 13:22:46")
        freezer.start()
        response_push = Repository().pushed_time(pushed_at)
        freezer.stop()
        self.assertDictEqual(response_push, {'pushed_time': 54987.0})

    @mock.patch("unit_test.repository_test.RepositoryTest.MockResponse", autospec=True)
    @mock.patch('repository.repository.requests.get')
    def test_watchers_count(self, mock_get, mock_response):
        '''Test for Repository class inside repository package'''
        mock_res = RepositoryTest.MockResponse({"watchers_count":6525}, 200)
        watchers_count = 6525
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        response_push = Repository().watchers_count(watchers_count)
        self.assertEqual(response_push, {"watchers_count":6525})

    @mock.patch("unit_test.repository_test.RepositoryTest.MockResponse", autospec=True)
    @mock.patch('repository.repository.requests.get')
    def test_forks_count(self, mock_get, mock_response):
        '''Test for Repository class inside repository package'''
        mock_res = RepositoryTest.MockResponse([{"base":{"repo":{"forks_count":371}}}], 200)
        forks_count = 371
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        response_push = Repository().get_forks_count(forks_count)
        self.assertEqual(response_push, {"forks_count":371})

    @mock.patch("unit_test.repository_test.RepositoryTest.MockResponse", autospec=True)
    @mock.patch('repository.repository.requests.get')
    def test_open_pr_count(self, mock_get, mock_response):
        '''Test for pulls class inside pulls package'''
        pulls_list = [{"number":79}, {"number":51}, {"number":17}]
        mock_res = RepositoryTest.MockResponse(pulls_list, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        last = 1
        response_push = Repository().open_pr_count(RepositoryTest.repos_url, last)
        output_dict = {'open_pull_request': 3}
        self.assertDictEqual(response_push, output_dict)

    @mock.patch("unit_test.repository_test.RepositoryTest.MockResponse", autospec=True)
    @mock.patch('repository.repository.requests.get')
    def test_get_open_issue_count(self, mock_get, mock_response):
        '''Test for Repository class inside repository package'''
        mock_res = RepositoryTest.MockResponse({'open_issues_count':556}, 200)
        open_issues_count = 556
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        response_push = Repository().get_open_issue_count(open_issues_count)
        self.assertEqual(response_push, {'open_issue_count': 556})

    @mock.patch("unit_test.repository_test.RepositoryTest.MockResponse", autospec=True)
    @mock.patch('repository.repository.requests.get')
    def test_get_repo_probability(self, mock_get, mock_response):
        '''Test for Repository class inside repository package'''
        mock_reponses = []
        mock_res = RepositoryTest.MockResponse([{'state':'closed',
                                                 "merged_at":'2018-08-29T20:05:38Z'}], 200)
        type(mock_response).return_value = mock.PropertyMock(
            return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)

        mock_res = RepositoryTest.MockResponse([{'state':'closed', "merged_at":None}], 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)
        mock_get.side_effect = mock_reponses
        mock_res = RepositoryTest.MockResponse([{'state':'closed',
                                                 "merged_at":'2018-08-29T20:05:38Z'}], 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)
        mock_get.side_effect = mock_reponses
        response_push = Repository().get_repo_probability('3', RepositoryTest.repos_url)
        self.assertEqual(response_push, {'pull_request_acceptance_rate': 66.66666666666666})
if __name__ == "__main__":
    unittest.main()
