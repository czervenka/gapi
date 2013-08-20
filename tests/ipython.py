#!/usr/bin/env python
import sys
import IPython

sys.path.insert(0, '/usr/local/google_appengine')
sys.path.insert(0, '..')

import dev_appserver
dev_appserver.fix_sys_path()

from google.appengine.api import apiproxy_stub_map

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

from google.appengine.api import urlfetch_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'urlfetch',
    urlfetch_stub.URLFetchServiceStub()
)
from google.appengine.api.memcache import memcache_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'memcache',
    memcache_stub.MemcacheServiceStub(),
)

import local_keys

from IPython.config.loader import Config


IPython.embed()
