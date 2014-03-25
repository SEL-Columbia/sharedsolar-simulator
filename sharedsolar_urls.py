#!/usr/bin/env python

"""
Implement all the urls to be simulated here, matching the values defined
in the android config.xml file.

Each function needs to  accept the server object and the cgi-parsed
FieldStorage data, and send an http response.

Each function also needs to be defined in the SharedSolarHandler class,
where the URLDispatcher is invoked and run.

"""

import json
import os
from random import random

from url_dispatcher import TEXT_HTML, APP_JSON, ALLISWELL, FORBIDDEN, response_code_number
import settings

# /vendor/validate
def vendor_validate (server, form):
    """Handle the /vendor/validate request from the Android tablet app.

    This request occurs when clicking the 'Vendor Login' button.

    It will POST a single value, vendordevice_id, which corresponds to
    the tablet device's mac address."""

    response = FORBIDDEN
    try:
        device_id = form.getvalue("vendordevice_id")

        # the actual server will check the device_id vs a permitted list
        # but for the purposes of the simulator, we'll allow all logins
        response = ALLISWELL

    except KeyError:
        pass
    
    server.send_response(response_code_number(response))
    server.send_header("Content-type", TEXT_HTML)
    server.end_headers()
    server.wfile.write(response)

# /vendor/accounts/list
def vendor_accounts_list (server, form):
    """Handle the /vendor/accounts/list request from the Android tablet app.

    This request occurs when clicking the 'Accounts' button.

    It will POST a single value, vendordevice_id, which corresponds to
    the tablet device's mac address.

    The function is expected to return a list of json objects, each containing:

    { "cid",   # Circuit ID
      "aid",   # Account ID
      "cr",    # amount of credit remaining
      "status" # boolean: is the circuit active or not
    }

    """

    response = FORBIDDEN
    try:
        # this version of the simulator allows all logins and doesn't
        # keep state, so the device_id value doesn't matter; it simply
        # needs to be present in the POST request
        device_id = form.getvalue("vendordevice_id")

        # get the account list from a file in the data folder
        try:
            with open(os.path.join(settings.DATA_FOLDER, settings.ACCOUNTS_LIST), 'r') as f:
                account_id_list = f.read().splitlines()

            data = []
            # produce some random results for each account
            for account_id in account_id_list:
                data.append({ 'cid': '.'.join(['192', '168', '1', str(int(random() * 256))]),
                              'aid': account_id,
                              'cr': "%0.2f" % (random() * 1000),
                              'status': (random() > 0.49) })

            server.send_response(response_code_number(ALLISWELL))
            server.send_header("Content-type", APP_JSON)
            server.end_headers()
            server.wfile.write(json.dumps(data))
                      
        except IOError:
            pass
            
    except KeyError:
        pass
    
    server.send_response(response_code_number(response))
    server.send_header("Content-type", TEXT_HTML)
    server.end_headers()
    server.wfile.write(response)


