import re
from typing import final, override

from bs4 import ResultSet, Tag

from lib.exceptions import NoTagFoundError
from lib.parser.obj._format_obj import checkbytes
from lib.util.constants import HEADERNAMES, ColType

type Codetags = ResultSet[Tag] | Tag
type Textdata = list[str] | str

class FileSignatureTag:
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        self.__name:    str
        self.row:       ResultSet[Tag]  = row
        self.tag:       Tag             = col.extract()
        self.text:      Textdata        = self.tag.get_text()

    @override
    def __str__(self) -> str:
        return self.text if isinstance(self.text, str) else '\n'.join(self.text)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

@final
class ByteData(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)

        self._original_hex: (list[str] | str)   = []
        self._code_tags:    ResultSet[Tag]      = self.tag.find_all('code')
        self._iso_tags:     ResultSet[Tag]      = self.row[ColType.ISO].find_all('code')
        self.hex:           (list[Filebyte] | Filebyte)

        self._set_hex()

    def _set_hex(self) -> None:
        for codetag in self._code_tags:
            for br in codetag.find_all('br'):
                _ = br.unwrap()

        if len(self._code_tags) == 1:
            self.text = self._code_tags[0].get_text()
        else:
            self.text = [hex.get_text() for hex in self._code_tags]

        self._balance_codetags()

    def _balance_codetags(self) -> None:
        sisters = [self._code_tags, self._iso_tags]
        sisters.sort(key=len, reverse=True)

        if len(sisters[0]) != len(sisters[1]):
            if (len(sisters[0]) - len(sisters[1]) == 1) and (sisters[1]):
                _ = sisters[0][0].append(sisters[0].pop().extract().getText())
            elif len(sisters[-1]) == 0:
                pass
            else:
                e = WikitableFormatError()
                e.add_note("Problem while balancing codetags for hex and iso columns")
                raise e

    @property
    def original_hex(self) -> (list[str] | str):
        return self._original_hex

@final
class ISOData(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)
        self._code_tags:    ResultSet[Tag] = self.tag.find_all('code')
        self._latin:        Latin1
        self._hex_bytes:    str

        self._set_iso()

    def _set_iso(self) -> None:
        if not self._code_tags:
            # log
            self.text = self.tag.get_text()
        else:
            if len(self._code_tags) == 1:
                self.text = self._code_tags[0].get_text()
            elif len(self._code_tags) > 1:
                self.text = [iso.get_text() for iso in self._code_tags]
    @property
    def hex_bytes(self) -> str:
        return self._hex_bytes

    @hex_bytes.setter
    def hex_bytes(self, h_str: str) -> None:
        self._hex_bytes = h_str

@final
class Offset(FileSignatureTag):
    '''
    Subclass does nothing as of now.
    '''

@final
class FileSignatureExtension(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)
        self._extensions = [tag.get_text() for tag in self.tag]

        self._set_exts()

    def _set_exts(self) -> None:
        if not self._extensions:
            self.text = ''
            return
        self.text = self._extensions[0] if len(self._extensions) == 1 else self._extensions

@final
class Description(FileSignatureTag):
    def __init__(self, col: Tag, row: ResultSet[Tag]) -> None:
        super().__init__(col, row)
        self.text = re.sub(pattern=r'(\[\w\d*\])', repl='', string=self.tag.get_text())

class ColumnFactory:
    @staticmethod
    def set_row(row: ResultSet[Tag]) -> list[FileSignatureTag]:
        subclasses: list[type[FileSignatureTag]]    = FileSignatureTag.__subclasses__()
        converted:  list[FileSignatureTag]          = []

        for idx, col in enumerate(row):
            converted.append(subclasses[idx](col, row))
        return converted

    @staticmethod
    def col_type(colType: int, col: Tag, row: ResultSet[Tag]) -> FileSignatureTag:
        return FileSignatureTag.__subclasses__()[colType](col, row)
