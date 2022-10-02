import os
import mimetypes
import traceback


class Request():
    def __init__(self, request):
        self._request = request

    @property
    def method(self):
        """return client request method"""
        return self._request.splitlines()[0].split()[0]

    @property
    def path(self):
        """return client request path"""
        url = self._request.splitlines()[0].split()[1]
        # do not return query string
        url = url.split('?')[0]
        # * / means index.html
        if url == '/':
            return "/index.html"
        return url.rstrip('/')

    @property
    def protocol(self):
        """return client request protocol(HTTP version)"""
        return self._request.splitlines()[0].split()[2]

    @property
    def body(self):
        return self._request.splitlines()[-1]


class Response():
    def ok(self, mime_type=b'text/plain', body=b'Hello World'):
        return b'HTTP/1.1 200 OK\r\nContent-Type: ' + mime_type + b'\r\n\r\n' + body

    @property
    def not_found(self):
        return b'HTTP/1.1 404 Page Not Found\r\n\r\n404 Page Not Found'

    @property
    def method_not_allowed(self):
        return b"HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"


def check_request_method(request_method):
    avaliable_method = ['GET', 'POST']
    if request_method not in avaliable_method:
        raise NotImplementedError


def get_response_content(request_path):
    # strip remove front /
    file_path = os.path.join(os.getcwd(), "webroot", request_path.strip('/'))
    if os.path.isfile(file_path) or os.path.isfile(file_path + '/index.html'):
        with open(file_path, 'rb') as fp:
            content = fp.read()
        mime_type = mimetypes.guess_type(file_path)[0].encode()
        return mime_type, content
    else:
        # file not found
        raise NameError


def HTTP_request_handler(request):
    _request = Request(request)
    _response = Response()
    # print(_request.method)
    # print(_request.path)
    try:
        check_request_method(_request.method)
        if _request.method == "GET":
            mime_type, content = get_response_content(_request.path)
            return _response.ok(mime_type, content)
        elif _request.method == "POST":
            # print HTTP request body
            print(_request.body)
            return _response.ok(b'text/plain', b'Data Received')
    except NotImplementedError:
        return _response.method_not_allowed
    except NameError:
        return _response.not_found
    except:
        traceback.print_exc()

    return _response.not_found
