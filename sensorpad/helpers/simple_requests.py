import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Response:

    def __init__(self, body, headers, status, error_count=0):
        self.body = body
        self.headers = headers
        self.status_code = status
        self.error_count = error_count

    @property
    def text(self):
        """Return body as text."""
        return self.body

    def json(self):
        """
        Decode body's JSON.

        Returns:
            Python representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output


def request(
    url,
    data=None,
    params=None,
    headers=None,
    method="GET",
    data_as_json=True,
    timeout=5,
    error_count=0,
):
    if not url.casefold().startswith("http"):
        raise URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers.update({"Accept": "application/json"})
    if method == "GET":
        params.update(data)
        data = None

    if params:
        url += "?" + urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urlencode(data).encode()

    httprequest = Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urlopen(httprequest, timeout=timeout) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except HTTPError as e:
        response = Response(
            body=str(e.read().decode()),
            headers=e.headers,
            status=e.code,
            error_count=error_count + 1,
        )

    return response
