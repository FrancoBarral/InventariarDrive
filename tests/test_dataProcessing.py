import unittest
from unittest.mock import patch
from utils.dataProcessing.dataProcessing import dataProcessingFilesAll, converterData, get_visibility
from googleapiclient.discovery import build

class TestDataProcessingFunctions(unittest.TestCase):
    '''Testing the convertData validating that the function correctly delivers the function'''

    @patch('googleapiclient.discovery.build')
    def test_dataProcessingFilesAll(self, mock_build):
        mock_data = [{
            'id': 'test_file_1',
                'name': 'Test File',
                'owners': [{'emailAddress':"test@test.com"}],
                'modifiedTime': '2023-12-31',
                'mimeType': 'plain',
                'visibility': 'private'}]

        result = converterData(mock_data,mock_build)

        expected_result = [
            {
            'id': 'test_file_1',
                'name': 'Test File',
                'owner': "test@test.com",
                'modifiedTime': '2023-12-31',
                'mimeType': 'plain',
                'visibility': 'private'}
        ]

        self.assertEqual(result, expected_result)

    
