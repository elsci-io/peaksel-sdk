import base64
from urllib.parse import urlencode

from peakselsdk.HttpClient import HttpClient
from peakselsdk.blob.blobs import floats_to_bytes_be
from peakselsdk.chromatogram.Chrom import ExtractedWaveLength
from peakselsdk.injection.InjectionClient import InjectionClient


class ChromClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self._http: HttpClient = settings
        self._org_id: str = org_id

    def add_chromatogram(self, injection_id: str, chrom_name: str, x: list[float], y: list[float]) -> None:
        if len(x) != len(y):
            raise ValueError(f"Number of values in x-axis ({len(x)}) isn't the same as in y-axis ({len(y)} ")
        if not chrom_name:
            raise ValueError("Chromatogram name must not be blank: " + chrom_name)
        self._http.post(f"/api/chromatogram", {
            "injectionId": injection_id,
            "name": chrom_name,
            "signalBase64": base64.b64encode(floats_to_bytes_be(y)).decode("ascii"),
            "domainBase64": base64.b64encode(floats_to_bytes_be(x)).decode("ascii"),
        })

    def add_wavelength_to_batch(self, batch_id: str, wavelength: ExtractedWaveLength) -> None:
        """
        For each injection in the batch that has DAD/PDA spectra extracts wavelength chromatogram.
        To get the results, fetch the injections and use
        `injection.chromatograms.filter_by_wavelength()`.

        :param batch_id:
        :param wavelength: e.g. `ExtractedWaveLength(WaveLength(254, 2))`: `254±2` sums 252..256 nm and divides by the
                           number of points. With a reference wavelength, its signal is subtracted from the extracted
                           signal: `ExtractedWaveLength(WaveLength(254, 2), WaveLength(360, 50))`.
        """
        injection_ids = [j.eid for j in InjectionClient(self._http, self._org_id).list_in_batch(batch_id)]
        self.add_wavelength(injection_ids, wavelength)

    def add_wavelength(self, injection_ids: list[str], wavelength: ExtractedWaveLength) -> None:
        """
        Same as `add_wavelength_to_batch()`, but for the given injections.
        """
        if not injection_ids:
            return
        # The IDs go in the URL: urllib3 puts `params` of a POST in the body
        query = urlencode({"injections": injection_ids}, doseq=True)
        self._http.post(f"/api/chromatogram/extracted?{query}", wavelength.to_json())
