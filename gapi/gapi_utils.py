import logging
from time import sleep
from gae_services import fetch, DeadlineExceededError, ApiProxy_DeadlineExceededError


RETRY_COUNT = 3
RETRY_MULTIPLIER = 3
USE_GZIP = True


from StringIO import StringIO
import gzip

def gunzip_str(data):
    return gzip.GzipFile(fileobj=StringIO(data)).read()

class SavedCall(object):

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
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

    original_retry_count = retry_count
    retry_delay = 0.1
    succeeded = False
    call = SavedCall(fetch, *args, **kwargs)

    while not succeeded and retry_count:
        try:
            result = call()
            succeeded = True
        except (DeadlineExceededError, ApiProxy_DeadlineExceededError), e:
            error_message = 'exceeded deadline'
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
    if result.headers.get('content-encoding', None) == 'gzip':
        result.content = gunzip_str(result.content)
    return result
