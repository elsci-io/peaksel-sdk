from elsci.peakselsdk.HttpClient import HttpClient


class BatchClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self.http: HttpClient = settings
        self.org_id: str = org_id

    def assign_injections(self, injection_ids: list[str], batch_id: str = None, batch_name: str = None) -> str:
        return self.http.put("/api/batch/reassign",
                             {"injections": injection_ids, "batchId": batch_id, "batchName": batch_name}).decode("utf-8")