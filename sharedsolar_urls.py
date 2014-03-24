#!/usr/bin/env python

"""
Implement all the urls to be simulated here, matching the values defined
in the android config.xml file.

Each function needs to  accept the server object and the cgi-parsed
FieldStorage data, and send an http response.

Each function also needs to be defined in the SharedSolarHandler class,
where the URLDispatcher is invoked and run.

"""

from url_dispatcher import TEXT_HTML, APP_JSON, ALLISWELL, FORBIDDEN, response_code_number

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

