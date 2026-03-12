from pathlib import Path

from lib.parser._wikitable_parser import Parser
from lib.parser.obj._html_obj import HTML
from lib.util import USER_ARGS, FileData

try:
    from pandas import DataFrame
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("pandas not found. Install with -> pip install pandas")
    raise e

class Table(HTML):
    def __init__(self) -> None:
        super().__init__()
        self.parser:    Parser = Parser(self.html)
        self.raw_fsigs: list[dict[str, FileData]] = self.parser.todict()
        self.dataframe: DataFrame = DataFrame()

        self.file_output: str = USER_ARGS.output if USER_ARGS.output else './output'
        self.file_format: (str | None) = USER_ARGS.format

        self._create_output()

    def _create_output(self) -> None:
        match self.file_format:
            case ('.json' | 'json'):
                self._create_json()

            case ('.csv' | 'csv'):
                self._create_csv()

            case ('.md' | 'md'):
                self._create_md()

            case None:
                print(self._create_json())

            case _:
                e = Exception()
                raise e

    def _create_json(self) -> str | None:
        self.dataframe = DataFrame(self.raw_fsigs)
        return self.dataframe.to_json(str(self.file_output+'.json'), orient='index', indent=True, force_ascii=False)

    def _create_csv(self) -> str | None:
        self.dataframe = DataFrame(self.raw_fsigs)
        return self.dataframe.to_csv(path_or_buf=self.file_output)

    def _create_md(self) -> str | None:
        self.dataframe = DataFrame(self.raw_fsigs)
        return self.dataframe.replace(r'\n', '<br>', regex=True).to_markdown(buf=self.file_output, tablefmt='github')

    def make_table(self) -> None:
        self.dataframe.fillna('', inplace=True)
