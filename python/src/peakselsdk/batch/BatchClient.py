import warnings

from peakselsdk.HttpClient import HttpClient
from peakselsdk.injection.Injection import InjectionShort


class BatchClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self.http: HttpClient = settings
        self.org_id: str = org_id

    def get_injections(self, id: str) -> list[InjectionShort]:
        warnings.warn("Calling deprecated method. Use InjectionClient.list_in_batch() instead.", DeprecationWarning)
        return InjectionShort.from_jsons(self.http.get_json(f"/api/batch/{id}/injections")["injections"])

    def assign_injections(self, injection_ids: list[str], batch_id: str = None, batch_name: str = None) -> str:
        warnings.warn("Calling deprecated method. Use InjectionClient.assign_to_batch() instead.", DeprecationWarning)
        return self.http.put("/api/batch/reassign",
                             {"injections": injection_ids, "batchId": batch_id, "batchName": batch_name}).decode("utf-8")