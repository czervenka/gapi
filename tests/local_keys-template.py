# service e-mail from Google API project
SERVICE_EMAIL = 'xxx@developer.gserviceaccount.com'  # an API service email to use

# The key from Google API console in PEM format. The downloaded *.p12 file can
# be converted using convert.py script.
# The value could be either path to the PEM file or it's content.
SERVICE_KEY = '''
-- paste PEM key here --
'''.strip()

# the user whose calendar, docs and tasks will be plaied with during tests
USER_EMAIL = 'google_email@example.com'
