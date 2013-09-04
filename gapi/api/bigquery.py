# Copyright 2013 Lukas Lukovsky <lukas.lukovsky@gmail.com>
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
__author__ = 'Lukas Lukovsky <terramexx@gmail.com>'

from ..client import ApiService, ApiResource


class Service(ApiService):

    _base_url = 'https://www.googleapis.com/bigquery/v2'
    _default_scope = 'https://www.googleapis.com/auth/bigquery'

    @property
    def _resources(self):
        return [DataSets, Jobs, JobsQueries, Tables]

ApiService._services['bigquery'] = Service


class DataSets(ApiResource):
    project_id = None

    _name = 'datasets'
    _methods = ['list']

    @property
    def _base_path(self):
        return '/projects/%s/datasets' % self.project_id


class Jobs(ApiResource):
    project_id = None

    _name = 'jobs'
    _methods = 'get', 'insert', 'list'

    @property
    def _base_path(self):
        return '/projects/%s/jobs' % self.project_id


class JobsQueries(ApiResource):
    project_id = None

    _name = 'jobs_queries'
    _methods = 'getQueryResults', 'query'

    @property
    def _base_path(self):
        return '/projects/%s/queries' % self.project_id

    def _api_getQueryResults(self, id, **kwargs):
        return ApiResource._api_get(self, id, method='GET', params=kwargs)

    def _api_query(self, query, **kwargs):
        return self._service.fetch(self._get_item_url({}), method='POST', payload=query, params=kwargs)


class Tables(ApiResource):
    project_id = None

    _name = 'tables'
    _methods = 'get', 'update'

    @property
    def _base_path(self):
        return '/projects/%s' % self.project_id

    def _get_item_url(self, dataset_id, table_id):
        return '%s/datasets/%s/tables/%s' % (self._base_url, dataset_id, table_id)

    def _api_get(self, dataset_id, table_id, **kwargs):
        return self._service.fetch(
            self._get_item_url(dataset_id, table_id), method='GET', params=kwargs)

    def _api_update(self, dataset_id, table_id, body, **kwargs):
        return self._service.fetch(
            self._get_item_url(dataset_id, table_id), method='PUT', payload=body, params=kwargs)
