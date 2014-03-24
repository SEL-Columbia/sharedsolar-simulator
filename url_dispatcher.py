#!/usr/bin/env python

""" 
URLDispatcher is a framework for defining url response functions,
based on the requested query path endpoint.

It requires that each simulated url contain an 'APPURL=' component
as part of the query string (see the included android config.xml
file for an example).

"""

# Content-types
TEXT_HTML = 'text/html'
APP_JSON  = 'application/json'

# Response Codes
ALLISWELL = '200 OK'
NOT_FOUND = '404 Not Found'
FORBIDDEN = '403 Forbidden'

def response_code_number (rc):
    """Convert the Response Code string (rc) into a number.
    This fn assumes the code string begins with a number,
    like the constants defined above."""

    try:
        return int(rc.split()[0])
    except:
        # deal with bad response code strings
        return 500

class URLDispatcher:
    """Class to define, store, and invoke server request functions
    based on the query string (url path) of the request"""

    def __init__(self):
        self.handlers = {}

    def add_url(self, url_path, handler_fn):
        self.handlers[url_path] = handler_fn

    def default_handler (self, server):
        server.send_response(response_code_number(NOT_FOUND))
        server.send_header("Content-type", TEXT_HTML)
        server.end_headers()
        server.wfile.write(NOT_FOUND)

    def run(self, server, path_query, cgi_form):
        try:
            url_path = filter(None, path_query.split('APPURL='))[0]
            self.handlers[url_path](server, cgi_form)
        except:
            self.default_handler(server)
