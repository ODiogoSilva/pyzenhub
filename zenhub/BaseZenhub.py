class _NotSetType:
    def __repr__(self):
        return "NotSet"

    value = None


NotSet = _NotSetType()


class BaseZenhub:
    def __init__(self, requester, headers, attributes):
        self._requester = requester

        self._initAttributes()
        self._storeAndUseAttributes(headers, attributes)

    def _storeAndUseAttributes(self, headers, attributes):
        self._headers = headers
        self._rawAttributes = attributes
        self._useAtttributes(attributes)
