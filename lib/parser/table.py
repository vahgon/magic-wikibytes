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
        self.dataframe: DataFrame = DataFrame(self.parser.todict())
        self.output:    Path = Path(USER_ARGS.output)

        self._create_output()

    def _create_output(self) -> None:
        match USER_ARGS.format:
            case ('.json' | 'json'):
                self._create_json()
            case ('.md' | 'md'):
                self._create_md()
            case None:
                self._cli_out()

            case _:
                e = Exception()
                raise e

    def _create_json(self) -> None:
        self.dataframe.to_json(Path(USER_ARGS.output).with_suffix('.json'), orient='index', indent=True, force_ascii=False)

    def _create_md(self) -> None:
        self.dataframe.replace(r'\n', '<br>', regex=True).to_markdown(buf=Path(USER_ARGS.output).with_suffix('.md'), tablefmt='github')

    def _cli_out(self) -> None:
        print(self.dataframe.to_json(orient='index', indent=True, force_ascii=False))

    def make_table(self) -> None:
        self.dataframe.fillna('', inplace=True)
