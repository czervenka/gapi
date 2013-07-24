def path_fixes():
    from os.path import dirname
    import sys
    sys.path.insert(0, '/usr/local/google_appengine')
    sys.path.insert(0, '..')
    from google.appengine import api

setUp = path_fixes
