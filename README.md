GAPI
====
A library for easy access to Google API from Google App Engine

Introduction
------------
This library allows easy acces to **Google API** from Google **App Engine** (GAE)
application using OAuth 2.0 and **service account**. I is intended to be
lightweight, understandable and resources friendly.

Newer Google's APIs use JSON for communication and Signed JWT Assertation (JSON
Web Token) for OAuth 2.0 authentication. I found it little painful to use the
Google's python library for this task.

**Features** I did not found in Google's library

*(reasons to use this one ;))*

* google.appengine.api.memcache to store auth tokens (only tokens, nothing more),
* simple way to run batch requests,
* automatically repeat request when it fails,
* easy paging through gotten records.

*Note: Only Calendar and Tasks APIs are currently implemented. But others can be added easily*

Quick example
--
        from gapi import Api
        api = Api(
            ['calendar', 'tasks'],  # the apis to use
            '983417309817307013970412734012734289@accounts.google.com',  # API project service client email
            'keys/key.pem',  # API project service key
            'admin@example.com',  # impersonate as user
        )

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

        # batch call
        def process_results(result, request):
            print 'Got results %r' % result

        for n in xrange(10):
            api.calendar.events.list(_callback=process_results)

        api.calendar.fetch_batch()

        # read Google documentation and use IPython to explore all apis


Tiny tutorial
--

... how to access calendar on your Google APPs domain from App Engine

A. Create a GAE project
^^
(see [Introduction](https://developers.google.com/appengine/docs/python/gettingstartedpython27/introduction))

B. Aquire service_email and  service_key. To obtain one, 
^^

1. go to [API Console](https://code.google.com/apis/console) and click "API Access" in the left menu
2. Click the "Create an OAuth 2.0 client ID..." button
3. Fill the form (only "Product name" is required) and click "Next"
4. Select "Service account"  and click "Create client ID"
5. Download the private key to a safe place
6. Write somewhere the Service account EMAIL (will be used in gapi) and client ID (will be used to grant access to you calendar).
7. Use convert_key.py utility to convert downloaded key to PEM format usable in Google App Engine

To be able to access a Google API which requires authentication, register your
client ID in your Google APPs [domain control panel](https://admin.google.com).
Depending on version of control panel, you can add new API client ID under
"Advanced tools" / "Authentication" / "Manage third party OAuth Client access"

To find scopes, you need, try something like:

    # example for calendar api and tasks api

    from gapi import Api
    api = Api(['calendar', 'tasks'], 'anything', 'anything')
    print api.scope

To Do
--

* better documentation
* tests
* build APIs from Googles API [Discovery service](https://www.googleapis.com/discovery/v1/apis)
