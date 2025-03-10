import base64

from peakselsdk.HttpClient import HttpClient
from peakselsdk.blob.blobs import floats_to_bytes_be


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
