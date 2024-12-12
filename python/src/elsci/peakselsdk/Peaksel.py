from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.InjectionClient import InjectionClient


class Peaksel:
    _client_settings: HttpClient
    _org_id: str

    def __init__(self, base_url: str, org_id: str, default_headers: dict[str:str]):
        self._client_settings = HttpClient(base_url, default_headers)
        self._org_id = org_id

    def injections(self) -> InjectionClient:
        return InjectionClient(self._client_settings, self._org_id)