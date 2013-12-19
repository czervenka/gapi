import logging
from time import sleep
from google.appengine.api.urlfetch import fetch, DeadlineExceededError
from google.appengine.runtime.apiproxy_errors import DeadlineExceededError as ApiProxy_DeadlineExceededError
from google.appengine.api import urlfetch


from gapi.exceptions import RateLimitExceededException



from StringIO import StringIO
import gzip

try:
    import gapi_config
except ImportError:
    gapi_config = type('modul', (object,), {})

RETRY_COUNT = getattr(gapi_config, 'RETRY_DELAY', 4)
RETRY_MULTIPLIER = getattr(gapi_config, 'RETRY_MULTIPLIER', 3)
USE_GZIP = getattr(gapi_config, 'USE_GZIP', True)
DEFAULT_DEADLINE = getattr(gapi_config, 'DEFAULT_DEADLINE', 2)

# FIXME: This is a hot patch - google api did not react to fetch(deadline=...)
# argument. Setting default deadline magically enabled fetch's deadline=....
# (needed on server only - works on local dev)
urlfetch.set_default_fetch_deadline(DEFAULT_DEADLINE)

def gunzip_str(data):
    return gzip.GzipFile(fileobj=StringIO(data)).read()

class SavedCall(object):

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        # logging.debug('Calling %s(%s)' % (self.callback.__name__, ', '.join(list(self.args)+[ '%s=%r' % (k,v) for k,v in self.kwargs.items()])))
        return self.callback(*self.args, **self.kwargs)


def api_fetch(*args, **kwargs):
    retry_count = kwargs.pop('_retry_count', RETRY_COUNT)
    retry_multiplier = kwargs.pop('_retry_multiplier', RETRY_MULTIPLIER)
    use_gzip = kwargs.pop('_use_gzip', RETRY_MULTIPLIER)
    if args:
        url = args[0]
    else:
        url = kwargs.get('url')
    if use_gzip:
        headers = kwargs.get('headers', {})
        headers['accept-encoding'] = 'gzip'
        headers['user-agent'] = 'gapi (gzip)'
        kwargs['headers'] = headers
    if not 'deadline' in kwargs:
        kwargs['deadline'] = DEFAULT_DEADLINE

    original_retry_count = retry_count
    retry_delay = 0.1
    succeeded = False
    call = SavedCall(fetch, *args, **kwargs)

    error_message = 'None'
    last_exception = None
    while not succeeded and retry_count:
        try:
            result = call()
            succeeded = True
        except (DeadlineExceededError, ApiProxy_DeadlineExceededError), e:
            error_message = 'exceeded deadline'
            call.kwargs['deadline'] = call.kwargs.get('deadline', 1) * 3
            logging.debug('Exceeded deadline - new deadline is %rs' % call.kwargs['deadline'])
        except RateLimitExceededException, e:
            error_message = 'rate limit exceeded'
        # except Exception, e:
        #     logging.warning('An unknown error while trying to fetch %r' % url)
        #     logging.warning('Exc class: %s.%s' % (e.__class__.__module__, e.__class__.__name__))
        #     raise e
        if succeeded and str(result.status_code)[0] == '5':
            error_message = 'status code %s' % result.status_code
            succeeded = False
        retry_count -= 1
        if not succeeded and retry_count:
            logging.info('Retrying in %0.2fs due to %s (url: %r; try %d / %d)' % (retry_delay, error_message, url, original_retry_count - retry_count, original_retry_count))
            sleep(retry_delay)
            retry_delay *= retry_multiplier
    if succeeded:
        if result.headers.get('content-encoding', None) == 'gzip':
            result.content = gunzip_str(result.content)
    else:
        if last_exception:
            raise last_exception
        else:
            raise DeadlineExceededError('Api fetch not successful after %s retries' % original_retry_count)
    return result
