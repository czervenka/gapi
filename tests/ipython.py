#!/usr/bin/env python
import sys
import IPython

sys.path.insert(0, '/usr/local/google_appengine')
sys.path.insert(0, '..')

import dev_appserver
dev_appserver.fix_sys_path()
from IPython.config.loader import Config
IPython.embed()
