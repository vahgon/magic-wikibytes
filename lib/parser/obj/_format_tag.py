from dataclasses import dataclass, field
from functools import partial

from bs4 import ResultSet, Tag

from lib.util.constants import BADTAGS, FIXTAGS, ColType

TAGS            = set(FIXTAGS) | set(BADTAGS)

repl_children   = Tag.unwrap
destroy         = Tag.decompose

@dataclass(init=True, repr=False)
class _TagContainer:
    _list: list[Tag] = field(default_factory=lambda: [Tag(name='') for _ in range(5)], repr=False)

    def __getitem__(self, idx: int) -> Tag:
        return self._list[idx]

    def __setitem__(self, idx: int, tag: Tag) -> None:
        TagCleaner.clean_children(tag)
        self._list[idx] = tag

    def clear(self) -> None:
        '''
        Clears all `Tag` elements in the list
        '''
    @property
    def hex(self) -> Tag: return self._list[ColType.HEX]
    @hex.setter
    def hex(self, tag: Tag) -> None: self._list[ColType.HEX] = tag

    @property
    def iso(self) -> Tag: return self._list[ColType.ISO]
    @iso.setter
    def iso(self, tag: Tag) -> None: self._list[ColType.ISO] = tag

    @property
    def off(self) -> Tag: return self._list[ColType.OFF]
    @off.setter
    def off(self, tag: Tag) -> None: self._list[ColType.OFF] = tag

    @property
    def ext(self) -> Tag: return self._list[ColType.EXT]
    @ext.setter
    def ext(self, tag: Tag) -> None: self._list[ColType.EXT] = tag

    @property
    def des(self) -> Tag: return self._list[ColType.DES]
    @des.setter
    def des(self, tag: Tag) -> None: self._list[ColType.DES] = tag

class TagCleaner:
    '''
    A TagCleaner will properly format every `PageElement` object found in a given list (`ResultSet`)
    of `Tags`.
    '''
    def __init__(self, rows: list[ResultSet[Tag]]) -> None:
        self.tags:      _TagContainer            = _TagContainer()

        self._rows:     list[ResultSet[Tag]]     = rows
        self._ptr:      int                      = 0

        self._colmap:   dict[int, partial[None]] = {
            ColType.HEX: partial(self._hex_col),
            ColType.ISO: partial(self._iso_col),
            ColType.OFF: partial(self._off_col),
            ColType.EXT: partial(self._ext_col),
            ColType.DES: partial(self._des_col),
        }

    def clean(self) -> None:
        '''
        Cleans all `Tag` objects found in the wikimedia table that makes up the 
        found `BeautifulSoup` wikitable.
        '''
        for row in self._rows:
            self._config_cols(row)

    def _config_cols(self, row: ResultSet[Tag]):
        for idx, col in enumerate(row):
            if self.tags[idx].name == '':
                self.tags[idx] = col
                self._colmap[idx](col)
                self._ptr+=1

        if self._ptr == 5:
            self._ptr = 0
            self._balance_hex_iso()
            self.tags = _TagContainer()

    def _config_rowspan(self) -> None: ...

    def _balance_hex_iso(self) -> None:
        code_tags = [self.tags[ColType.HEX].find_all('code'),
                     self.tags[ColType.ISO].find_all('code')]
        code_tags.sort(reverse=True, key=len)

        diff = abs(len(code_tags[0]) - len(code_tags[1]))
        match diff:
            case 0:
                return
            case 1:
                # Wrap larger of unbalanced Tag to be an equal amount of code Tags
                return

            case _:
                if code_tags[1] == 0:
                    # Add a code Tag to the column that has none
                    return
                raise Exception()

    @staticmethod
    def _hex_col(col: Tag) -> None: ...

    @staticmethod
    def _iso_col(col: Tag) -> None: ...

    @staticmethod
    def _off_col(col: Tag) -> None: ...

    @staticmethod
    def _ext_col(col: Tag) -> None: ...

    @staticmethod
    def _des_col(col: Tag) -> None: ...

    @staticmethod
    def clean_children(col: Tag) -> None:
        '''
        Removes/formats all found `PageElement` objects from a given `Tag` based on their 
        `.name` property.

        :param col: The `Tag` object to format
        '''
        for tag in col.find_all(TAGS):
            if tag.name in FIXTAGS:
                _ = repl_children(tag)
            elif tag.name in BADTAGS:
                destroy(tag)
