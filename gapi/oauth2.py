# Copyright 2007 Robin Gottfried <copyright@kebet.cz>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = 'Robin Gottfried <google@kebet.cz>'

"""
Uses PyCrypto

OAuth 2.0 for Server to Server Applications
see https://developers.google.com/accounts/docs/OAuth2ServiceAccount
"""
from types import StringTypes
from time import time
from base64 import urlsafe_b64encode
from json import dumps, loads
from google.appengine.api import memcache
from google.appengine.api.urlfetch import fetch
import logging

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from .gapi_utils import SavedCall
from .exceptions import InvalidGrantException

JWT_HEADER = {
    "alg": "RS256",
    "typ": "JWT",
}


class TokenRequest(object):

    def __init__(self, service_email, key, scope, impersonate_as=None, life_time=3600, validate_certificate=True):
        self.service_email = service_email
        self.key = key
        if isinstance(scope, (list, tuple)):
            scope = ' '.join(scope)
        self.scope = scope
        self.email = impersonate_as
        self.life_time = life_time
        self.validate_certificate = validate_certificate

    def get_claims(self):
        request_time = int(time())
        claims = {
            "iss": self.service_email,
            "scope": self.scope,
            "aud": "https://accounts.google.com/o/oauth2/token",
            "iat": request_time,
            "exp": request_time + self.life_time,
        }
        if self.email is not None:
            claims['prn'] = self.email
        return claims

    def _cache_key(self):
        """Key used to identify in cache"""
        return 'token:%s:%s:%s' % (self.service_email, self.scope, self.email)

    def sign(self, message):
        return '.'.join((message, google_base64_url_encode(sing_RS256(message, self.key))))

    def get_signed_assertion(self):
        header = google_base64_url_encode(dumps(JWT_HEADER))
        claims = google_base64_url_encode(dumps(self.get_claims()))
        payload = '.'.join((header, claims))
        return self.sign(payload)

    def get_payload(self):
        from urllib import urlencode
        return urlencode({
            "grant_type": 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            "assertion": self.get_signed_assertion(),
        })

    def _cache_get(self):
        return memcache.get(self._cache_key())

    def _cache_set(self, token):
        memcache.set(self._cache_key(), token, token['expires_in'])

    def get_token(self):
        """
        Retrieves and returns access token from cache or from Google auth.
        """
        token = self._cache_get()
        if not token:
            # logging.debug('Fetching new token for %s/%s.' % (self.service_email, self.email))

            call = SavedCall(fetch,
                'https://accounts.google.com/o/oauth2/token',
                method='POST',
                payload=self.get_payload(),
                validate_certificate=self.validate_certificate,
            )
            result = call()
            if str(result.status_code) == '5':
                sleep(0.1)
                result = call()
            if result.status_code != 200:
                error = ''
                try:
                    response = loads(result.content)
                    error = response['error']
                except Exception, e:
                    pass
                if error == 'invalid_grant':
                    raise InvalidGrantException(result, "Error getting token for %r (service: %r)" % (self.service_email, self.email))
                raise Exception(result.status_code, result.content)  # TODO: custom exception
            token = loads(result.content)
            self._cache_set(token)
        return token

    def __str__(self):
        token = self.get_token()
        if token:
            return '%s %s' % (token['token_type'], token['access_token'])
        else:
            return ''


def sing_RS256(message, key):
    """
    Generates a sign using SHA256withRSA (also known as RSASSA-PKCS1-V1_5-SIGN with the SHA-256 hash function).
    Needed to make an Signed JSON Web Tokens request (Signed JWT assertion)
    """
    if isinstance(key, StringTypes):
        if len(key) > 800:  # key as string
            key_data = key
        else:  # key as file
            key_data = open(key).read()
    elif hasattr(key, 'read'):
        key_data = key.read()
    key = RSA.importKey(key_data)
    h = SHA256.new(message)
    signer = PKCS1_v1_5.new(key)
    return signer.sign(h)


def google_base64_url_encode(data):
    return urlsafe_b64encode(data)  # original google api also rstrips '=' from base64 why? #.rstrip('=')
