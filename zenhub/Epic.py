import zenhub.BaseZenhub


class Epic(zenhub.BaseZenhub.BaseZenhub):
    @property
    def issue_number(self):
        return self._issueNumber

    @property
    def repo_id(self):
        return self._repoId

    @property
    def issue_url(self):
        return self._issueUrl

    def _initAttributes(self):
        self._issueNumber = zenhub.BaseZenhub.NotSet
        self._repoId = zenhub.BaseZenhub.NotSet
        self._issueUrl = zenhub.BaseZenhub.NotSet

    def _useAtttributes(self, attributes):
        if "issue_number" in attributes:
            self._issueNumber = attributes["issue_number"]

        if "repo_id" in attributes:
            self._repoId = attributes["repo_id"]

        if "issue_url" in attributes:
            self._issueUrl = attributes["issue_url"]