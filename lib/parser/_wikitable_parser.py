import re
from typing import Self

from lib.exceptions import NoTagFoundError
from lib.parser.obj._format_tag import TagCleaner
from lib.parser.obj._row_containers import Row
from lib.util.constants import ParsedTableDict

try:
    from bs4 import BeautifulSoup, ResultSet, Tag
    from bs4.filter import SoupStrainer
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("bs4 not found. Install with -> pip install bs4")
    raise e

class _WikiTable:
    def __init__(self, html: str) -> None:
        self._wikitable: Tag
        self._html:      str            = re.sub(pattern=r'\n', repl='', string=html)
        self._strainer:  SoupStrainer   = SoupStrainer(name='table', attrs= { 'class': 'wikitable sortable' })
        self.tbody_tag:  Tag

        self._strain_soup()

    def _strain_soup(self) -> None:
        self._wikitable = BeautifulSoup(markup=self._html, parse_only=self._strainer, features='lxml')
        tbody = self._wikitable.select_one('tbody')

        if not isinstance(tbody, Tag):
            e = NoTagFoundError()
            e.add_note("Error formatting wikitable - no <tbody> tag was found.")
            raise e

        self.tbody_tag = tbody

    def prettify(self) -> str:
        '''
        Pretty prints the Wikimedia API's response wikitable. This is done by calling
        prettify() on the tbody `Tag`

        :return: string
        '''
        return self._wikitable.prettify()

class Parser(_WikiTable):
    '''
    Converts wikimedia response's wikitable into a more accessible format. 
    '''
    def __init__(self, html: str) -> None:
        super().__init__(html)
        self._table_rows:   list[ResultSet[Tag]]
        self._table_header: ResultSet[Tag]
        self._parsed_table: list[Row] = []
        self.__idx = 0

        self._clean_tags()
        self._parse_rows()

    def __iter__(self) -> Self:
        self.__idx = 0
        return self

    def __next__(self) -> Row:
        if self.__idx < 5:
            result = self._parsed_table[self.__idx]
            self.__idx += 1
            return result
        raise StopIteration

    def _clean_tags(self) -> None:
        found_rows = [row.find_all(['td', 'th']) for row in self.tbody_tag.select('tr')]
        self._table_header = found_rows.pop(0)
        self._table_rows = TagCleaner(found_rows).clean()

    def _parse_rows(self) -> None:
        for row in self._table_rows:
            if len(row) == 5:
                self._parsed_table.append(Row(row))

    def todict(self) -> ParsedTableDict:
        """
        Fills a list of the original row instances but in dictionary format. The default 
        number of keys in each dictonary item is 5 in {`column name`: `column data`} format.

        :return: list[dict[str, ColData]] (`ParsedTableDict`)
        """
        return [{col.name: col.text for col in row} for row in self._parsed_table]
