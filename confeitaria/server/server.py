import inspect
import multiprocessing
import time

import cgi
import wsgiref.simple_server as simple_server

class Server(object):
    """
    The ``Server`` objects listen to HTTP requests and serve responses according
    to the page object returned values.
    """

    def __init__(self, page, port=8080):
        self.page = page
        self.port = port
        self._process = None

    def run(self):
        """
        This method starts the server up serving the given page.
        A page is an object of a class as the one below:

        >>> class TestPage(object):
        ...     def index(self):
        ...         return "This is a test"

        To run it, just call `Server.run()`, as in:

        >>> s = Server(TestPage())

        >>> import multiprocessing, time
        >>> p = multiprocessing.Process(target=s.run)
        >>> p.start()
        >>> time.sleep(1)

        Then the server is supposed to serve the content provided by the page:

        >>> import requests
        >>> r = requests.get('http://localhost:8080/')
        >>> r.text
        u'This is a test'
        >>> r.status_code
        200
        >>> r.headers['content-type']
        'text/html'

        >>> p.terminate()

        You can also, mostly for testing purposes, start up a server through a
        ``with`` statement:

        >>> with Server(TestPage()):
        ...     r = requests.get("http://localhost:8080")
        ...     r.text
        u'This is a test'
        """
        httpd = simple_server.make_server('', self.port, self._run_app)
        print "Serving on port 8000..."
        httpd.serve_forever()

    def _run_app(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        components = (c for c in path_info.split('/') if c)
        page = self.page

        for c in components:
            try:
                page = getattr(page, c)
            except AttributeError:
                break

        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        query_parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
        for key, value in query_parameters.items():
            if isinstance(value, list) and len(value) == 1:
                query_parameters[key] = value[0]

        start_response(status, headers)

        if hasattr(page, 'index'):
            try:
                names, _, _, values = inspect.getargspec(page.index)
                values = values if values is not None else []
                names = names[1:]

                page_parameters = {
                    name: value
                    for name, value in zip(reversed(names), reversed(values))
                }
                merged_parameters = {
                    name: query_parameters.get(name, value)
                    for name, value in page_parameters.items()
                }

                return page.index(**merged_parameters)
            except TypeError as te:
                if (type(page) is type and callable(getattr(page, 'index', None))):
                    raise NotPageError(('{p} is not a page object'
                        ' (did you forget to instantiate it?)').format(p=page))
                else:
                     raise te
        else:
            raise NotPageError(('{p} is not a page object,'
                ' has no index() method.').format(p=page))

    def __enter__(self):
        self._process = multiprocessing.Process(target=self.run)
        self._process.start()
        time.sleep(1)

    def __exit__(self, type, value, traceback):
        self._process.terminate()
        self._process = None

class NotPageError(Exception):
    pass
