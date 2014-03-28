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

def _send_response (server, response, content_type=TEXT_HTML, rc=response_code_number(FORBIDDEN)):
    """Logic to send an appropriate server reply, with the given
    content type, response code, and response content"""
    
    server.send_response(rc)
    server.send_header("Content-type", content_type)
    server.end_headers()
    server.wfile.write(response)
    
def _with_valid_device (form, response_fn, bad_response_fn):
    """Check the POST form data for the existence of the 'vendordevice_id' parameter
    (which corresponds to the tablet device's mac address), and if present, invoke
    the response_fn in reply, else invoke the bad_response_fn"""

    try:
        device_id = form.getvalue("vendordevice_id")
        # the actual server will check the device_id vs a permitted list
        # but for the purposes of the simulator, we'll allow any value
        if device_id is not None:
            return response_fn()

    except KeyError:
        pass

    return _bad_response_fn()


# /vendor/validate
def vendor_validate (server, form):
    """Handle the /vendor/validate request from the Android tablet app.

    This request occurs when clicking the 'Vendor Login' button."""

    _with_valid_device (form,
                        lambda: _send_response (server, ALLISWELL, rc=response_code_number(ALLISWELL)),
                        lambda: _send_response (server, FORBIDDEN))
    

# /vendor/accounts/list
def vendor_accounts_list (server, form):
    """Handle the /vendor/accounts/list request from the Android tablet app.

    This request occurs when clicking the 'Accounts' button.

    The function is expected to return a list of json objects, each containing:

    { "cid",   # Circuit ID
      "aid",   # Account ID
      "cr",    # amount of credit remaining
      "status" # boolean: is the circuit active or not
    }

    """

    reply_fn = lambda: _send_response (server, FORBIDDEN)

    # get the account and circuit list from a file in the data folder
    try:
        with open(os.path.join(settings.DATA_FOLDER, settings.ACCOUNTS_LIST), 'r') as f:
            account_id_list = f.read().splitlines()

        with open(os.path.join(settings.DATA_FOLDER, settings.CIRCUITS_LIST), 'r') as f:
            circuit_id_list = f.read().splitlines()

        data = []
        # produce some random results for each account
        for account_id in account_id_list:
            data.append({ 'cid': circuit_id_list[ int(random() * len(circuit_id_list)) ],
                          'aid': account_id,
                          'cr': "%0.2f" % (random() * 1000),
                          'status': (random() > 0.49) })

        reply_fn = _send_response (server, json.dumps(data), content_type=APP_JSON, rc=response_code_number(ALLISWELL))
        return

    except IOError:
        pass

    _with_valid_device (form, reply_fn, lambda: _send_response (server, FORBIDDEN))

 
# /vendor/account/toggle
def vendor_account_toggle (server, form):
    """Handle the /vendor/account/toggle request from the Android tablet app.

    This request occurs when clicking the status button from within the list
    of accounts, to change an account's status to off from on, and vice-versa.

    The actual server will update a database with the status switch but since
    the simulator currently just sets this randomly (see vendor_accounts_list,
    above) we'll just respond ok for now, if the request is otherwise valid."""

    _with_valid_device (form,
                        lambda: _send_response (server, ALLISWELL, rc=response_code_number(ALLISWELL)),
                        lambda: _send_response (server, FORBIDDEN))

# /vendor/account/credit/add
def vendor_account_credit_add (server, form):
    """Handle the /vendor/account/credit/add request from the Android tablet app.

    This request occurs when clicking the credit (+)/(-) buttons for a given
    account, to add/subtract credit.

    The actual server will update a database with the additional amount but
    since the simulator currently just sets this randomly (see vendor_accounts_list,
    above) we'll just respond ok for now, if the request is otherwise valid."""

    _with_valid_device (form,
                        lambda: _send_response (server, ALLISWELL, rc=response_code_number(ALLISWELL)),
                        lambda: _send_response (server, FORBIDDEN))

# /admin/circuits/use 
def admin_circuits_use (server, form):
    """Handle the /admin/circuits/use request from the Android tablet app.

    This request occurs when clicking the 'Charts' button.

    The function is expected to return a list of json objects, each containing:

    { "cid",      # Circuit ID
      "aid",      # Account ID
      "wh_today", # Watt Hours Today
      "pmax",     # Power Max parameter
      "emax",     # Energy Max PARAMETER
      "watts",    # Watts
      "cr"        # amount of credit available
    }

    """

    reply_fn = lambda: _send_response (server, FORBIDDEN)

    # get the account and circuit list from a file in the data folder
    try:
        with open(os.path.join(settings.DATA_FOLDER, settings.ACCOUNTS_LIST), 'r') as f:
            account_id_list = f.read().splitlines()

        with open(os.path.join(settings.DATA_FOLDER, settings.CIRCUITS_LIST), 'r') as f:
            circuit_id_list = f.read().splitlines()

        data = []
        # produce some random results for each circuit
        for circuit_id in circuit_id_list:
            data.append({ 'cid': circuit_id,
                          'aid': account_id_list[ int(random() * len(account_id_list)) ],
                          'wh_today': "%0.2f" % (random() * 100),
                          'pmax': "%0.2f" % (random() * 10),
                          'emax': "%0.2f" % (random() * 10),
                          'watts': "%0.2f" % (random() * 100),
                          'cr': "%0.2f" % (random() * 500) })

        reply_fn = _send_response (server, json.dumps(data), content_type=APP_JSON, rc=response_code_number(ALLISWELL))

    except IOError:
        pass

    _with_valid_device (form, reply_fn, lambda: _send_response (server, FORBIDDEN))

# /fieldtech/device/sync
def fieldtech_device_sync (server, form):
    """Handle the /fieldtech/device/sync request from the Android tablet app.

    This request occurs from within the 'TechHome' portion of the app.

    The actual server will update a database with the required info but
    we'll just respond ok for now, if the request is otherwise valid."""

    _with_valid_device (form,
                        lambda: _send_response (server, ALLISWELL, rc=response_code_number(ALLISWELL)),
                        lambda: _send_response (server, FORBIDDEN))

# remaining app request urls:
# /manage/update_tokens
# /manage/make_tokens
