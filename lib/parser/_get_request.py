import asyncio
from enum import StrEnum
from typing import Self, final

from lib.exceptions import UnexpectedFormatError
from lib.util.constants import API_URL

try:
    from requests import Request, Response, Session
    from requests.adapters import ResponseError
    from requests.sessions import PreparedRequest
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("requests module missing -> 'pip install requests'")
    raise

type JsonDict = dict[str, dict[str, str]]

header = {
    "User-Agent": "",
    "Accept-Language": "en"
}

class _ReqData(StrEnum):
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

@final
class WikimediaRequest:
    def __new__(cls, email: str, prev_revid: str | None = None) -> Self:
        if not hasattr(cls, 'revid_checked'):
            cls._obj    = super().__new__(cls)
            cls._email  = email
            cls._orevid = prev_revid
            cls._reqobj = asyncio.create_task(cls._make_request(_ReqData.REVID, cls._email))

            return cls._obj

        cls._reqobj = asyncio.create_task(cls._make_request(_ReqData.TEXT, cls._email))
        return cls._obj

    @classmethod
    async def _async_init(cls) -> Self:
        cls._req            = await cls._reqobj
        cls._json: JsonDict = await cls._get_json(cls._req.json())

        if not hasattr(cls, 'revid_checked'):
            cls.raw_data = cls._json['parse']['revid']
            setattr(cls, 'revid_checked', True)
        else:
            cls.raw_data = cls._json['parse']['text']

        return cls._obj

    @classmethod
    def __await__(cls):
        return cls._async_init().__await__()

    @staticmethod
    async def _make_request(dat_desired: str, email: str) -> Response:
        header['User-Agent']    = email
        params['prop']          = dat_desired

        req: PreparedRequest = Request(
            url     = req_info['url'],
            method  = req_info['method'],
            headers = req_info['headers'],
            params  = req_info['params'],
        ).prepare()

        res = Session().send(request=req, allow_redirects=True)

        if not res.status_code == 200:
            raise ResponseError(f"""Unexpected status code ${res.status_code}
                                 from call to ${req_info['url']}""")

        return res

    @staticmethod
    async def _get_json(raw_json) -> JsonDict:
        if not isinstance(raw_json, dict):
            raise UnexpectedFormatError("Could not convert json to dictionary...")

        return raw_json
