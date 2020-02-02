import zenhub.BaseZenhub


class Workspaces(zenhub.BaseZenhub.BaseZenhub):
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def id(self):
        return self._id

    @property
    def repositories(self):
        return self._repositories

    def get_board(self):
        url = f"/p2/workspaces/{self._id}/repositories/{self._repositoryId}/board"
        [_, responseJson] = self._requester.requestJsonAndCheck('GET', url)
        return responseJson

    def _initAttributes(self):
        self._name = zenhub.BaseZenhub.NotSet
        self._description = zenhub.BaseZenhub.NotSet
        self._id = zenhub.BaseZenhub.NotSet
        self._repositories = zenhub.BaseZenhub.NotSet

    def _useAttributes(self, attributes):
        if "name" in attributes:
            self._name = attributes["name"]
        if "description" in attributes:
            self._description = attributes["description"]
        if "id" in attributes:
            self._id = attributes["id"]
        if "repositories" in attributes:
            self._repositories = attributes["repositories"]
