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

from ..client import ApiService, ApiResource


class Service(ApiService):

    _base_url = 'https://www.googleapis.com/tasks/v1'
    _default_scope = 'https://www.googleapis.com/auth/tasks'

    @property
    def _resources(self):
        return [Tasks, Lists]

ApiService._services['tasks'] = Service


class Tasks(ApiResource):

    list_id = '@default'

    _name = 'tasks'
    _methods = 'list', 'get', 'insert', 'update', 'patch', 'delete', 'watch'

    @property
    def _base_path(self):
        return '/lists/%s/tasks' % self.list_id

    def __init__(self, service):
        super(self.__class__, self).__init__(service)


class Lists(ApiResource):
    _name = 'lists'
    _methods = 'list', 'get', 'insert', 'update', 'patch', 'delete'
    user = '@me'

    @property
    def _base_path(self):
        return '/users/%s/lists' % self.user
