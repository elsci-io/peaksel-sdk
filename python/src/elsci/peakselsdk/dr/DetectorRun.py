import json
from enum import EnumType

from elsci.peakselsdk.signal.Range import FloatRange


class SpectrumCompression(EnumType): # this enum won't be changed in the future, so we can use it in DTOs
    CONTINUUM = "CONTINUUM"
    CENTROIDED = "CENTROIDED"

class AnalyticalMethod(EnumType): # values can change in the future, so we have to use plain strings in the DTOs for forward compatibility
    MS = "MS"
    UV = "UV"
    ELS = "ELS"
    RI = "RI"
    FI = "FI"

class DetectorType: # values can change in the future, so we have to use plain strings in the DTOs for forward compatibility
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

class IonMode: # values can change in the future, so we have to use plain strings in the DTOs for forward compatibility
    """
    P is positive, N is negative
    """

    # Electron Impact - knocks out or adds electrons.
    EIP = "EIP"; EIM = "EIM"
    # Chemical Ionisation (Positive) - adds H+ (or another atom) to ionize the analyte.
    CIP = "CIP"; CIM = "CIM"
    # Electrospray Ionisation- adds or removes H+ (or another atom) to ionize the analyte.
    ESP = "ESP"; ESM = "ESM"


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

    def has_spectra(self) -> bool:
        return self.spectrumCompression is not None

    def __str__(self):
        return json.dumps(self, default=vars)


