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

    _base_url = 'https://www.googleapis.com/admin/directory/v1'
    _default_scope = 'https://www.googleapis.com/auth/admin.directory.user.readonly https://www.googleapis.com/auth/admin.directory.group.readonly'

    @property
    def _resources(self):
        return [Members, Users]

ApiService._services['admin'] = Service


class Members(ApiResource):
    _name = 'members'
    _methods = 'delete', 'get', 'insert', 'list', 'patch', 'update'

    def __init__(self, *args, **kwargs):
        super(Members, self).__init__(*args, **kwargs)
        self.group_key = None

    @property
    def _base_path(self):
        return '/groups/%s/members' % self.group_key


class Users(ApiResource):

    _name = 'users'
    _methods = 'list', 'get', 'insert', 'update', 'patch', 'delete'

    @property
    def _base_path(self):
        return '/users'
