import base64
import json

from peakselsdk.chromatogram.Chrom import Chrom, ChromList
from peakselsdk.chromatogram.peak.Peak import PeakList, Peak, UnknownPeak, UnknownPeakList
from peakselsdk.dr.DetectorRun import DetectorRun, DetectorRunList
from peakselsdk.plate.Plate import PlateLocation
from peakselsdk.substance.Substance import Substance
from peakselsdk.user.User import User


class InjectionShort:
    def __init__(self: str, id: str, name: str, plateId: str, instrumentName: str, methodName: str,
                 plateLocation: PlateLocation = None, creator: User = None, **kwargs):
        self.eid: str = id
        self.name: str | None = name
        self.plateId: str = plateId
        self.instrumentName: str | None = instrumentName
        self.methodName: str | None = methodName
        self.plateLocation: PlateLocation = plateLocation
        self.creator: User | None = creator
        """ Creator is None if the injection was uploaded by crawler, not by user """

    @staticmethod
    def from_json(json: dict) -> "InjectionShort":
        result = InjectionShort(**json)
        if json["creator"]:
            result.creator = User.from_json(json["creator"])
        result.plateLocation = PlateLocation(int(json["row"]), int(json["col"]))
        return result

    @staticmethod
    def from_jsons(jsons: list[dict]) -> "list[InjectionShort]":
        result: list[InjectionShort] = []
        for json in jsons:
            result.append(InjectionShort.from_json(json))
        return result

    def __str__(self) -> str:
        return json.dumps(self, default=vars)

class InjectionFull(InjectionShort):
    def __init__(self, meta: InjectionShort, batchId: str | None = None, **kwargs):
        self.__dict__.update(meta.__dict__)
        self.batchId: str | None = batchId
        self.substances: list[Substance] = Substance.from_jsons(kwargs["substances"])
        self.detectorRuns: DetectorRunList = DetectorRunList(DetectorRun.from_jsons(kwargs["detectorRuns"]))
        self.chromatograms: ChromList[Chrom] = ChromList(Chrom.from_jsons(kwargs["chromatograms"]))
        self.peaks: PeakList[Peak] = PeakList(Peak.from_jsons(kwargs["peaks"]))
        self.userDefinedProps: dict[str, any] = kwargs["userDefinedProps"] or dict()
        self._unknown_peaks: UnknownPeakList[UnknownPeak] | None = None

    def unknown_peaks(self) -> UnknownPeakList[UnknownPeak]:
        if self._unknown_peaks is None:
            result = []
            for c in self.chromatograms:
                if c.base64_encoded_detected_peaks is None: continue
                detected_peaks = UnknownPeak.decode(base64.b64decode(c.base64_encoded_detected_peaks))
                peaks = self.peaks.by_chromatogram(c.eid)
                # Filter out peaks that are already selected
                for detected_peak in detected_peaks:
                    matched_peak = next((peak for peak in peaks if peak.rtIdx == detected_peak.rt_idx), None)
                    if not matched_peak:
                        detected_peak.chromatogram_id = c.eid
                        result.append(detected_peak)
            self._unknown_peaks = UnknownPeakList(result)
        else:
            self._unknown_peaks = UnknownPeakList([])
        return self._unknown_peaks

    @staticmethod
    def from_json(json: dict) -> "InjectionFull":
        return InjectionFull(InjectionShort.from_json(json), **json)
