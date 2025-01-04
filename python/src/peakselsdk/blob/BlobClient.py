from peakselsdk.HttpClient import HttpClient
from peakselsdk.blob.Floats2d import Floats2d
from peakselsdk.blob.Spectrum import Spectrum
from peakselsdk.blob.blobs import bytes_to_floats_le


class BlobClient:
    def __init__(self, settings: HttpClient):
        self.http: HttpClient = settings

    def get_chrom_signal(self, blob_id: str) -> tuple[float,...]:
        """
        Gets the intensities of the points on a chromatogram. Note, that the time-axis is kept in the DetectorRun
        and is shared across all chromatograms in that run, use `get_detector_run_domain(another_blob_id)` to get it.

        :param blob_id: is taken from `Chromatogram.eid`
        :return: intensities of the chromatogram points
        """
        return self._get_1d_floats(blob_id)

    def get_detector_run_domain(self, blob_id: str) -> tuple[float,...]:
        """
        Returns the time-axis for this run, it's shared across all chromatograms of this detector.
        :param blob_id: `DetectorRun.eid`
        :return:
        """
        return self._get_1d_floats(blob_id)

    def get_spectra(self, blob_id: str) -> list[Spectrum]:
        return Spectrum.from_bytes(self.get_blob(blob_id))

    def get_peak_spectrum(self, blob_id: str) -> Floats2d:
        return self._get_2d_floats(blob_id)

    def get_blob(self, blob_id: str, little_endian = False) -> bytes:
        if not blob_id:
            raise Exception(f"You must pass a blob ID, got: {blob_id}")
        # Little Endian flag is passed for forward compatibility when we fix the endianness of signals and baseline
        return self.http.get_bytes(f"/api/blob/{blob_id}?littleEndianWords={little_endian}",
                                   headers={"Accept": "application/octet-stream"})

    def _get_1d_floats(self, blob_id: str) -> tuple[float,...]:
        return bytes_to_floats_le(self.get_blob(blob_id, little_endian=True))

    def _get_2d_floats(self, blob_id: str) -> Floats2d:
        data = self.get_blob(blob_id, little_endian=True)
        half_len = (len(data)-4) // 2 # first 4 bytes is the length
        x: tuple[float,...] = bytes_to_floats_le(data, 4, len_bytes=half_len)
        y: tuple[float,...] = bytes_to_floats_le(data, 4+half_len)
        return Floats2d(x, y)
