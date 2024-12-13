from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.injection.InjectionClient import InjectionClient
from elsci.peakselsdk.org.OrgClient import OrgClient


class Peaksel:
    _client_settings: HttpClient
    org_id: str | None

    def __init__(self, base_url: str, org_id: str = None, default_headers: dict[str:str] = None):
        """
        :param base_url: e.g. https://peaksel.elsci.io
        :param org_id: if you intend to work with injections or batches, this must be passed
        :param default_headers: these HTTP headers will be added to every request
        """
        self._client_settings = HttpClient(base_url, default_headers)
        self.org_id = org_id

    def injections(self) -> InjectionClient:
        return InjectionClient(self._client_settings, self._org_id())

    def orgs(self) -> OrgClient:
        return OrgClient(self._client_settings, self._org_id())

    def _org_id(self) -> str:
        if self.org_id is None:
            raise Exception("Before calling endpoints that require organization (almost all endpoints do), you "
                            "must set org_id in Peaksel class")
        return self.org_id