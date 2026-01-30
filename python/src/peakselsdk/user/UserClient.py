from peakselsdk.HttpClient import HttpClient
from peakselsdk.user.User import User


class UserClient:
    def __init__(self, settings: HttpClient):
        self.http: HttpClient = settings

    def get_current_user(self) -> User | None:
        resp = self.http.get_json(f"/api/me")
        return User.from_json(resp) if "id" in resp else None
