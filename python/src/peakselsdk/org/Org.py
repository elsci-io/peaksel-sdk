from peakselsdk.Account import AccountType


class OrgTiny:
    displayName: str

    def __init__(self, displayName: str, **kwargs):
        self.displayName = displayName

    @staticmethod
    def from_json(json: dict) -> "OrgTiny":
        return OrgTiny(**json)

class OrgShort(OrgTiny):
    id: str
    name: str
    type: AccountType

    def __init__(self, id: str, name: str, type: AccountType, org: OrgTiny, **kwargs):
        self.__dict__.update(org.__dict__)
        self.id = id
        self.name = name
        self.type = type

    @staticmethod
    def from_json(json: dict) -> "OrgShort":
        return OrgShort(org=OrgTiny.from_json(json), **json)