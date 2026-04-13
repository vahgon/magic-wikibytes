from argparse import Namespace
from pathlib import Path
from typing import Self

from lib.parser._wikitable_parser import Parser
from lib.parser.obj._html_obj import HTML

try:
    from pandas import DataFrame
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("pandas not found. Install with -> pip install pandas")
    raise e

class Table(HTML):
    """
    Initializes the creation of the parsed wikitable object sent from the Wikimedia API.
    """
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._parser: Parser
        self._dataframe: DataFrame
        self._output: Path

    async def _init(self) -> Self:
        await self._async_init()

        if not self.USER_ARGS.force and not await self.check_duplicate_revid():
            print("duplicate ID detected")
            return self

        await self.get_wikitable_req()

        self._parser    = Parser(self.request.raw_data, self.USER_ARGS)
        self._dataframe = DataFrame(self._parser.todict())

        if self.USER_ARGS.output:
            self._output = self.USER_ARGS.output

            self._create_output()
        else:
            self._cli_out()

        return self

    def __await__(self):
        return self._init().__await__()

    def _create_output(self) -> None:
        if self._output:
            match self._output.suffix:
                case '.json':
                    self._create_json()
                case '.md':
                    self._create_md()
                case _:
                    # log warn
                    self._output = self._output.with_suffix('.json')
                    self._create_json()

    def _create_json(self) -> None:
        self._dataframe.to_json(
            self._output.with_suffix('.json'),
            orient='index',
            indent=True,
            force_ascii=False
        )

    def _create_md(self) -> None:
        self._dataframe.replace(r'\n', '<br>', regex=True).to_markdown(
            buf=self._output.with_suffix('.md'),
            tablefmt='github'
        )

    def _cli_out(self) -> None:
        print(self._dataframe.to_json(
            orient='index',
            indent=True,
            force_ascii=False))
