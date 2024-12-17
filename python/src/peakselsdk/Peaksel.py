from peakselsdk.HttpClient import HttpClient
from peakselsdk.batch.BatchClient import BatchClient
from peakselsdk.blob.BlobClient import BlobClient
from peakselsdk.chromatogram.peak.PeakClient import PeakClient
from peakselsdk.injection.InjectionClient import InjectionClient
from peakselsdk.org.OrgClient import OrgClient
from peakselsdk.substance.SubstanceClient import SubstanceClient


class Peaksel:
    http_client: HttpClient
    org_id: str | None

    def __init__(self, base_url: str, org_name: str = None, org_id: str = None, default_headers: dict[str:str] = None):
        """
        :param base_url: e.g. https://peaksel.elsci.io
        :param org_name: the unique name of the org (can be taken from the URL in Peaksel). Ideally you should pass
                         `org_id` instead, but if you don't know it - the SDK will figure out the ID by the name.
        :param org_id: id of the org in which scope you're going to work. You can pass this or hte `org_name`
        :param default_headers: these HTTP headers will be added to every request
        """
        self.http_client = HttpClient(base_url, default_headers)
        if not org_id and not org_name:
            raise Exception("Either org_id or org_name must be passed to Peaksel constructor. Name can be taken "
                            "from the URL in Peaksel app.")
        self.org_id: str = org_id or self.orgs().get_by_name(org_name).id

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
        return OrgClient(self.http_client)

    def _org_id(self) -> str:
        if self.org_id is None:
            raise Exception("Before calling endpoints that require organization (almost all endpoints do), you "
                            "must set org_id in Peaksel class")
        return self.org_id