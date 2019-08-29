'''Test for Pulls class inside repository package'''
import datetime
import unittest
import mock
from freezegun import freeze_time
from pulls.pulls import Pulls
class PullsTest(unittest.TestCase):
    '''Test for Repository class inside repository package'''
    pulls_url = 'https://api.github.com/repos/d3/d3/pulls/3301'
    created_at = "2018-08-12T05:31:14Z"
    state = "open"
    class MockRes:
        """ class for pulls_class unit test """
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """Converts response into json"""
            return self.json_data

    @mock.patch("unit_test.pulls_test.PullsTest.MockRes", autospec=True)
    @mock.patch('pulls.pulls.requests.get')
    def test_created_time(self, mock_get, mock_response):
        '''Test for pulls class inside pulls package'''
        pulls_list = {"number":79, "created_at":"2018-08-12T05:31:14Z", "state":"open"}
        mock_res = PullsTest.MockRes(pulls_list, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        freezer = freeze_time("2018-08-13 14:44:10")
        freezer.start()
        assert datetime.datetime.now() == datetime.datetime(2018, 8, 13, 14, 44, 10)
        response_push = Pulls().created_time(PullsTest.created_at, PullsTest.state)
        freezer.stop()
        dict1 = {}
        dict1 = {'open_pr_time': 119576.0}
        self.assertDictEqual(response_push, dict1)

    @mock.patch("unit_test.pulls_test.PullsTest.MockRes", autospec=True)
    @mock.patch('pulls.pulls.requests.get')
    def test_closed_pull_request_time(self, mock_get, mock_response):
        '''Test for pulls class inside pulls package'''
        pulls_list = {"number":79, "closed_at":"2018-08-12T05:31:14Z",
                      "created_at": "2017-03-20T17:52:26Z"}

        mock_res = PullsTest.MockRes(pulls_list, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        freezer = freeze_time("2018-08-13 14:44:10")
        freezer.start()
        assert datetime.datetime.now() == datetime.datetime(2018, 8, 13, 14, 44, 10)
        response_push = Pulls().closed_pull_request_time(pulls_list['created_at'], pulls_list['closed_at'])
        freezer.stop()
        output_dict = {'open_pr_time': 44019528.0}
        self.assertDictEqual(response_push, output_dict)


    @mock.patch("unit_test.pulls_test.PullsTest.MockRes", autospec=True)
    @mock.patch('pulls.pulls.requests.get')
    def test_commits(self, mock_get, mock_response):
        '''Test for commits feature method'''
        mock_res = PullsTest.MockRes({"number":1}, 200)
        type(mock_response).return_value = mock.PropertyMock(
            return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        commits = 4
        mock_res = PullsTest.MockRes({"commits": 4}, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)

        response_push = Pulls().get_commits(commits)
        self.assertEqual(response_push, {'commits': 4})

    @mock.patch("unit_test.pulls_test.PullsTest.MockRes", autospec=True)
    @mock.patch('pulls.pulls.requests.get')
    def test_get_changed_files(self, mock_get, mock_response):
        '''Test for changed file features'''
        mock_res = PullsTest.MockRes({"number":1}, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)
        changed_files = 4
        mock_res = PullsTest.MockRes({"changed_files": 4}, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(
            return_value=type(mock_response).return_value)

        response_push = Pulls().get_changed_files(changed_files)
        self.assertEqual(response_push, {'changed_files': 4})

if __name__ == "__main__":
    unittest.main()
