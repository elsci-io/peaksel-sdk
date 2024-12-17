import json


class User:
    def __init__(self, id: str, name: str, firstname: str | None, lastname: str | None, **kwargs):
        self.eid: str = id
        self.name: str = name
        self.firstname: str | None = firstname
        self.lastname: str | None = lastname

    @staticmethod
    def from_json(json: dict) -> "User":
        return User(**json)

    def __str__(self) -> str:
        return json.dumps(self, default=vars)
