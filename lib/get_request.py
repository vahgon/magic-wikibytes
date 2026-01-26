from requests.adapters import ResponseError
from lib.exceptions import UnexpectedFormatError

try:
    import requests
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("requests module missing -> 'pip install requests'")
    raise

wikimediaAPICall= 'https://en.wikipedia.org/w/api.php' 
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
reqInfo= {
    "url": wikimediaAPICall,
    "method": "GET",
    "headers": header,
    "params": params
}

def format_request(req: requests.Request) -> requests.Request:
    req.url = reqInfo['url']
    req.method = reqInfo['method']
    req.headers = reqInfo['headers']
    req.params = reqInfo['params']
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

    rawData = res.json()
    resJson: ReqJson | None = rawData if isinstance(rawData, dict) is not False else None
    if resJson is None:
        e = UnexpectedFormatError()
        e.add_note("When converting type of response data to json, result was not dict")
        raise e

    html: str = str(resJson['parse']['text'])
    return (resJson['parse'], html)
