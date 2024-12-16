from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.blob.Spectrum import Spectrum
from elsci.peakselsdk.blob.blobs import bytes_to_floats_le


class BlobClient:
    def __init__(self, settings: HttpClient):
        self.http: HttpClient = settings

    def get_detector_run_domain(self, blob_id: str) -> tuple[float,...]:
        return self.get_1d_floats(blob_id)

    def get_spectra(self, blob_id: str) -> list[Spectrum]:
        return Spectrum.from_bytes(self.get_blob(blob_id))

    def get_1d_floats(self, blob_id: str) -> tuple[float,...]:
        return bytes_to_floats_le(self.get_blob(blob_id))

    def get_blob(self, blob_id: str) -> bytes:
        return self.http.get_bytes(f"/api/blob/{blob_id}", headers={"Accept": "application/octet-stream"})