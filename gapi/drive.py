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
__author__ = 'Lukas Marek <lukas.marek@gmail.com>'


from .client import ApiService, ApiResource


class Service(ApiService):

    _base_url = 'https://www.googleapis.com/drive/v2'
    _default_scope = 'https://www.googleapis.com/auth/drive'

    @property
    def _resources(self):
        return [Files, Revisions, Changes, About, Permissions]

ApiService._services['drive'] = Service


class Files(ApiResource):
    _name = 'files'
    _methods = 'list', 'get', 'insert', 'update', 'patch', 'delete', 'touch', 'trash', 'untrash'
    _base_path = '/files'

    def _api_touch(self, id, **kwargs):
        return self._service.fetch(self._get_item_url({'id': id}) + '/touch', method='POST', params=kwargs)

    def _api_trash(self, id, **kwargs):
        return self._service.fetch(self._get_item_url({'id': id}) + '/trash', method='POST', params=kwargs)

    def _api_untrash(self, id, **kwargs):
        return self._service.fetch(self._get_item_url({'id': id}) + '/untrash', method='POST', params=kwargs)


class Revisions(ApiResource):
    _name = 'revisions'
    _methods = 'get', 'list', 'patch', 'update'

    def __init__(self, *args, **kwargs):
        super(Revisions, self).__init__(*args, **kwargs)
        self.file_id = None

    @property
    def _base_path(self):
        if self.file_id is None:
            raise ValueError('Unknown file_id!')
        return '/files/%s/revisions' % self.file_id


class About(ApiResource):
    _name = 'about'
    _methods = ['get']
    _base_path = '/about'

    def _api_get(self, **kwargs):
        return self._service.fetch(self._get_item_url({}), method='GET', params=kwargs)


class Changes(ApiResource):
    _name = 'changes'
    _methods = 'get', 'list'
    _base_path = '/changes'

class Permissions(ApiResource):
    _name = 'permissions'
    _methods = 'delete', 'get', 'insert', 'list', 'patch', 'update'

    def __init__(self, *args, **kwargs):
        super(Permissions, self).__init__(*args, **kwargs)
        self.file_id = None

    @property
    def _base_path(self):
        return '/files/%s/permissions' % self.file_id








