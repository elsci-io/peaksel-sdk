from elsci.peakselsdk.Account import AccountType


class Org:
    displayName: str

    def __init__(self, displayName: str):
        self.displayName = displayName

    @staticmethod
    def from_json(json: dict) -> "Org":
        return Org(**json)

class OrgWithId(Org):
    id: str
    name: str
    type: AccountType

    def __init__(self, id: str, name: str, type: AccountType, displayName: str):
        super().__init__(displayName)
        self.id = id
        self.name = name
        self.type = type

    @staticmethod
    def from_json(json: dict) -> "OrgWithId":
        return OrgWithId(**json)