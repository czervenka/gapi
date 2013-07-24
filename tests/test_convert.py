from init import setUp

def test_convert_generates_key():
    """Convert generates PEM key from google PKCS12"""
    from convert_key import main
    key = main('convert.py', 'test_google_bundle.p12')
    key_to_compare = open('test_generated_key.pem', 'rb').read()
    assert key == key_to_compare
