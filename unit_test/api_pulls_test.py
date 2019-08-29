from web_git_prediction.views import api_getconnection,fileresult,result
import requests
import unittest
from unittest import mock
# This is the class we want to test
class PullsApiClass:
    url= 'http://10.44.126.19/api/pulls_extract'
    def fetch_json(self, url):
        response = requests.get(url)
        return response.json()
    def fetch_json1(self, url1):
        response = requests.get(url1)
        return response.json()
# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    if args[0] == 'http://10.44.126.19/api/pulls_extract':
        return MockResponse({"filesize":456,"status": "pull level csv generated"}, 200)
    return MockResponse(None, 404)
class PullsAPIClassTestCase(unittest.TestCase):
    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):
        mgc = PullsApiClass()
        json_data = mgc.fetch_json('http://10.44.126.19/api/pulls_extract')
        self.assertEqual(json_data,{"filesize":456,"status": "pull level csv generated"})
        self.assertIn(mock.call('http://10.44.126.19/api/pulls_extract'), mock_get.call_args_list)
        self.assertEqual(len(mock_get.call_args_list), 1)
if __name__ == '__main__':
    unittest.main()
