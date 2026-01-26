from lib.parser._wikitable_parser import parse_html
from lib.parser._html_obj import HTML
from lib.constants import ROOT

try:
    from pandas import DataFrame
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("pandas not found. Install with-> pip install pandas")
    raise e

class Table(HTML):
    def __init__(self) -> None:
        super().__init__()
        self.raw_file_sigs: list[dict[str, str | None]] = list()
        self.df: DataFrame = DataFrame()

    def _create_json(self) -> None:
        _ = self.df.to_json(path_or_buf=f"{ROOT}/signatures.json", lines=False, orient='index', indent=4, force_ascii=False)
    def _create_csv(self) -> None:
        _ = self.df.to_csv()
    def _create_md(self) -> None:
        _ = self.df.to_markdown()

    def make_table(self) -> None:
        self.raw_file_sigs = parse_html(self.html)
        self.df = DataFrame(self.raw_file_sigs)
        self._create_json()
