"""
mocking requests calls
"""
import unittest
import mock
import pandas as pd
from fetching_file_data.fetching_file_data import Fetch_file
from utils.utils import Utils
from search.search import Search

class FetchingfileDataTest(unittest.TestCase):
    """
    Testcase for file
    """
    owner = 'd3'
    repository = 'd3'
    @mock.patch('requests.get')
    @mock.patch('utils.utils')

    class MockRes:
        """ class for pulls_class unit test """
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """Converts response into json"""
            return self.json_data
    
    #@mock.patch('utils.utils.requests.get.json')
    @mock.patch("unit_test.pulls_test.PullsTest.MockRes", autospec=True)
    @mock.patch('fetching_file_data.fetching_file_data.requests.get')
    @mock.patch('utils.utils.Utils.pagination')
    def test_file(self,mock_pagination, mock_get, mock_response):
        mock_reponses = []
        mock_res1 = [{'number': 12,  'pull_numbers':2,'commits': 4,'changes':2,'status':'modified',"additions":19,'deletions':0,'filename':"shadowsocks-csharp/Controller/Logging.cs" }]
        mock_res = FetchingfileDataTest.MockRes(mock_res1, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)

        mock_res1 = [{'number': 12,  'pull_numbers':2,'commits': 4,'changes':2,'status':'modified',"additions":19,'deletions':0,'filename':"shadowsocks-csharp/Controller/Logging.cs" }]
        mock_res = FetchingfileDataTest.MockRes(mock_res1, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)
        mock_get.side_effect = mock_reponses


        mock_res1 = {'number': 12,  'pull_numbers':2,'commits': 4,'changes':2,'status':'modified',"additions":19,'deletions':0,'filename':"shadowsocks-csharp/Controller/Logging.cs" }
        mock_res = FetchingfileDataTest.MockRes(mock_res1, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)
        mock_get.side_effect = mock_reponses

        mock_res1 = {'number': 12,'state':'closed','merged_at':' null', 'pull_numbers':2,'commits': 4,'changes':2,'status':'modified',"additions":19,'deletions':0,'filename':"shadowsocks-csharp/Controller/Logging.cs" }
        mock_res = FetchingfileDataTest.MockRes(mock_res1, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(return_value=type(mock_response).return_value)
        mock_reponses.append(type(mock_get).return_value)
        mock_get.side_effect = mock_reponses
        
        mock_res = 1
        type(mock_pagination).return_value = mock.PropertyMock(return_value=mock_res)

        mock_res2 =['repository_name', 'pull_numbers', 'commits', ' changes', 'status',
                    'additions', 'deletions', 'filename', 'criticality',
                    'count_of_occurrence']
        

        response = Fetch_file().json_to_csv(FetchingfileDataTest.owner, FetchingfileDataTest.repository)
        #print(response.columns)
        self.assertListEqual(list(response.columns), list(mock_res2))
        
if __name__ == "__main__":
    unittest.main()