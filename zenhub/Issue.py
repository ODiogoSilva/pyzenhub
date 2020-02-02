import zenhub.BaseZenhub


class Issue(zenhub.BaseZenhub.BaseZenhub):
    def __init__(self, issueNumber, requester, headers, attributes, repositoryId):
        super().__init__(requester, headers, attributes, repositoryId)
        self._issueNumber = issueNumber

    @property
    def issue_number(self):
        return self._issueNumber

    @property
    def estimate(self):
        return self._estimate

    @property
    def plus_ones(self):
        return self._plus_ones

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def pipelines(self):
        return self._pipelines

    @property
    def is_epic(self):
        return self._is_epic

    def get_events(self):
        url = f"/p1/repositories/{self._repositoryId}/issues/{self.issue_number}/events"
        [_, responseJson] = self._requester.requestJsonAndCheck('GET', url)
        return responseJson

    def move_issue_to_pipeline(self):
        # TODO: First implement workspace endpoints.
        pass

    def move_issue_to_pipeline_in_oldest_workspace(self):
        # TODO: First implement workspace endpoints.
        pass

    def set_estimate(self, estimate):
        url = f"/p1/repositories/{self._repositoryId}/issues/{self.issue_number}/estimate"
        [_, response] = self._requester.requestJsonAndCheck('PUT', url, json={"estimate": estimate})
        return response

    def _initAttributes(self):
        self._estimate = zenhub.BaseZenhub.NotSet
        self._plus_ones = zenhub.BaseZenhub.NotSet
        self._pipeline = zenhub.BaseZenhub.NotSet
        self._pipelines = zenhub.BaseZenhub.NotSet
        self._is_epic = zenhub.BaseZenhub.NotSet

    def _useAttributes(self, attributes):
        if "estimate" in attributes:
            self._estimate = attributes["estimate"]
        if "plus_ones" in attributes:
            self._plus_ones = attributes["plus_ones"]
        if "pipeline" in attributes:
            self._pipeline = attributes["pipeline"]
        if "pipelines" in attributes:
            self._pipelines = attributes["pipelines"]
        if "is_epic" in attributes:
            self._is_epic = attributes["is_epic"]