from typing import final, override

from bs4 import ResultSet, Tag

from lib.parser.obj._format_obj import checkbytes
from lib.util.constants import HEADERNAMES, ColType

class FileSignatureTag:
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        self.__name: str
        self.tag:    Tag               = col.extract()
        self.text:   (list[str] | str) = self.tag.get_text()
        self.row:    ResultSet[Tag]    = row

    @override
    def __str__(self) -> str:
        return self.text if isinstance(self.text, str) else '\n'.join(self.text)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @staticmethod
    def set_text(tags: list[str]) -> (list[str] | str):
        if not tags:
            return ''
        return  tags[0] if len(tags) == 1 else tags

@final
class ByteData(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)
        self._original_hex: (list[str] | str) = []
        self._code_tags:    ResultSet[Tag]    = self.tag.find_all('code')
        self.text = self.set_text([hex.get_text() for hex in self._code_tags])

    @property
    def original_hex(self) -> (list[str] | str):
        return self._original_hex

@final
class ISOData(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)
        self._original_iso: (list[str] | str) = []
        self._code_tags:    ResultSet[Tag]    = self.tag.find_all('code')
        self.text = self.set_text([iso.get_text() for iso in self._code_tags])

@final
class Offset(FileSignatureTag):
    '''
    todo - format offset & add to formatting done in checkbytes object
    '''

@final
class FileSignatureExtension(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)
        self.text = [t.get_text() for t in self.tag.children] if len(self.tag) > 1 else self.text

@final
class Description(FileSignatureTag): ...

class ColumnFactory:
    '''
    Factory class used to populate `Row` objects.
    '''
    @staticmethod
    def set_row(row: ResultSet[Tag]) -> list[FileSignatureTag]:
        '''
        Factory method used to populate `Row` objects with column information.

        :param row: `ResultSet`[`Tag`] holding each columns value
        :return: `list`[`FileSignatureTag`] - class holding each columns information.
         '''
        subclasses: list[type[FileSignatureTag]] = FileSignatureTag.__subclasses__()
        cols: list[FileSignatureTag]             = []

        for idx, col in enumerate(row):
            cols.append(subclasses[idx](col, row))
            cols[idx].name = HEADERNAMES[idx]

        bal_bytes = checkbytes(cols[ColType.HEX].text, cols[ColType.ISO].text)

        if isinstance(cols[ColType.HEX].text, str) and isinstance(cols[ColType.ISO].text, str):
            cols[ColType.HEX].text = bal_bytes.hex
            cols[ColType.ISO].text = bal_bytes.iso

        return cols
