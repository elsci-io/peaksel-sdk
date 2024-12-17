import collections
import json
import typing

from urllib3 import BaseHTTPResponse, PoolManager

from peakselsdk.util.dict_util import merged_dicts


class HttpClient:
    """
    A wrapper around urllib3. We may change the implementation to:
      - `urllib` from stdlib (maybe, but need to implement pooling and a lot of other features in that case)
      - or `requests` (doubtfully, as it has too more dependencies and doesn't provide that much more functionality)
    """

    def __init__(self, base_url: str, default_headers: dict[str:str]):
        self.base_url = base_url
        self.default_headers = merged_dicts(default_headers, {"Content-Type": "application/json;charset=UTF-8"})
        self.http = PoolManager()

    def get_bytes(self, rel_url: str, params: dict[str, any] | None = None, headers: dict[str, str] = None) -> bytes:
        return self._body_binary(self.request(rel_url, "GET", params=params, headers=headers))

    def get_json(self, rel_url: str, params: dict[str, any] | None = None, headers: dict[str, str] = None) -> any:
        return self._body_json(self.request(rel_url, "GET", params=params, headers=headers))

    def post(self, url: str, body: bytes | dict = None, params: dict[str, any] | None = None,
             headers: dict[str, str] = None) -> any:
        body_data = body
        if isinstance(body, collections.abc.Mapping):
            body_data = json.dumps(body_data)
        resp: BaseHTTPResponse = self.request(url, "POST", body=body_data, headers=headers, params=params)
        return self._body_json(resp)

    def put(self, url: str, body: bytes | dict = None, params: dict[str, any] | None = None,
            headers: dict[str, str] = None) -> any:
        body_data = body
        if isinstance(body, collections.abc.Mapping):
            body_data = json.dumps(body_data)
        resp: BaseHTTPResponse = self.request(url, "PUT", body=body_data, headers=headers, params=params)
        return resp.data

    def upload(self, rel_url: str, filepath: str, method="POST", params: dict[str, any] | None = None) -> any:
        with open(filepath, 'rb') as file:
            file_content = file.read()
            all_params = merged_dicts(params, {"fakekey": ("filename", file_content)})
            resp = self.request(rel_url, method=method, params=all_params,
                                headers={'Content-Type': 'application/octet-stream'})
            return self._body_json(resp)

    def request(self, rel_url: str, method: str,
                body: bytes | typing.IO[typing.Any] | typing.Iterable[bytes] | str | None = None,
                params: dict[str, any] | None = None,
                headers: dict[str, str] = None) -> BaseHTTPResponse:
        all_headers = merged_dicts(self.default_headers, headers)
        resp = self.http.request(method, self.base_url + rel_url, body=body, headers=all_headers, fields=params)
        self._assert_ok(resp, body)
        return resp

    def _assert_ok(self, resp: BaseHTTPResponse, req_body: any) -> BaseHTTPResponse:
        status: int = self._status(resp)
        if 200 <= status < 300:
            return resp
        if status == 401:
            err_line = (f"Request {resp.url} failed with status 401 (Unauthorized), meaning that the passed "
                        f"credentials aren't valid or the Session has expired and you need to re-login")
        else:
            err_line = f"Request {resp.url} failed with status {status}"
        body = self._body(resp)
        if not body:
            body = "<Response body is empty>"
        raise Exception(f"{err_line}:\n"
                        f" request:  {req_body}\n"
                        f" response: {body}")

    # Methods like this are written so that we don't access urllib3 in the main code directly, as we may switch
    # to a different implementation (urllib from stdlib) at some point.
    def _status(self, resp: BaseHTTPResponse) -> int:
        return resp.status

    def _body(self, resp: BaseHTTPResponse) -> str:
        return resp.data.decode("utf-8")

    def _body_binary(self, resp: BaseHTTPResponse) -> bytes:
        return resp.data

    def _body_json(self, resp: BaseHTTPResponse) -> any:
        return resp.json()

    def _reason(self, resp: BaseHTTPResponse) -> str:
        return resp.reason
