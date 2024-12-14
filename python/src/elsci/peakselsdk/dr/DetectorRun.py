import json
from enum import EnumType

from elsci.peakselsdk.signal.Range import FloatRange


class SpectrumCompression(EnumType):
    CONTINUUM = "CONTINUUM"
    CENTROIDED = "CENTROIDED"

class AnalyticalMethod(EnumType):
    MS = "MS"
    UV = "UV"
    ELS = "ELS"
    RI = "RI"
    FI = "FI"

class DetectorType:
    MS = "MS"
    SIM = "SIM"
    TQD_SIM = "TQD_SIM"
    TQD_SCAN = "TQD_SCAN"
    SRM = "SRM"
    TOF = "TOF"
    QTOF_SCAN = "QTOF_SCAN"
    QTOF_PROD_SCAN = "QTOF_PROD_SCAN"
    QTOF_PREC_SCAN = "QTOF_PREC_SCAN"
    UV = "UV"
    ELS = "ELS"
    RI = "RI"
    FI = "FI"


class DetectorRun:
    def __init__(self, id: str, description: str | None, units: str, seqNum: int | None, domainBlobId: str,
                 spectrumCompression: SpectrumCompression | None, analyticalMethod: str, detectorType: str,
                 ionMode: str | None, scanWindow: FloatRange | None, alignMin: float, **kwargs):
        self.eid: str = id
        self.description: str | None = description
        self.units: str = units
        self.seqNum: int | None = seqNum
        self.domainBlobId: str = domainBlobId
        self.spectrumCompression: SpectrumCompression | None = spectrumCompression
        self.analyticalMethod: str = analyticalMethod
        self.detectorType: str = detectorType
        self.ionMode: str | None = ionMode
        self.scanWindow: FloatRange | None = scanWindow
        self.alignMin: float = alignMin

    @staticmethod
    def from_json(json: dict) -> "DetectorRun":
        result = DetectorRun(**json)
        result.scanWindow = FloatRange.from_json(json["scanWindow"])
        return result

    def __str__(self):
        return json.dumps(self, default=vars)


