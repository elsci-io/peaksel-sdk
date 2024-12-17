from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.org.Org import OrgShort


class OrgClient:
    http: HttpClient
    org_id: str

    def __init__(self, settings: HttpClient, org_id: str):
        self.http = settings
        self.org_id = org_id

    def create(self, name: str) -> OrgShort:
        resp = self.http.post(f"/api/org", body={"displayName": name})
        return OrgShort.from_json(resp)

    def get_by_name(self, name: str) -> OrgShort:
        return OrgShort.from_json(self.http.get_json(f"/api/org?name={name}"))