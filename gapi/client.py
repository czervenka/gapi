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

from uuid import uuid1
from datetime import datetime
from gapi import AUTH_TYPE_V2
from .service import Service


def value_to_gdata(value):
    if isinstance(value, datetime):
        if not value.tzinfo:
            raise ValueError('Missing timezone info in datetime value (user dateutil.tz or pytz to add timezone).')
        value = value.isoformat()
    elif isinstance(value, dict):
        value = dict([(k, value_to_gdata(v)) for k, v in value.items()])
    elif isinstance(value, list):
        value = [value_to_gdata(v) for v in value]
    return value


class ApiService(Service):

    _base_url = None
    _services = {}

    def __init__(self, service_email, service_key, scope=None, email=None, validate_certificate=True, auth_type=AUTH_TYPE_V2):
        '''
        @service_email ... service email from Google API console
        @service_key   ... service key in PEM format (either path to file or it's content)
        @scope         ... scope for the service (default RW scope of the api
        @email         ... email of the user to impersonate as
        @validate_certificate ... if validate server certificate
        '''
        if 'scope' is None:
            scope = self._default_scope
        Service.__init__(self, service_email, service_key, scope=scope, email=email, validate_certificate=validate_certificate, auth_type=auth_type)

        # setup resources as self properties
        for resource in self._resources:
            setattr(self, resource._name, resource(self))

    @property
    def _default_scope(self):
        raise NotImplementedError()

        raise NotImplementedError()


class ApiResource(object):

    _methods = 'list', 'get', 'update', 'insert', 'path', 'delete', 'watch'

    def __init__(self, service):
        self._service = service
        for method in self._methods:
            setattr(self, method, getattr(self, '_api_%s' % method))

    @property
    def _base_url(self):
        return '%s%s' % (self._service._base_url, self._base_path)

    def _get_item_url(self, item):
        if 'id' in item:
            return '%s/%s' % (self._base_url, item['id'])
        else:
            return self._base_url

    def _api_list(self, **kwargs):
        kwargs = value_to_gdata(kwargs)
        return self._service.fetch(self._base_url, params=kwargs)

    def _api_insert(self, item, **kwargs):
        kwargs = value_to_gdata(kwargs)
        item = value_to_gdata(item)
        return self._service.fetch(self._get_item_url(item), method='POST', params=kwargs, payload=item)

    def _api_update(self, item, **kwargs):
        kwargs = value_to_gdata(kwargs)
        item = value_to_gdata(item)
        return self._service.fetch(self._get_item_url(item), method='PUT', params=kwargs, payload=item)

    def _api_get(self, id, **kwargs):
        kwargs = value_to_gdata(kwargs)
        return self._service.fetch(self._get_item_url({'id': id}), method='GET', params=kwargs)

    def _api_patch(self, item, **kwargs):
        kwargs = value_to_gdata(kwargs)
        item = value_to_gdata(item)
        return self._service.fetch(self._get_item_url(item), method='PATCH', params=kwargs, payload=item)

    def _api_delete(self, id, **kwargs):
        kwargs = value_to_gdata(kwargs)
        return self._service.fetch(self._get_item_url({'id': id}), method='DELETE', params=kwargs)

    def _api_watch(self, address, id=None, token=None, expiration=None):
        if not id:
            id = str(uuid1())
        payload = {
            'id': id,
            'address': address,
            'type': 'web_hook',
        }
        if token:
            payload['token'] = token
        if expiration:
            payload['params'] = {
                'ttl': expiration
            }
        return self._service.fetch(self._base_url + '/watch', method='POST', payload=payload)
