from typing import Any, Self

from bs4 import ResultSet, Tag

from lib.parser.obj._col_containers import ColumnFactory, FileSignatureTag

class Row:
    def __init__(self, row: ResultSet[Tag], args) -> None:
        self._cols:         list[FileSignatureTag] = ColumnFactory().set_row(row, args)
        self._col_amount:   int                    = len(row)
        self.__idx:         int                    = 0
        self.row:           ResultSet[Tag]         = row

    def __iter__(self) -> Self:
        self.__idx = 0
        return self

    def __next__(self) -> FileSignatureTag:
        if self.__idx < self._col_amount:
            result = self._cols[self.__idx]
            self.__idx += 1
            return result
        raise StopIteration
