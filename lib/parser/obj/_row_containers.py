from readline import parse_and_bind
from typing import Self
from lib.parser.obj._col_containers import (coldata, hexadecimal, iso, offset, extension, description)
from lib.util.constants import ColType
from bs4 import Tag, ResultSet

class ColumnsInstance:
    def __init__(self) -> None:
        self.hex: hexadecimal
        self.iso: iso
        self.off: offset
        self.ext: extension
        self.des: description

    def set_col(self, col: Tag, idx: int) -> None:
        if 5 <= idx < 0:
            e = IndexError()
            e.add_note("Index %d out of range" % idx)
            raise e

        match idx:
            case ColType.HEX:
                self.hex = hexadecimal(col, idx)
            case ColType.ISO:
                self.iso = iso(col, idx)
            case ColType.OFF:
                self.off = offset(col, idx)
            case ColType.EXT:
                self.ext = extension(col, idx)
            case ColType.DES:
                self.des = description(col, idx)
            case _:
                pass

class RowInstance:
    def __init__(self, row: ResultSet[Tag]) -> None:
        self._row: ResultSet[Tag] = row
        self.columns: ColumnsInstance

    def set_cols(self, cols: ColumnsInstance) -> None:
        self.columns = cols

    def _check_rowspan(self, col: Tag) -> int:
        return col.has_attr('rowspan')

class Table:
    def __init__(self, wikitable: Tag) -> None:
        self.tableRows: list[ResultSet[Tag]] = [row.find_all(['td']) for row in wikitable.select('tr')]
        self.parsedTable: list[ColumnsInstance] = []
        self.parseIdx: int = 0
        self._create_table()

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> ColumnsInstance:
        if self.parseIdx < len(self.parsedTable):
            result = self.parsedTable[self.parseIdx]
            self.parseIdx += 1
            return result

        raise StopIteration

    def file_signature_table(self): 
        while self.parseIdx < len(self.parsedTable):
            yield self.parsedTable[self.parseIdx]
            self.parseIdx+=1

    def _create_table(self):
        for row in self.tableRows:
            if len(row) == 5:
                parsedRow: ColumnsInstance = ColumnsInstance()
                for idx, col in enumerate(row):
                    print(idx)
                    parsedRow.set_col(col, idx)
                self.parsedTable.append(parsedRow)
