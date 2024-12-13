from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.org.Org import OrgWithId


class OrgClient:
    http: HttpClient
    org_id: str

    def __init__(self, settings: HttpClient, org_id: str):
        self.http = settings
        self.org_id = org_id

    def create(self, name: str) -> OrgWithId:
        resp = self.http.post(f"/api/org", body={"displayName": name})
        return OrgWithId.from_json(resp)
