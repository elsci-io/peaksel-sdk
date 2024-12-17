from peakselsdk.HttpClient import HttpClient
from peakselsdk.substance.Substance import SubstanceChem


class SubstanceClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self.http: HttpClient = settings
        self.org_id: str = org_id

    def add(self, inj_id: str, substance: SubstanceChem):
        self.http.post(f"/api/substance?injectionId={inj_id}", {
            "substance": substance.to_json_fields(),
            "ionModeToExtractionProps": {}
        })

