"""Module for the http server classes. """
#added code for handle multi-threading and Python 3.X
#added by shaurobe, kmccabe2, fdemello
from six.moves import BaseHTTPServer
from six.moves import socketserver


class WebServer(socketserver.ThreadingMixIn,BaseHTTPServer.HTTPServer):
    """Class representing an http server. """

    def __init__(self, routes_repo, options, *args, **kw):
        self.timeout = options.timeout_milliseconds/1000
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kw)
        self.routes_repo = routes_repo
        self.options = options
