from peakselsdk.dr.DetectorRun import FloatRange
from peakselsdk.signal.Floats import FloatPoint

class WaveLength:
    def __init__(self, nm: int, precision: int):
        self.nm: int = nm
        self.precision: int = precision

class ExtractedWaveLength:
    def __init__(self, extracted: WaveLength, reference: WaveLength | None):
        self.extracted: WaveLength = extracted
        self.reference: WaveLength | None = reference

    @staticmethod
    def from_json(json: dict) -> "ExtractedWaveLength":
        ref: WaveLength | None = None
        jsonRefWl = json["refWl"]
        if jsonRefWl and jsonRefWl != 0:
            ref = WaveLength(jsonRefWl, json["refWlPrecision"])
        return ExtractedWaveLength(WaveLength(json["wl"], json["precision"]), ref)


class Chrom:
    def __init__(self, chromatogramId: str, name: str | None, domainId: str | None, signalId: str | None,
                 detectorId: str | None, substanceId: str | None, totalSignal: bool | None,
                 wavelength: ExtractedWaveLength | None, maxSignalIntensity: float | None, minSignalIntensity: float | None,
                 massRange: list[FloatRange] | None, baselineAnchors: list[FloatPoint] | None, **kwargs):
        self.eid: str = chromatogramId
        self.name: str = name
        self.domainId: str = domainId
        self.signalId: str = signalId
        self.detectorId: str = detectorId
        self.substanceId: str | None = substanceId
        self.totalSignal: bool = totalSignal
        self.wavelength: ExtractedWaveLength | None = wavelength # For UV only
        self.maxSignalIntensity: float = maxSignalIntensity
        self.minSignalIntensity: float = minSignalIntensity
        self.massRange: list[FloatRange] | None = massRange # for MS only
        self.baselineAnchors: list[FloatPoint] = baselineAnchors

    @staticmethod
    def from_json(json: dict) -> "Chrom":
        result: Chrom = Chrom(**json)
        if json["wavelength"]:
            result.wavelength = ExtractedWaveLength.from_json(json["wavelength"])
        if json["massRange"]:
            result.massRange = FloatRange.from_jsons(json["massRange"])
        result.baselineAnchors = FloatPoint.from_jsons(json["baselineAnchors"])
        return result

    @staticmethod
    def from_jsons(jsons: list[dict]) -> list["Chrom"]:
        chroms: list[Chrom] = []
        for dr in jsons:
            chroms.append(Chrom.from_json(dr))
        return chroms


class ChromList(list[Chrom]):
    pass