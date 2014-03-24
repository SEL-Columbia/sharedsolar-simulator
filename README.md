# sharedsolar-simulator

## About

This is a simple [HTTP](http://en.wikipedia.org/wiki/Http) server which simulates how physical [SharedSolar](http://sharedsolar.org/) hardware in the field interacts with the [SharedSolar android app](https://github.com/SEL-Columbia/sharedsolar-android), to enable app development in the absence of said hardware.

## Usage

1. Determine the hostname or ip address of the computer running the simulator

  The computer runnning this simulator must be visible to the android device or emulator running the app, so make sure both are on the same network.

2. Pick a port number compatible with the user account running this simulator (8000 is usually a good choice) and start the simulator from a terminal prompt, using the hostname or ip address from step 1:

  ```
$ python sharedsolar_simulator.py 198.27.127.57 8000
```

3. Edit the <tt>config.xml</tt> file in the <tt>/res/values/</tt> folder of your android project code so that the <tt>meter</tt> and <tt>gateway</tt> urls match what was used in step 2.

  For each endpoint to simulate, add an <tt>APPURL=[original production url]</tt> value in the query path, so the simulator knows how to handle and respond to it (see the [config.xml](config.xml) in this repo for an example).

  Requests from the android app will be echoed in the terminal, like this:

  ```
$ python sharedsolar_simulator.py 198.27.127.57 8000
198.27.127.69 - - [24/Mar/2014 11:11:31] "POST /cgi-bin/shared_solar_simulator.py/?APPURL=/vendor/validate HTTP/1.1" 200 -
198.27.127.69 - - [24/Mar/2014 11:11:38] "POST /cgi-bin/shared_solar_simulator.py/?APPURL=/vendor/validate HTTP/1.1" 200 -
```

## Extensibility

Each url to be simulated needs to be both *declared* and *implemented* as a separate handling function.

Each handling function needs to accept the BaseHTTPServer object and the cgi-parsed FieldStorage data, and send an http response.

The declarations happen in the [sharedsolar_simulator.py](sharedsolar_simulator.py) file, in the SharedSolarHandler class,
where the URLDispatcher is invoked and run.

The implementations are placed in the [sharedsolar_urls.py](sharedsolar_urls.py) file.


## Acknowledgements

* [Doug Hellmann](http://www.doughellmann.com/) for his article on [BaseHTTPServer](http://pymotw.com/2/BaseHTTPServer/)
* [Guido van Rossum](http://www.python.org/~guido/) for his article [Five-minute Multimethods in Python](http://www.artima.com/weblogs/viewpost.jsp?thread=101605) which inspired the [url_dispatcher.py](url_dispatcher.py) code
