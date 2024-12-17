from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.batch.BatchClient import BatchClient
from elsci.peakselsdk.blob.BlobClient import BlobClient
from elsci.peakselsdk.chromatogram.peak.PeakClient import PeakClient
from elsci.peakselsdk.injection.InjectionClient import InjectionClient
from elsci.peakselsdk.org.OrgClient import OrgClient
from elsci.peakselsdk.substance.SubstanceClient import SubstanceClient


class Peaksel:
    http_client: HttpClient
    org_id: str | None

    def __init__(self, base_url: str, org_id: str = None, default_headers: dict[str:str] = None):
        """
        :param base_url: e.g. https://peaksel.elsci.io
        :param org_id: if you intend to work with injections or batches, this must be passed
        :param default_headers: these HTTP headers will be added to every request
        """
        self.http_client = HttpClient(base_url, default_headers)
        self.org_id = org_id

    def injections(self) -> InjectionClient:
        return InjectionClient(self.http_client, self._org_id())

    def batches(self) -> BatchClient:
        return BatchClient(self.http_client, self._org_id())

    def blobs(self) -> BlobClient:
        return BlobClient(self.http_client)

    def substances(self) -> SubstanceClient:
        return SubstanceClient(self.http_client, self.org_id)

    def peaks(self) -> PeakClient:
        return PeakClient(self.http_client)

    def orgs(self) -> OrgClient:
        return OrgClient(self.http_client, self._org_id())

    def _org_id(self) -> str:
        if self.org_id is None:
            raise Exception("Before calling endpoints that require organization (almost all endpoints do), you "
                            "must set org_id in Peaksel class")
        return self.org_id