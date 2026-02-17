from lib.util.constants import HEADERNAMES, FileData
from typing import final
from bs4 import Tag, ResultSet
import bs4
import re

type codetags = (ResultSet[Tag] | Tag)

def _format_hexstring(hexString: str) -> str:
    return hexString.replace(' ', '').replace('\xa0', '')

class HexInstance:
    def __init__(self, hexString: str) -> None:
        self.text: str = _format_hexstring(hexString) if (hexString.count(' ') != 0 or hexString.count('\xa0') != 0) else hexString
        self.byteList: list[str] = [self.text[i:i+2] for i in range(0, len(self.text), 2)]
        self.wildcardbytes: bool = True if self.byteList.count('??') else False
        self._format_hex()

    def _format_hex(self) ->  None:
        for i in self.byteList:
            if i != '??':
                byte = bytes.fromhex(i)
                decoded = byte.decode('latin-1')

class coldata:
    def __init__(self, tag: Tag, idx: int) -> None:
        self.tag: Tag = tag
        self.string: FileData = tag.get_text()
        self.name: str = HEADERNAMES[self.__idx]
        self.__idx: int = idx
        self._fix_coltag_children()

    def __call__(self, tag: Tag, idx: int):
        self.__init__(tag, idx)

    def _expected_tag(self, tagName: str) -> bool:
        return True if self.tag.find(tagName) else False

    def _get_codeTags(self, tagName: str) -> (ResultSet[Tag] | Tag):
        if not self._expected_tag(tagName):
            # log this
            return self.tag

        codeTags = self.tag.find_all(tagName)
        return codeTags[0] if len(codeTags) == 1 else codeTags
    
    def _fix_coltag_children(self) -> None:
        BADTAGS = ['cite', 'sup', 'span']
        FIXTAGS = ['a', 'p']

        for tag in BADTAGS:
            for foundTag in self.tag.find_all(tag):
                foundTag.decompose()

        for tag in FIXTAGS:
            for foundTag in self.tag.find_all(tag):
                _ = foundTag.replaceWithChildren()

        for codeTag in self.tag.find_all('code'):
            for br in codeTag.find_all('br'):
                _ = br.extract()

    def _remove_br(self) -> None:
        for brTag in self.tag.find_all('br'):
            brTag.decompose()

@final
class hexadecimal(coldata):
    def __init__(self, tag: Tag, idx: int) -> None:
        super().__init__(tag, idx)
        self.__hexString: str
        self.__qData: str | None
        self.__codeTags: ResultSet[Tag] | Tag = super()._get_codeTags('code')

        self.string = self._set_hex()
    
    def _set_hex(self) -> str | list[str]:
        if isinstance(self.__codeTags, Tag):
            return HexInstance(self.__codeTags.get_text()).text

        hexList: str | list[str] = []
        for tag in self.__codeTags:
            hexList.append(HexInstance(tag.get_text()).text)
        return hexList

@final
class iso(coldata):
    def __init__(self, tag: Tag, idx: int) -> None:
        super().__init__(tag, idx)
        self.__codeTags: ResultSet[Tag] | Tag = super()._get_codeTags('code')
        self.string: FileData = self._set_iso()

    def _set_iso(self) -> (list[str] | str):
        if isinstance(self.__codeTags, Tag):
            return self.__codeTags.get_text()
        
        return [iso.get_text() for iso in self.__codeTags]

@final
class offset(coldata):
    def __init__(self, tag: Tag, idx: int) -> None:
        super().__init__(tag, idx)

@final
class extension(coldata):
    def __init__(self, tag: Tag, idx: int) -> None:
        super().__init__(tag, idx)
        self._remove_br()
        self.text: str | list[str] = self.tag.get_text(separator='\n').split('\n')

@final
class description(coldata):
    def __init__(self, tag: Tag, idx: int) -> None:
        super().__init__(tag, idx)
