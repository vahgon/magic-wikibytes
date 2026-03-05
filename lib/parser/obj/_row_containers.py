from typing import Self

from bs4 import ResultSet, Tag

from lib.parser.obj._col_containers import ColumnFactory, FileSignatureTag
from lib.util.constants import ColType, FIXTAGS, BADTAGS, HEADERNAMES

TAGS            = set(FIXTAGS) | set(BADTAGS)
repl_children   = Tag.unwrap
destroy         = Tag.decompose

appendRow: Callable[[list[FileSignatureTag], FileSignatureTag], None] = list.append

class Row:
    def __init__(self, row: ResultSet[Tag]) -> None:
        self._cols:         list[FileSignatureTag]  = []
        self._colAmount:    int                     = len(row)
        self.__idx:         int                     = 0
        self.row:           ResultSet[Tag]          = row

        self._fill_row()

    def _format_children(self, col: Tag) -> Tag:
        for tag in col.find_all(TAGS, recursive=True):
            if tag in BADTAGS:
                destroy(tag)
            elif tag in FIXTAGS:
                _ = repl_children(tag)
        return col

    def _fill_row(self) -> None:
        for col in ColType:
            appendRow(self._cols, ColumnFactory.col_type(col, self._format_children(self.row[col]), self.row))
            self._cols[col].name = HEADERNAMES[col]

    def __iter__(self) -> Self:
        self.__idx = 0
        return self

    def __next__(self) -> FileSignatureTag:
        if self.__idx < self._colAmount:
            result = self._cols[self.__idx]
            self.__idx += 1
            return result
        raise StopIteration
