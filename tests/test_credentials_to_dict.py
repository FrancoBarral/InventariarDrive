import unittest
from unittest.mock import Mock
from utils.credentials_to_dict.credentials_to_dict import credentials_to_dict

class TestCredentialsToDict(unittest.TestCase):
    def test_credentials_to_dict_with_valid_credentials(self):
        mock_credentials = Mock()
        mock_credentials.token = 'test_token'
        mock_credentials.refresh_token = 'test_refresh_token'
        mock_credentials.token_uri = 'https://test_token_uri'
        mock_credentials.client_id = 'test_client_id'
        mock_credentials.client_secret = 'test_client_secret'
        mock_credentials.scopes = ['test_scope1', 'test_scope2']

        result = credentials_to_dict(mock_credentials)

        expected_result = {
            'token': 'test_token',
            'refresh_token': 'test_refresh_token',
            'token_uri': 'https://test_token_uri',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'scopes': ['test_scope1', 'test_scope2']
        }

        self.assertEqual(result, expected_result)

