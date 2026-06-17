import json

from peakselsdk.HttpClient import HttpClient
from peakselsdk.substance.Substance import SubstanceChem, Analyte


class SubstanceClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self.http: HttpClient = settings
        self.org_id: str = org_id

    def add(self, inj_id: str, substance: SubstanceChem):
        self.http.post(f"/api/substance?injectionId={inj_id}", {
            "substance": substance.to_json_fields(),
            "chromExtractionSettings": []
        })

    def add_analyte(self, inj_id: str, analyte: Analyte) -> str:
        if analyte.structure:
            created_struct = json.loads(self.http.put("/api/substance/create-structure", analyte.structure.encode("utf-8"),
                                  headers={'Content-Type': 'application/octet-stream',
                                           "Accept": "application/json"}))[0]
            sub = SubstanceChem(alias=analyte.alias, structureId=created_struct["structureId"])
        else:
            sub = SubstanceChem(alias=analyte.alias, mf=analyte.mf)

        substance_id = self.http.post(f"/api/substance?injectionId={inj_id}",
                             {"substance": sub.to_json_fields(), "chromExtractionSettings": []})["substance"]["id"]
        return substance_id
