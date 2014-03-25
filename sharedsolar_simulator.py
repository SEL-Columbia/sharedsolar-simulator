#!/usr/bin/env python

"""
This is a simple http server which simulates how physical SharedSolar 
hardware in the field interacts with the android device app.

"""

import BaseHTTPServer
import cgi
import urlparse
import sys

from url_dispatcher import URLDispatcher
import sharedsolar_urls

class SharedSolarHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    """A simple http server for handling designated requests,
    based on Doug Hellmann's example code:

    http://pymotw.com/2/BaseHTTPServer/
    """ 

    def do_POST (self):
        path = urlparse.urlparse(self.path)
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        u = URLDispatcher()
        # define which response function to use,
        # based on the value of the path.query
        # prefixed by APPURL (see the config.xml file)
        u.add_url('/vendor/validate', sharedsolar_urls.vendor_validate)
        u.add_url('/vendor/accounts/list', sharedsolar_urls.vendor_accounts_list)
        u.add_url('/vendor/account/toggle', sharedsolar_urls.vendor_account_toggle)
        u.add_url('//vendor/account/credit/add', sharedsolar_urls.vendor_account_credit_add)

        u.run(self, path.query, form)

    # request methods the android app doesn't make, but 
    # nevertheless we need to respond to as an http server
    def do_GET (self):
        u = URLDispatcher()
        u.run(self, None)

    def do_HEAD (self):
        u = URLDispatcher()
        u.run(self, None)

if __name__ == '__main__':
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((host, port), SharedSolarHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

    except (IndexError, ValueError):
        # define the usage 
        print sys.argv[0], '[host (name or ip address)]', '[port number]'
