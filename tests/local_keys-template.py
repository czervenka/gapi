AUTH_TYPE_V1 = 'oauth.v1'
AUTH_TYPE_V2 = 'oauth.v2'

AUTHv2 = {
    # service e-mail from Google API project
    'service_email': '',  # an API service email to use
    # The key from Google API console in PEM format. The downloaded *.p12 file can
    # be converted using convert.py script.
    # The value could be either path to the PEM file or it's content.
    'service_key': '''
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
'''.strip(),  # an API service key to use
    'impersonate_as': '',   # impersonate as this user during tests
    'auth_type': AUTH_TYPE_V2,
}

AUTHv1 = {
    'service_email': '',
    'service_key': '',
    'impersonate_as': '',
    'auth_type': AUTH_TYPE_V1,
}

AUTH = AUTHv2
