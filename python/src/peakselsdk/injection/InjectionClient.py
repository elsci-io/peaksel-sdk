from peakselsdk.HttpClient import HttpClient
from peakselsdk.injection.Injection import InjectionFull


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

    def get(self, inj_id) -> InjectionFull:
        return InjectionFull.from_json(self.http.get_json(f"/api/injection/{inj_id}"))

    def set_props(self, injection_id: str, props: dict[str, any]) -> None:
        """
        You can associate your own key-value properties with the injections - calculations, labels, etc.

        :param injection_id: the injection to update
        :param props: custom properties that are turned into a JSON. The previous custom props will be completely
                      overritten if they existed. Note, that there can be a limit to how much data can be stored in
                      these props.
        """
        self.http.put(f"/api/injection/{injection_id}/props/userdefined", props)