from requests.adapters import ResponseError
from lib.exceptions import UnexpectedFormatError

try:
    import requests
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("requests module missing -> 'pip install requests'")
    raise

wikimedia_api_call = 'https://en.wikipedia.org/w/api.php' 
email = ''

header = {
    "User-Agent": email,
    "Accept-Language": "en"
}
params = {
    "action": "parse",
    "format": "json",
    "page": "List_of_file_signatures",
    "prop": "revid|text",
    "disablelimitreport": 1,
    "disableeditsection": 1,
    "disabletoc": 1,
    "contentformat": "application/json",
    "formatversion": "2"
}
req_info = {
    "url": wikimedia_api_call,
    "method": "GET",
    "headers": header,
    "params": params
}

def format_request(req: requests.Request) -> requests.Request:
    req.url = req_info['url']
    req.method = req_info['method']
    req.headers = req_info['headers']
    req.params = req_info['params']
    return req

def make_request() -> requests.Response:
    req = format_request(requests.Request())
    request = req.prepare()
    response = requests.Session()
    return response.send(request=request, allow_redirects=True)

type HtmlJson = dict[str, str | int]
type ReqJson = dict[str, HtmlJson]
    
def get_json_response(res: requests.Response | None = None) -> tuple[HtmlJson, str]:
    res = make_request()
    if not res.status_code == 200:
        e = ResponseError()
        e.add_note(f"Did not receive status code ${res.status_code}")
        raise e

    raw_data = res.json()
    res_json: ReqJson | None = raw_data if isinstance(raw_data, dict) is not False else None

    if res_json is None:
        e = UnexpectedFormatError()
        e.add_note("When converting type of response data to json, result was not dict")
        raise e

    html: str = str(res_json['parse']['text'])

    return (res_json['parse'], html)

