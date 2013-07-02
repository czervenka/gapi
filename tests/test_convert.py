def test_convert_generates_key():
    """Convert generates PEM key from google PKCS12"""
    from os.path import dirname
    import sys
    from google.appengine import api
    sys.path.insert(0, dirname(dirname(__file__)))

    from convert_key import main
    key = main('convert.py', 'test_google_bundle.p12')
    key_to_compare = open('test_generated_key.pem', 'rb').read()
    assert key == key_to_compare
