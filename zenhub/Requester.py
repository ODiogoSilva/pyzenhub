import json

import requests
from urllib.parse import urlparse, parse_qsl, urlencode, urlunsplit

from . import Constants


class RequestsResponse:
    # mimic the httplib response object
    def __init__(self, r):
        self.status = r.status_code
        self.headers = r.headers
        self.text = r.text

    def getheaders(self):
        return dict(self.headers).items()

    def read(self):
        return self.text


class HttpsRequestSession:
    def __init__(self, host, port):
        self.port = port if port else 443
        self.host = host
        self.protocol = "https"

        self.verb = None
        self.url = None
        self.input = None
        self.headers = None

        self.session = requests.Session()

    def request(self, verb, url, headers):
        self.verb = verb
        self.url = url
        self.headers = headers

    def getResponse(self):
        verb = getattr(self.session, self.verb.lower())
        url = f"{self.protocol}://{self.host}:{self.port}{self.url}"
        r = verb(
            url,
            headers=self.headers
        )
        return RequestsResponse(r)


class Requester:
    def __init__(self, token: str, baseUrl: str):
        self.__authorizationHeader = token
        self.__contentType = Constants.HEADER_CONTENT_TYPE
        self.__baseUrl = baseUrl

        parsedUrl = urlparse(self.__baseUrl)
        self.__hostname = parsedUrl.hostname
        self.__port = parsedUrl.port
        self.__prefix = parsedUrl.path

    def requestJsonAndCheck(self, verb, requestUrl, parameters=None, headers=None):
        # TODO: Make a request and check the status of the response.
        return self.__checkResponse(*self.__makeRequest(verb, requestUrl, parameters, headers))

    def __checkResponse(self, status, headers, response):
        # TODO: actually handle status to create exceptions here.
        output = self.__structuredFromJson(response)
        return headers, output

    def __structuredFromJson(self, data):
        if len(data) == 0:
            return None
        else:
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            try:
                return json.loads(data)
            except ValueError:
                return {"data": data}

    def __makeRequest(self, verb, requestUrl, parameters=None, headers=None):
        assert verb in Constants.VALID_HTTP_VERBS
        parameters = parameters if parameters is not None else dict()
        headers = headers if headers is not None else dict()

        self.__injectRequestHeaders(headers)
        requestUrl = self.__buildRequestUrl(requestUrl, parameters)

        return self.__getResponse(verb, requestUrl, headers)

    def __injectRequestHeaders(self, headers):
        self.__authenticate(headers)
        self.__setContentType(headers)

    def __authenticate(self, requestHeaders):
        requestHeaders["X-Authentication-Token"] = self.__authorizationHeader

    def __setContentType(self, requestHeaders):
        requestHeaders["Content-Type"] = self.__contentType

    def __buildRequestUrl(self, url, parameters):
        url = self.__buildFullUrlPath(url)
        return self.__addParametersToUrl(url, parameters)

    def __buildFullUrlPath(self, url):
        return self.__prefix + url

    @staticmethod
    def __addParametersToUrl(url, parameters):
        # TODO
        return url

    def __getResponse(self, verb, url, headers):
        connection = self.__getConnectionHandle()
        connection.request(verb, url, headers)
        response = connection.getResponse()

        status = response.status
        responseHeaders = dict((k.lower(), v) for k, v in response.getheaders())
        responseOutput = response.read()

        return status, responseHeaders, responseOutput

    def __getConnectionHandle(self):
        return HttpsRequestSession(self.__hostname, self.__port)
