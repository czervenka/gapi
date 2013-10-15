# Copyright 2007 Robin Gottfried <copyright@kebet.cz>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = 'Robin Gottfried <google@kebet.cz>'

from json import loads


class GapiException(Exception):
    pass


class GoogleApiHttpException(GapiException):

    def __init__(self, result):
        self.code = result.status_code
        self.error = ''
        self.content = ''
        try:
            self.content = loads(result.content)
            if 'error' in self.content:
                self.error = self.content['error']
        except:
            self.error = result.content

    def __str__(self):
        return '%s %s' % (self.code, self.error)


class NotFoundException(GoogleApiHttpException):
    pass


class DailyLimitExceededException(GoogleApiHttpException):
    def __init__(self, result, url):
        self.url = url
        super(self.__class__, self).__init__(result)


class RateLimitExceededException(GoogleApiHttpException):
    def __init__(self, result, url):
        self.url = url
        super(self.__class__, self).__init__(result)


class PermitionException(GoogleApiHttpException):
    def __init__(self, result, message):
        self.message = message
        super(PermitionException, self).__init__(result)

    def __str__(self):
        return '%s %s (%r)' % (self.code, self.error, self.message)



class UnauthorizedUrl(PermitionException):
    pass


class InvalidGrantException(PermitionException):
    pass

class AccessDeniedException(PermitionException):
    pass


class InvalidCredentialsException(PermitionException):
    pass


class UnauthorizedException(GoogleApiHttpException):
    def __init__(self, result, url):
        self.url = url
        super(self.__class__, self).__init__(result)
