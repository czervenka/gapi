from unittest import TestCase
from mock import patch
import mock

SERVICE_KEY = 'test_generated_key.pem'
SERVICE_EMAIL = 'service_account@example.com'
USER_EMAIL = 'user@example.com'
USER2_EMAIL = 'user2@example.com'


class DictObject(object):

    def __init__(self, **properties):
        self.__dict__.update(properties)


def get_gae_mock_fetch():
    fetch = mock.MagicMock()
    fetch.__call__ = mock.MagicMock()
    return fetch


def get_gae_mock_memcache():
    memcache = mock.MagicMock()
    memcache.get, memcache.set = mock.MagicMock(), mock.MagicMock()
    memcache.get.return_value = None
    return memcache


class TestToken(TestCase):

    @patch('google.appengine.api.urlfetch.fetch', get_gae_mock_fetch())
    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_gets_token(self):
        from gapi import oauth2, exceptions
        from google.appengine.api.urlfetch import fetch
        from google.appengine.api import memcache
        token = oauth2.TokenRequest(SERVICE_EMAIL, SERVICE_KEY, 'https://www.googleapis.com/auth/calendar', USER_EMAIL)
        self.assertFalse(fetch.called, msg="Token fetched before needed (lazy evaluation failed).")

        fetch.return_value = DictObject(**{
            'status_code': 200,
            'content': '{"access_token" : "1/8xbJqaOZXSUZbHLl5EOtu1pxz3fmmetKx9W8CV4t79M", "token_type" : "Bearer", "expires_in" : 3250 }'
        })
        fetch.return_value.headers = {}
        header = str(token)
        self.assertEquals(header, 'Bearer 1/8xbJqaOZXSUZbHLl5EOtu1pxz3fmmetKx9W8CV4t79M', msg="The token string representation does not conform values from auth server")
        self.assertEquals(memcache.get.call_count, 1, msg="Token tries to retrieve the key from memcahced first.")
        self.assertEquals(memcache.set.call_args[0][2], 3250, msg="The memcache expiration equals expiration of the token got from auth server.")

        fetch.return_value.status_code = 403
        fetch.return_value.content = '{"error": "invalid_grant"}'
        token = oauth2.TokenRequest(SERVICE_EMAIL, SERVICE_KEY, 'https://www.googleapis.com/auth/calendar', USER_EMAIL)
        self.assertRaises(exceptions.InvalidGrantException, token.get_token)
