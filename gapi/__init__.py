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

from .client import ApiService
import calendar
import tasks


class Api(object):
    """
    Google API connector.

    USAGE:
        from gapi import Api
        api = Api(['calendar', 'tasks'], '983417309817307013970412734012734289@accounts.google.com', 'keys/key.pem', 'admin@example.com')

        # list all events
        response = api.calendar.events.list()
        events = []
        for events_page in response.iter_pages():
            events.extend(events_page.get('items', []))

        # update an event
        event =events[0]
        event['summary'] = 'Modified summary: ' + event['summary']
        api.calendar.events.update(event)

        # delete an event
        api.calendar.events.delete(event)

        # to clear calendar completely
        api.calendar.calendar.clear()

        # to impersonate to a different user
        api.impersonate(user_email)

        # read Google documentation and use IPython to explore all apis
    """

    def __init__(self, apis, service_email, service_key, impersonate_as=None, validate_certificate=True):
        all_apis = ApiService._services
        scopes = set()
        services = {}
        for api in apis:
            if not api in all_apis:
                raise ValueError('API %r is not registered. Please import API module first.' % api)
            service = all_apis[api]
            scopes.add(service._default_scope)
            services[api] = service
        self._services = services
        for service_name, service in services.items():
            setattr(
                self,
                service_name,
                service(service_email=service_email, service_key=service_key, scope=list(scopes), email=impersonate_as, validate_certificate=validate_certificate),
            )

    @property
    def scopes(self):
        if self._services:
            return ' '.join(getattr(self, self._services.keys()[0]).scope)
        else:
            return None

    def impersonate(self, email):
        for service in self._services:
            getattr(self, service).email = email
