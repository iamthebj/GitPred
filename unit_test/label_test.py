'''unit testing for label'''
import unittest
import mock
from labels.label import Label
class LabelTest(unittest.TestCase):
    '''test for label class'''
    label = 'https://api.github.com/repos/d3/d3/pulls/3301'
    state = 'closed'
    merged_at = r'2018-08-15T15:01:42Z'
    class MockResponse:
        '''Class for creating mock response'''
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            '''converting response to json form'''
            return self.json_data

    @mock.patch("unit_test.label_test.LabelTest.MockResponse")
    @mock.patch('requests.get')
    def test_label(self, mock_get, mock_response):
        '''Test for Repository class inside repository package'''
        mock_data_list = {'id': 208203595, 'number':64, 'state':'closed',
                          'merged_at':r'2018-08-15T15:01:42Z'}
        mock_res = LabelTest.MockResponse(mock_data_list, 200)
        type(mock_response).return_value = mock.PropertyMock(return_value=mock_res)
        type(mock_get).return_value = mock.PropertyMock(return_value=type(mock_response).return_value)
        response_label = Label().get_label(LabelTest.state, LabelTest.merged_at)
        output_dict = {'state': 'Accepted'}
        self.assertDictEqual(response_label, output_dict)

if __name__ == "__main__":
    unittest.main()
