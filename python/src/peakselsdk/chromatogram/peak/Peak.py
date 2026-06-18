import json
import struct
from dataclasses import dataclass


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
    def by_chromatogram(self, chromatogram_id: str) -> list[Peak]:
        return [peak for peak in self if peak.chromatogramId == chromatogram_id]


class UnknownPeak:
    def __init__(self, **kwargs):
        self.start_minutes: float = kwargs["start_minutes"]
        self.rt_minutes: float = kwargs["rt_minutes"]
        self.end_minutes: float = kwargs["end_minutes"]
        self.base: float = kwargs["base"]
        self.area: float = kwargs["area"]
        self.area_perc: float = kwargs["area_perc"]
        self.rt_idx: int | None = kwargs["rt_idx"]
        self.start_idx: int = kwargs["start_idx"]
        self.end_idx: int = kwargs["end_idx"]
        self.participates_in_chrom_area: bool = kwargs["participates_in_chrom_area"]

    @staticmethod
    def decode(data: bytes):
        schema_ver = data[0]
        if schema_ver == 0:
            return UnknownPeak._decode_detected(data)
        elif schema_ver == 1:
            return UnknownPeak._decode_top_unknowns(data)
        else:
            raise ValueError(f"Unknown schema version: {schema_ver}")

    @staticmethod
    def _decode_detected(data: bytes) -> list[UnknownPeak]:
        schema_fmt = ">6f4i"
        schema_size = struct.calcsize(schema_fmt)
        payload = data[1:]
        peaks = []
        for i in range(0, len(payload), schema_size):
            chunk = payload[i:i + schema_size]
            values = struct.unpack(schema_fmt, chunk)
            peaks.append(UnknownPeak(
                start_minutes=values[0],
                rt_minutes=values[1],
                end_minutes=values[2],
                base=values[3],
                area=values[4],
                area_perc=values[5],
                start_idx=values[6],
                rt_idx=values[7],
                end_idx=values[8],
                participates_in_chrom_area=values[9] == 1,
            ))
        return peaks

    @staticmethod
    def _decode_top_unknowns(data: bytes) -> list[UnknownPeak]:
        schema_fmt = ">6f"
        schema_size = struct.calcsize(schema_fmt)
        payload = data[1:]
        peaks = []
        for i in range(0, len(payload), schema_size):
            chunk = payload[i:i + schema_size]
            values = struct.unpack(schema_fmt, chunk)
            peaks.append(UnknownPeak(
                start_minutes=values[0],
                rt_minutes=values[1],
                end_minutes=values[2],
                base=values[3],
                area=values[4],
                area_perc=values[5],
            ))
        return peaks
