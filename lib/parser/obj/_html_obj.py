from lib.parser._get_request import get_response
from lib.util import EMAIL

class HTML:
    def __init__(self) -> None:
        self.html: str
        self.revId: int
        self.email: str = EMAIL
        self.resJson: dict[str, str | int]

        [self.resJson, self.html, self.revId] = get_response()
