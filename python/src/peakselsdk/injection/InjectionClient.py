from typing import Any

from peakselsdk.HttpClient import HttpClient
from peakselsdk.injection.Injection import InjectionFull, InjectionShort


class InjectionClient:
    def __init__(self, settings: HttpClient, org_id: str):
        self.http: HttpClient = settings
        self.org_id: str = org_id

    def upload(self, filepath: str) -> list[str]:
        """
        Uploads a ZIP with raw data inside.
        :param filepath: local path to the ZIP file with the raw data inside
        :return: list of IDs of the successfully uploaded injections
        """
        # passing orgId in the URL because urllib3 doesn't like mixing octet/binary-stream and params -
        # seems like it just doesn't pass them or passes them encoded in the body
        resp = self.http.upload(f"/api/injection?orgId={self.org_id}", filepath)
        success_injection_ids = resp['successInjectionIds']
        last_error: str = resp["lastError"]
        if last_error:
            raise Exception(f"Not all injections were created successfully:"
                            f"\n successfully created: {success_injection_ids}"
                            f"\n last error: {last_error}")
        return success_injection_ids

    def list_orphan(self, name_starting_with: str = None, page: int = 0) -> list[InjectionShort]:
        """
        List injections that aren't assigned to any batch.
        :param name_starting_with: empty or None if no search by name is needed. Search is case-insensitive.
        :param page: if you want to get more than 50 results, you can specify the page number. The first page is 0.
                     To go through all injections, keep calling this method until it returns an empty list.
        :return: Injections sorted by upload date (newest first)

        ## Example

        ```python

        for page in range(100):
            list = peaksel.injections().list_orphan(page=page)
            for inj in list:
                print(f"{inj.eid} {inj.name}")
            else:
                break
        ```
        """
        name = name_starting_with or ""
        offset = (page or 0) * 50
        resp = self.http.get_json(f"/api/query/ORPHAN_INJECTIONS?orgId={self.org_id}&name={name}&offset={offset}&checkAcl=true")
        return InjectionShort.from_jsons(resp["content"])

    def list_in_batch(self, batch_id: str) -> list[InjectionShort]:
        return InjectionShort.from_jsons(self.http.get_json(f"/api/batch/{batch_id}/injections")["injections"])

    def get(self, inj_id) -> InjectionFull:
        return InjectionFull.from_json(self.http.get_json(f"/api/injection/{inj_id}"))

    def set_props(self, injection_id: str, props: dict[str, Any]) -> None:
        """
        You can associate your own key-value properties with the injections - calculations, labels, etc.

        :param injection_id: the injection to update
        :param props: custom properties that are turned into a JSON. The previous custom props will be completely
                      overritten if they existed. Note, that there can be a limit to how much data can be stored in
                      these props.
        """
        self.http.put(f"/api/injection/{injection_id}/props/userdefined", props)

    def assign_to_batch(self, injection_ids: list[str], batch_id: str = None, batch_name: str = None) -> str:
        return self.http.put("/api/batch/reassign",
                             {"injections": injection_ids, "batchId": batch_id, "batchName": batch_name}).decode("utf-8")
