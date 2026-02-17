from lib.parser._wikitable_parser import parse_html, pretty_html
from lib.util import DOCS_PATH, USER_ARGS, FileData
from lib.parser.obj._html_obj import HTML
from pathlib import Path
import logging

try:
    from pandas import DataFrame
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("pandas not found. Install with -> pip install pandas")
    raise e

class Table(HTML):
    def __init__(self) -> None:
        super().__init__()
        self.fileOutput: Path | None = USER_ARGS.output
        self.fileFormat: str | None = USER_ARGS.format
        self.fileToDocs: bool | None = USER_ARGS.docs

        self.rawFileSigs: list[dict[str, FileData]]
        self.df: DataFrame = DataFrame()

    def _determine_io(self) -> None:
        if self.fileOutput:
            logging.info(f'Creating file {self.fileOutput}')
            self._set_output(self.fileOutput)

        elif self.fileFormat:
            logging.info(f'Printing wikitable to screen as {self.fileFormat}')
            self._set_output(self.fileFormat)

        elif self.fileToDocs:
            logging.info(f'Creating wikitable in all implemented formats and saving to {Path(f'{DOCS_PATH}/signatures.*')}')
            self._set_output(None)
        else:
            logging.info("No file format or output path provided, Printing raw response data.")
            print(pretty_html(self.html))

    def _set_output(self, out: Path | str | None) -> None:
        suffix: str | None = out.suffix if isinstance(out, Path) else out 

        match suffix:
            case '.json' | 'json':
                _ = self._create_json()
            case '.csv' | 'csv':
                _ = self._create_csv()
            case '.md' | 'md':
                _ = self._create_md()
            case None:
                self.fileOutput = Path(f'{DOCS_PATH}/signatures.json')
                _ = self._create_json()
                self.fileOutput = Path(f'{DOCS_PATH}/signatures.csv')
                _ = self._create_csv()
                self.fileOutput = Path(f'{DOCS_PATH}/signatures.md')
                _ = self._create_md()
            case _:
                e = Exception()
                raise e

    def _create_json(self) -> str | None:
        self.df = DataFrame(self.rawFileSigs)
        return self.df.to_json(self.fileOutput, orient='index', indent=True, force_ascii=False)

    def _create_csv(self) -> str | None:
        self.df = DataFrame(self.rawFileSigs)
        return self.df.to_csv(path_or_buf=self.fileOutput)

    def _create_md(self) -> str | None:
        self.df = DataFrame(self.rawFileSigs)
        return self.df.replace(r'\n', '<br>', regex=True).to_markdown(buf=self.fileOutput, tablefmt='github')

    def make_table(self) -> None:
        self.rawFileSigs = parse_html(self.html)
        self.df.fillna('', inplace=True)

        self._determine_io()
