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
Compatibility layer providing services compatible with those in Google Appengine.
"""
MEMCACHE_CLIENT = None

try:
    import google.appengine
    GAE = True
    from google.appengine.api import memcache as MEMCACHE_CLIENT
    from google.appengine.api.urlfetch import fetch, DeadlineExceededError
    from google.appengine.runtime.apiproxy_errors import DeadlineExceededError as ApiProxy_DeadlineExceededError

except ImportError:
    GAE=False

    import urllib2

    def local_fetch(url, payload=None, method='GET', headers={}, deadline=6, validate_certificate=True):
        # FIXME: validate_certificate not used

        opener = urllib2.build_opener()
        request = urllib2.Request(url, data=payload, headers=headers)
        request.get_method = lambda: method
        return opener.open(request, timeout=deadline)

    def fetch(*args, **kwargs):

        response = local_fetch(*args, **kwargs)
        return type('FetchResult', (object,), {
                'content': response.read(),
                'headers': response.headers,
                'header_msg': response.headers,
                'status_code': response.getcode(),
            })

    # TODO: translate urlfetch exceptions to google's exceptins
    class ApiProxy_DeadlineExceededError(Exception): pass
    class DeadlineExceededError(Exception): pass

def get_memcache(servers=['127.0.0.1:11211'], debug=False):
    global MEMCACHE_CLIENT
    if MEMCACHE_CLIENT is None:
        import memcache
        MEMCACHE_CLIENT = memcache.Client(servers, debug=debug)
        MEMCACHE_CLIENT.Client = lambda : memcache.Client(servers)
    return MEMCACHE_CLIENT
