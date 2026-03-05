from lib.parser._get_request import get_response
from lib.util import EMAIL

class HTML:
    def __init__(self) -> None:
        self._email:       str = EMAIL
        self._revision_id: int
        self._res_json:    (dict[str, str | int])
        self.html:         str

        [self._res_json, self.html, self._revision_id] = get_response()

    def check_rev_id(self) -> None:
        '''
        Checks whether the last execution of this script had a response with a differing revision
        id than the current execution. If so, parse the response. If not, don't.
        '''
