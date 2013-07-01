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

import logging
from json import loads, dumps
from copy import deepcopy
from .oauth2 import TokenRequest
from .exceptions import GoogleApiHttpException, NotFoundException
from google.appengine.api.urlfetch import fetch


class Service(object):

    BASE_URL = 'https://www.googleapis.com'

    def __init__(self, service_email, service_key, scope=None, email=None):
        self._email = None
        self._scope = None
        self.scope = scope
        self.email = email
        self._service_email = service_email
        self._service_key = service_key

    def _get_token(self):
        if not self.email:
            return None
        if self.token is None:
            self.token = TokenRequest(self._service_email, self._service_key, self.scope, self.email)
        return self.token

    def _get_email(self):
        return self._email

    def _set_email(self, email):
        if self.email != email:
            self.token = None
            self._email = email

    def _del_email(self):
        self.email = None

    email = property(_get_email, _set_email, _del_email)

    def _get_scope(self):
        return self._scope

    def _set_scope(self, scope):
        if self._scope != scope:
            self._scope = scope
            self.token = None

    def _del_scope(self):
        self._scope = None
        self.token = None

    scope = property(_get_scope, _set_scope, _del_scope)

    def fetch(self, url, method='GET', headers={}, payload=None, params={}):
        from urllib import urlencode
        kwargs = {}
        for k in 'url', 'method', 'headers', 'payload', 'params':
            kwargs[k] = locals()[k]
        if params:
            url += '?' + urlencode(params)
        if 'content-type' not in headers:
            headers['content-type'] = 'application/json'
        headers['Authorization'] = str(self._get_token())
        payload = dumps(payload)
        result = fetch(url=url, method=method, headers=headers, payload=payload)
        if str(result.status_code)[0] != '2':
            if result.status_code == 404:
                raise NotFoundException(result)
            else:
                raise GoogleApiHttpException(result)
        else:
            if result.status_code == 204:
                return None
            else:
                return ApiResult(loads(result.content), self.fetch, kwargs)


class ApiResult(dict):

    def __init__(self, data, query, query_kargs):
        self.query = query
        self.query_kwargs = query_kargs
        super(self.__class__, self).__init__(data)

    def get_next_page(self, page_token):
        kwargs = deepcopy(self.query_kwargs)
        kwargs['params']['pageToken'] = page_token
        return self.query(**kwargs)

    def next_page(self):
        page_token = self.get('nextPageToken', None)
        if page_token:
            return self.get_next_page(page_token)

    def iter_pages(self):
        yield self

        page = self.next_page()
        while page:
            yield page
            page = page.next_page()


