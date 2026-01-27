from lib.get_request import get_json_response
from lib.util import EMAIL

class HTML:
    def __init__(self) -> None:
        self.email: str = EMAIL
        self.resJson: dict[str, str | int]
        self.html: str

        [self.resJson, self.html] = get_json_response()

    def compare_revision(self) -> None:
        ...
    def mk_markdown_table(self) -> None:
        ...
    def mk_json(self) -> None:
        ...
