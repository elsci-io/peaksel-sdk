import typing

from urllib3 import request, BaseHTTPResponse, PoolManager


class HttpClient:
    """
    A wrapper around urllib3. We may change the implementation to:
      - `urllib` from stdlib (maybe, but need to implement pooling and a lot of other features in that case)
      - or `requests` (doubtfully, as it has too more dependencies and doesn't provide that much more functionality)
    """

    def __init__(self, base_url: str, default_headers: dict[str:str]):
        self.base_url = base_url
        self.default_headers = default_headers
        self.http = PoolManager()

    def post(self, url: str):
        print(self.base_url + url)
        resp: BaseHTTPResponse = request("GET", self.base_url + url)
        print(resp.status)
        print(resp.data)

    def upload(self, url: str, filepath: str, method="POST", params: dict[str, any] | None = None) -> any:
        with open(filepath, 'rb') as file:
            file_content = file.read()
            all_params = self._dicts(params, {"fakekey": ("filename", file_content)})
            resp = self.request(url, method=method, params=all_params,
                                headers={'Content-Type': 'application/octet-stream'})
            return self._body_json(resp)

    def request(self, url: str, method: str,
                body: bytes | typing.IO[typing.Any] | typing.Iterable[bytes] | str | None = None,
                params: dict[str, any] | None = None,
                headers: dict[str, str] = ()) -> BaseHTTPResponse:
        all_headers = self._dicts(self.default_headers)
        all_headers.update(headers)
        resp = self.http.request(method, self.base_url + url, body=body, headers=all_headers, fields=params)
        self._assert_ok(resp)
        return resp

    def _assert_ok(self, resp: BaseHTTPResponse) -> BaseHTTPResponse:
        status: int = self._status(resp)
        if 200 <= status < 300:
            return resp
        if status == 401:
            err_line = (f"Request {resp.url} failed with status 401 (Unauthorized), meaning that the passed "
                        f"credentials aren't valid or the Session has expired and you need to re-login")
        else:
            err_line = f"Request {resp.url} failed with status {status} {self._reason(resp)}"
        body = self._body(resp)
        if not body:
            body = "<Response body is empty>"
        raise Exception(err_line + ":\n" + body)

    # Methods like this are written so that we don't access urllib3 in the main code directly, as we may switch
    # to a different implementation (urllib from stdlib) at some point.
    def _status(self, resp: BaseHTTPResponse) -> int:
        return resp.status

    def _body(self, resp: BaseHTTPResponse) -> str:
        return resp.data.decode("utf-8")

    def _body_json(self, resp: BaseHTTPResponse) -> any:
        return resp.json()

    def _reason(self, resp: BaseHTTPResponse) -> str:
        return resp.reason

    def _dicts(self, d1: dict[str, any] | None, d2: dict[str, any] | None = None) -> dict[str, any]:
        result: dict[str, any] = {}
        if d1:
            result.update(d1)
        if d2:
            result.update(d2)
        return result