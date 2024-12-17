from peakselsdk.HttpClient import HttpClient
from peakselsdk.chromatogram.peak.Peak import Peak, PeakList


class PeakClient:
    def __init__(self, settings: HttpClient):
        self.http: HttpClient = settings

    def add(self, inj_id: str, chrom_id: str, substance_id: str, start_idx: int, end_idx: int) -> PeakList:
        """
        :param start_idx: the index (inclusive) of the point where the peak starts on chromatogram
        :param end_idx: the index (inclusive) of the point where the peak ends on chromatogram
        :return: all peaks in the injection
        """
        return Peak.from_jsons(self.http.post(f"/api/peak?"
                                              f"injectionId={inj_id}&"
                                              f"chromatogramId={chrom_id}&"
                                              f"substanceId={substance_id}&"
                                              f"startIdx={start_idx}&"
                                              f"endIdx={end_idx}"))
