import json
from enum import EnumType

from peakselsdk.signal.Range import FloatRange
from peakselsdk.util.dict_util import pass_if_defined


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

class DetectorRunBlobs:
    def __init__(self, domain: str, spectra: str = None, **kwards):
        self.domain: str = domain
        self.spectra: str | None = spectra

    @staticmethod
    def from_json(json: dict) -> "DetectorRunBlobs":
        return DetectorRunBlobs(**json)

    def __str__(self):
        return json.dumps(self, default=vars)

class DetectorRun:
    def __init__(self, id: str, description: str, units: str, seqNum: int | None, blobs: DetectorRunBlobs,
                 spectrumCompression: SpectrumCompression | None, analyticalMethod: str, detectorType: str,
                 ionMode: str | None, scanWindow: FloatRange | None, alignMin: float, **kwargs):
        self.eid: str = id
        self.description: str = description
        self.units: str = units
        self.seqNum: int | None = seqNum
        self.blobs: DetectorRunBlobs = blobs
        self.spectrumCompression: SpectrumCompression | None = spectrumCompression
        self.analyticalMethod: str = analyticalMethod
        self.detectorType: str = detectorType
        self.ionMode: str | None = ionMode
        self.scanWindow: FloatRange | None = scanWindow
        self.alignMin: float = alignMin

    @staticmethod
    def from_json(json: dict) -> "DetectorRun":
        result = DetectorRun(**json)
        result.scanWindow = pass_if_defined(json["scanWindow"], FloatRange.from_json)
        result.blobs = pass_if_defined(json["blobs"], DetectorRunBlobs.from_json)
        return result

    @staticmethod
    def from_jsons(jsons: list[dict]) -> list["DetectorRun"]:
        drs: list[DetectorRun] = []
        for dr in jsons:
            drs.append(DetectorRun.from_json(dr))
        return drs

    def has_spectra(self) -> bool:
        return self.blobs.spectra is not None

    def is_positive_ion_mode(self) -> bool:
        if self.analyticalMethod != AnalyticalMethod.MS:
            raise Exception(f"Requested Ion Mode from DetectorRun({self.eid}, {self.analyticalMethod}), but it's "
                            f"available only for Mass Spec runs.")
        return self.ionMode.endswith("P") # negative modes end with N


    def __str__(self):
        return json.dumps(self, default=vars)


class DetectorRunList(list[DetectorRun]): # implementing `list` and not just Iterable protocol, otherwise json.dumps() treats it as an object

    def get_by_id(self, eid: str) -> DetectorRun:
        for dr in self:
            if dr.eid == eid:
                return dr
        raise Exception("Couldn't find DetectorRun " + eid)

    def filter_by_type(self, detector_type: DetectorType) -> "DetectorRunList":
        return DetectorRunList([dr for dr in self if dr.detectorType == detector_type])
