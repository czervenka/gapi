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

from .client import ApiService, ApiResource

class Service(ApiService):

    _base_url = 'https://www.googleapis.com/calendar/v3'
    _default_scope = 'https://www.googleapis.com/auth/calendar'

    @property
    def _resources(self):
        return [Events, Calendar, Calendars, Colors]

ApiService._services['calendar'] = Service


class Events(ApiResource):

    calendar = 'primary'

    _name = 'events'
    _methods = 'list', 'get', 'insert', 'update', 'patch', 'delete', 'instances', 'updated'

    @property
    def _base_path(self):
        return '/calendars/%s/events' % self.calendar

    def __init__(self, service):
        super(self.__class__, self).__init__(service)

    def _api_instances(self, id, **kwargs):
        return self._service.fetch(self._get_item_url({'id': id}) + '/instances', method='GET', params=kwargs)

    def _api_updated(self, **kwargs):
        kwargs['fields'] = 'updated'
        return self.list(**kwargs)['updated']


class Calendar(ApiResource):
    _name = 'calendar'
    _base_path = '/calendars'
    _methods = 'get', 'insert', 'update', 'patch', 'delete', 'clear'

    def _api_get(self, id='primary', **kwargs):
        return super(self.__class__, self)._api_get(id, **kwargs)

    def _api_clear(self, id='primary', **kwargs):
        return self._service.fetch(self._get_item_url({'id': id}) + '/clear', method='POST', params=kwargs)


class Calendars(ApiResource):
    _name = 'calendars'
    _base_path = '/calendarList'
    _methods = 'list', 'get', 'insert', 'update', 'patch', 'delete'
    email = 'me'

    @property
    def _base_path(self):
        return '/users/%s/calendarList' % self.email

class Colors(ApiResource):
    _name = 'colors'
    _base_path = '/colors'
    _methods = ['list']
