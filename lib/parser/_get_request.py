from enum import StrEnum
from lib.exceptions import UnexpectedFormatError
from lib.util.constants import API_URL
from asyncio import Event

try:
    from requests import Request, Response, Session
    from requests.adapters import ResponseError
    from requests.sessions import PreparedRequest
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("requests module missing -> 'pip install requests'")
    raise

type JsonDict = dict[str, dict[str, str]]

email = ''

header = {
    "User-Agent": "",
    "Accept-Language": "en"
}

class RequestData(StrEnum):
    TEXT    = "text"
    REVID   = "revid"

params = {
    "action": "parse",
    "format": "json",
    "page": "List_of_file_signatures",
    "prop": "",
    "disablelimitreport": 1,
    "disableeditsection": 1,
    "disabletoc": 1,
    "contentformat": "application/json",
    "formatversion": "2"
}
req_info= {
    "url": API_URL,
    "method": "GET",
    "headers": header,
    "params": params
}

class WikimediaRequest:
    def __init__(self) -> None:
        self._resp: Response        = self._make_request(RequestData.TEXT, "")
        self.json:  JsonDict        = self._get_json(self._resp.json())
        self.raw:   dict[str, str]  = self.json['parse']
        self.email: str

    @staticmethod
    def _check_revid():
        ...

    @staticmethod
    def _get_text() -> None:
        params['prop'] = "text"

    @staticmethod
    def _make_request(dat_desire: str, email: str) -> Response:
        header['User-Agent']    = email
        params['prop']          = dat_desire

        req: PreparedRequest = Request(
            url     = req_info['url'],
            method  = req_info['method'],
            headers = req_info['headers'],
            params  = req_info['params'],
        ).prepare()

        res = Session().send(request=req, allow_redirects=True)

        if not res.status_code == 200:
            raise ResponseError(f"Unexpected status code ${res.status_code} from call to ${req_info['url']}")

        return res

    @staticmethod
    def _get_json(raw_json) -> dict[str, dict[str, str]]:
        if not isinstance(raw_json, dict):
            raise UnexpectedFormatError("Could not convert json to dictionary")

        return raw_json
