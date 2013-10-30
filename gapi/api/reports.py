# Copyright 2013 Lukas Marek <lukas.marek@gmail.com>
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
from datetime import date, datetime, timedelta
from ..gapi_utils import api_fetch
from ..client import ApiService, ApiResource, value_to_gdata


__author__ = 'Robin Gottfried <google@kebet.cz>'


# https://www.googleapis.com/admin/reports/v1/activity/users/{userKey}/applications/{applicationName}

class Service(ApiService):

    _base_url = 'https://www.googleapis.com/admin/reports/v1'
    _default_scope = 'https://www.googleapis.com/auth/admin.reports.usage.readonly'

    @property
    def _resources(self):
        return [Usage]

ApiService._services['reports'] = Service


class Usage(ApiResource):
    _name = 'usage'
    _methods = 'get', 'get_latest',
    _base_path = '/usage/users/{user}/dates/{date}'

    def _api_get(self, user, day, **kwargs):
        if isinstance(day, (datetime, date)):
            day = day.strftime('%Y-%m-%d')
        url = self._base_url.format(user=user, date=day)
        print '%r' % url
        return self._service.fetch(url, method='GET', params=kwargs)

    def _api_get_latest(self, user, max_age=8, **kwargs):
        from ..exceptions import GoogleApiHttpException
        day = date.today()
        age = 1
        result = None
        while not result and age <= max_age:
            try:
                result = self._api_get(user, day-timedelta(age), **kwargs)
            except GoogleApiHttpException, e:
                # would be nice if Google had returned useful informations on
                # data not available
                if e.code == 400:
                    age *= 2
                else:
                    raise
        return result



