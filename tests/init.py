def path_fixes():
    from os.path import dirname
    import sys
    import os
    sys.path.insert(0, '/usr/local/google_appengine')
    gapi_path = os.path.dirname(__file__)
    gapi_path = os.path.dirname(gapi_path)
    sys.path.insert(0, gapi_path)
    from google.appengine import api

setUp = path_fixes
