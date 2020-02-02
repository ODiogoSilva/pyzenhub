from zenhub.Requester import Requester
from . import (
    Epic,
    Issue,
    Workspaces,
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
        return [Epic.Epic(self.__requester, responseHeaders, x, self._repositoryId) for x in epics]

    def get_issue(self, issue_number):
        url = f"/p1/repositories/{self._repositoryId}/issues/{issue_number}"
        [responseHeaders, responseJson] = self.__requester.requestJsonAndCheck('GET', url)
        return Issue.Issue(issue_number, self.__requester, responseHeaders, responseJson, self._repositoryId)

    def get_issue_events(self, issue_number):
        url = f"/p1/repositories/{self._repositoryId}/issues/{issue_number}/events"
        [_, responseJson] = self.__requester.requestJsonAndCheck('GET', url)
        return responseJson

    def get_workspaces(self):
        url = f"/p2/repositories/{self._repositoryId}/workspaces"
        [responseHeaders, workspaces] = self.__requester.requestJsonAndCheck('GET', url)
        return [
            Workspaces.Workspaces(
                self.__requester, responseHeaders, workspace, self._repositoryId
            ) for workspace in workspaces
        ]

    def get_board(self, workspaceId):
        url = f"/p2/workspaces/{workspaceId}/repositories/{self._repositoryId}/board"
        [_, responseJson] = self.__requester.requestJsonAndCheck('GET', url)
        return responseJson

    def get_oldest_board(self):
        url = f"/p1/repositories/{self._repositoryId}/board"
        [_, responseJson] = self.__requester.requestJsonAndCheck('GET', url)
        return responseJson
