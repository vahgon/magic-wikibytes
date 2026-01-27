from lib.parser._wikitable_parser import parse_html
from lib.parser._html_obj import HTML
from lib.util import DOCS_PATH, USER_ARGS
from pathlib import Path

try:
    from pandas import DataFrame
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("pandas not found. Install with-> pip install pandas")
    raise e

class Table(HTML):
    def __init__(self) -> None:
        super().__init__()
        self.rawFileSigs: list[dict[str, str | None]] = list()
        self.df: DataFrame = DataFrame()
        self.verboseStr: str = ''

        self.format: str | None = USER_ARGS.format
        self.output: Path | None = USER_ARGS.output

    def _print_or_create(self) -> None:
        if self.output and self.format:
            self.output = Path(f'{self.output}.{self.format}')
            self.verboseStr = f'Both output and format given - Created file {self.output}'
            self._set_output(self.output)

        elif self.output:
            self.verboseStr = f'Created file {self.output}'
            self._set_output(self.output)

        elif self.format:
            self.verboseStr = f'Table printed to console as {self.format}'
            self._set_output(self.format)

        else:
            self.output = Path(f'{DOCS_PATH}/signatures.*')
            self.verboseStr = f'No flags set for output or format - defaulted to {self.output}'
            self._set_output(None)

        if USER_ARGS.verbose:
            print(self.verboseStr)

    def _set_output(self, out: Path | str | None) -> None:
        suffix: str | None = out.suffix if isinstance(out, Path) else out 
        toPrint: str | None

        match suffix:
            case '.json' | 'json':
                toPrint = self._create_json()
            case '.csv' | 'csv':
                toPrint = self._create_csv()
            case '.md' | 'md':
                toPrint = self._create_md()
            case None:
                self.output = Path(f'{DOCS_PATH}/signatures.json')
                toPrint = self._create_json()

                self.output = Path(f'{DOCS_PATH}/signatures.csv')
                toPrint = self._create_csv()

                self.output = Path(f'{DOCS_PATH}/signatures.md')
                toPrint = self._create_md()
            case _:
                e = Exception()
                raise e

        if isinstance(toPrint, str):
            print(toPrint)

    def _create_json(self) -> str | None:
        return self.df.to_json(path_or_buf=self.output, lines=False, orient='index', indent=4, force_ascii=False)

    def _create_csv(self) -> str | None:
        return self.df.to_csv(path_or_buf=self.output)

    def _create_md(self) -> str | None:
        md = self.df.replace('\n', '<br>', regex=True)
        return md.to_markdown(self.output, tablefmt='github')

    def make_table(self) -> None:
        self.rawFileSigs= parse_html(self.html)
        self.df = DataFrame(self.rawFileSigs)
        self.df.fillna('',inplace=True)

        self._print_or_create()
