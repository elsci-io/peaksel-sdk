import json


class PeakBlobs:
    def __init__(self, spectrum: str = None, **kwargs):
        self.spectrum = spectrum

    @staticmethod
    def from_json(json: dict) -> "PeakBlobs":
        return PeakBlobs(**json)

class Peak:
    def __init__(self, id: str, area: float, areaPercent: float, rt: float, rtIdx: int, substanceId: str,
                 chromatogramId: str, indexRange: list[int], blobs: PeakBlobs, **kwards):
        self.eid: str = id
        self.area: float = area
        self.areaPercent: float = areaPercent
        self.rt: float = rt
        self.rtIdx: int = rtIdx
        self.substanceId: str = substanceId
        self.chromatogramId: str = chromatogramId
        self.indexRange: list[int] = indexRange
        self.blobs: PeakBlobs = blobs

    @staticmethod
    def from_json(json: dict) -> "Peak":
        result = Peak(**json)
        result.blobs = PeakBlobs.from_json(json["blobs"])
        return result

    @staticmethod
    def from_jsons(jsons: list[dict]) -> "PeakList":
        result: PeakList = PeakList()
        for json in jsons:
            result.append(Peak.from_json(json))
        return result

    def __str__(self) -> str:
        return json.dumps(self, default=vars)

class PeakList(list[Peak]):
    pass