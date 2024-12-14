from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.injection.Injection import FullInjection


class InjectionClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self.http: HttpClient = settings
        self.org_id: str = org_id

    def upload(self, filepath: str) -> list[str]:
        # passing orgId in the URL because urllib3 doesn't like mixing octet/binary-stream and params -
        # seems like it just doesn't pass them or passes them encoded in the body
        resp = self.http.upload(f"/api/injection?orgId={self.org_id}", filepath)
        return resp['successInjectionIds']

    def get(self, inj_id) -> FullInjection:
        return FullInjection.from_json(self.http.get(f"/api/injection/{inj_id}"))