from zenhub.Requester import Requester
from . import (
    Epic,
    Constants
)


class Zenhub:
    def __init__(self, token: str, repositoryId: str, baseUrl=None):
        assert token is not None

        if baseUrl is None:
            baseUrl = Constants.PUBLIC_BASE_URL
        self._baseUrl = baseUrl

        self.__requester = Requester(token, baseUrl)
        self._repositoryId = repositoryId

    def get_epics(self):
        url = f"/p1/repositories/{self._repositoryId}/epics"
        [responseHeaders, responseJson] = self.__requester.requestJsonAndCheck('GET', url)
        epics = responseJson["epic_issues"]
        return [Epic.Epic(self.__requester, responseHeaders, x) for x in epics]
