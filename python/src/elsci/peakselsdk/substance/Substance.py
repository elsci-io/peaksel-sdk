import json


class Substance:
    def __init__(self, id: str, emw: float, mf: str = None, color: str = None,
                 structureId: str = None, structureSvgPath: str = None,
                 alias: str = None, **kwargs):
        self.eid: str = id
        self.structureId: str | None = structureId
        self.color: str | None = color
        self.structureSvgPath: str | None = structureSvgPath
        self.alias: str | None = alias
        self.mf: str | None = mf
        self.emw: float = emw

    @staticmethod
    def from_json(json: dict) -> "Substance":
        return Substance(**json)

    def __str__(self):
        return json.dumps(self, default=vars)

