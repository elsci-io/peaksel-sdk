from peakselsdk.HttpClient import HttpClient
from peakselsdk.blob.Floats2d import Floats2d
from peakselsdk.blob.Spectrum import Spectrum
from peakselsdk.blob.blobs import bytes_to_floats_le


class BlobClient:
    def __init__(self, settings: HttpClient):
        self.http: HttpClient = settings

    def get_detector_run_domain(self, blob_id: str) -> tuple[float,...]:
        return self._get_1d_floats(blob_id)

    def get_spectra(self, blob_id: str) -> list[Spectrum]:
        return Spectrum.from_bytes(self.get_blob(blob_id))

    def get_peak_spectrum(self, blob_id: str) -> Floats2d:
        return self._get_2d_floats(blob_id)

    def get_blob(self, blob_id: str) -> bytes:
        if not blob_id:
            raise Exception(f"You must pass a blob ID, got: {blob_id}")
        return self.http.get_bytes(f"/api/blob/{blob_id}", headers={"Accept": "application/octet-stream"})

    def _get_1d_floats(self, blob_id: str) -> tuple[float,...]:
        return bytes_to_floats_le(self.get_blob(blob_id))

    def _get_2d_floats(self, blob_id: str) -> Floats2d:
        data = self.get_blob(blob_id)
        half_len = (len(data)-4) // 2 # first 4 bytes is the length
        x: tuple[float,...] = bytes_to_floats_le(data, 4, len_bytes=half_len)
        y: tuple[float,...] = bytes_to_floats_le(data, 4+half_len)
        return Floats2d(x, y)
