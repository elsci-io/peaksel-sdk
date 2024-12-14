import json

from elsci.peakselsdk.dr.DetectorRun import DetectorRun
from elsci.peakselsdk.plate.Plate import PlateLocation
from elsci.peakselsdk.substance.Substance import SubstanceChem, Substance
from elsci.peakselsdk.user.User import User


class InjectionMeta:
    def __init__(self: str, id: str, name: str, plateId: str, instrumentName: str, methodName: str,
                 plateLocation: PlateLocation = None, creator: User = None, **kwargs):
        self.eid: str = id
        self.name: str | None = name
        self.plateId: str = plateId
        self.instrumentName: str | None = instrumentName
        self.methodName: str | None = methodName
        self.plateLocation: PlateLocation = plateLocation
        self.creator: User = creator

    @staticmethod
    def from_json(json: dict) -> "InjectionMeta":
        result = InjectionMeta(**json)
        result.creator = User.from_json(json["creator"])
        result.plateLocation = PlateLocation(int(json["row"]), int(json["col"]))
        return result

    def __str__(self) -> str:
        return json.dumps(self, default=vars)

class FullInjection(InjectionMeta):
    def __init__(self, meta: InjectionMeta, batchId: str| None = None, **kwargs):
        self.__dict__.update(meta.__dict__)
        self.batchId: str | None = batchId
        self.substances: list[Substance] = []
        self.detectorRuns: list[DetectorRun] = []
        for s in kwargs["substances"]:
            self.substances.append(Substance.from_json(s))
        for dr in kwargs["detectorRuns"]:
            self.detectorRuns.append(DetectorRun.from_json(dr))

    @staticmethod
    def from_json(json: dict) -> "FullInjection":
        return FullInjection(InjectionMeta.from_json(json), **json)

