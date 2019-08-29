'''unit testing search'''
import json
import unittest
import mock
from unittest.mock import patch
from unittest.mock import MagicMock
from search.search import Search
from utils.utils import Utils
class SearchTest(unittest.TestCase):
    '''test for search class'''
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    @mock.patch("unit_test.search_test.SearchTest.MockResponse", autospec=True)
    @mock.patch('search.search.requests.get')
    def test_search(self, mock_get, mock_response):
        '''Test for search function'''
        mock_data_list = {'items':[{'full_name':'d3/d3'},
                                   {'full_name':'Nightonke/Nightonke'},
                                   {'full_name':'vitalets/vitalets'}]}
        mock_res = SearchTest.MockResponse(mock_data_list, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(return_value=type(mock_response).return_value)
        config = Utils().get_config_file('config.ini')
        search = config.get('Search', 'search_keyword')
        
        response_search = Search().search(search)
        output_dict = [{'owner_name': 'd3', 'repository_name': 'd3'},
                 {'owner_name': 'Nightonke', 'repository_name': 'Nightonke'},
                 {'owner_name':'vitalets', 'repository_name':'vitalets'}]
        self.assertListEqual(response_search, output_dict)
    
if __name__ == "__main__":
    unittest.main()
