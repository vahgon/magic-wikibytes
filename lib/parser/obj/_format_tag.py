import re
from collections import deque
from dataclasses import dataclass, field
from functools import partial
from typing import Self

from bs4 import ResultSet, Tag

from lib.util.constants import BADTAGS, FIXTAGS, JNK_CHARS, ColType

repl_children = Tag.unwrap
destroy       = Tag.decompose
TAGS          = (set(FIXTAGS) | set(BADTAGS))

@dataclass
class _RowspanTag:
    tag: Tag
    idx: int

@dataclass
class _TagContainer:
    _contains_rowspans: bool = False
    _rowspan_amount:    int  = 0
    _idx:               int  = 0

    row_list: ResultSet[Tag] = field(
        default_factory=lambda: ResultSet(source=None, result=[Tag(name='') for _ in range(5)]),
        repr=False
    )
    rowspan_cols: list[_RowspanTag] = field(default_factory=list[_RowspanTag])

    def __getitem__(self, idx: int) -> Tag:
        return self.row_list[idx]

    def __setitem__(self, idx: int, tag: Tag) -> None:
        self.row_list[idx] = tag

        if tag.has_attr('rowspan'):
            self.has_rowspan = True
            self.rowspan = int(str(tag['rowspan']))
            self.rowspan_cols.append(_RowspanTag(tag, idx))

            del tag.attrs['rowspan']

    def __iter__(self) -> Self:
        self._idx = 0
        return self

    def __next__(self) -> Tag:
        if self._idx < 5:
            result = self.row_list[self._idx]
            self._idx+=1
            return result
        raise StopIteration

    @property
    def rowspan(self) -> int:
        return self._rowspan_amount

    @property
    def has_rowspan(self) -> bool:
        return self._contains_rowspans

    @rowspan.setter
    def rowspan(self, x: int) -> None:
        self._rowspan_amount = x

    @has_rowspan.setter
    def has_rowspan(self, x: bool) -> None:
        self._contains_rowspans = x

    def _set_rowspan(self, rowspan: int, tag: Tag, idx: int) -> None:
        self.rowspan = rowspan
        self.rowspan_cols.append(_RowspanTag(tag, idx))

class TagCleaner:
    '''
    A TagCleaner will properly format every `PageElement` object found in a given `ResultSet`
    of `Tags`.
    '''
    def __init__(self, rows: list[ResultSet[Tag]], args) -> None:
        self._span_newrow   = args.newrow_cr
        self._ext_paren     = args.ext_paren

        self._colmap:    dict[int, partial[None]] = {
            ColType.HEX: partial(self._hex_col),
            ColType.ISO: partial(self._iso_col),
            ColType.OFF: partial(self._off_col),
            ColType.EXT: partial(self._ext_col),
            ColType.DES: partial(self._des_col),
        }
        self._rows: deque[ResultSet[Tag]] = deque(rows)
        self._ptr:  int                   = 0
        self.tags:  list[_TagContainer] = []

    def clean(self) -> list[ResultSet[Tag]]:
        '''
        Cleans all `Tag` objects found in the `BeautifulSoup` wikitable received from the 
        wikimedia API

        :return: list of row[columns]
        '''
        while self._rows:
            self._fill_tag_container(self._rows.popleft(), _TagContainer())

        for row in self.tags:
            for idx, col in enumerate(row):
                self._colmap[idx](col)

        return [cleaned.row_list for cleaned in self.tags]

    def _fill_tag_container(self, row: ResultSet[Tag], tag_container: _TagContainer) -> None:
        for idx, col in enumerate(row):
            tag_container[idx] = col

        self.tags.append(tag_container)
        if tag_container.has_rowspan:
            self._config_rowspan_tags(tag_container)

        self._balance_hexiso_codetags(tag_container)

    def _config_rowspan_tags(self, row: _TagContainer) -> None:
        # If we have rowspan cols we can do one of two things:
        #   - Add the next _ cols to the current instance with rowspans
        #   - Create an entire new _TagContainer instance
        while row.rowspan > 1:
            next_row = self._rows.popleft()
            if self._span_newrow:
                spanned_row = _TagContainer()

                for span_col in row.rowspan_cols:
                    spanned_row[span_col.idx] = span_col.tag

                for idx, col in enumerate(spanned_row):
                    if col.name == '':
                        spanned_row[idx] = next_row.pop(0)

                self.tags.append(spanned_row)
            else:
                for idx, col in enumerate(row):
                    if idx not in [r_idx.idx for r_idx in row.rowspan_cols]:
                        row[idx].extend(next_row.pop(0))

            row.rowspan -= 1

    def _balance_hexiso_codetags(self, container: _TagContainer) -> None:
        code_tags = [(ColType.HEX, container[ColType.HEX].find_all('code')),
                     (ColType.ISO, container[ColType.ISO].find_all('code'))]
        code_tags.sort(key=lambda tupl: len(tupl[1]), reverse=True)
        diff = abs(len(code_tags[0][1]) - len(code_tags[1][1]))

        while diff != 0:
            if len(code_tags[1][1]) == 0: # No code tags
                if container[code_tags[1][0]].get_text() == '':  # No NavigableString(s) in <td>
                    self._add_child_to_tag(src_tag=container[code_tags[1][0]], name='code')
                else:  # Has unwrapped content
                    self._wrap_tag_contents(src_tag=container[code_tags[1][0]], new_name='code')
            else:  # Imbalanced
                self._add_child_to_tag(src_tag=container[code_tags[1][0]], name='code')
            diff -= 1

    def _hex_col(self, col: Tag) -> None:
        for code_tag in col.find_all('code'):
            for char in JNK_CHARS:
                code_tag.string = code_tag.get_text().replace(char, '').lower()

    def _iso_col(self, col: Tag) -> None:
        self._clean_children(col)

    def _off_col(self, col: Tag) -> None:
        self._clean_children(col)

    def _ext_col(self, col: Tag) -> None: 
        self._clean_children(col)

        if self._ext_paren:
            if col.get_text().count('('):
                cleaned = re.sub(pattern=r'\s?\(.*?\)',
                                 repl='',
                                 string=col.get_text(separator='\n'),
                                 flags=re.DOTALL).splitlines()

                col.clear(decompose=True)
                for idx, cleaned_col in enumerate(cleaned):
                    col.insert(idx, cleaned_col)

    def _des_col(self, col: Tag) -> None:
        self._clean_children(col)

    @staticmethod
    def _add_child_to_tag(src_tag: Tag, name: str) -> None:
        child = Tag(name=name)
        src_tag.append(child)

    @staticmethod
    def _wrap_tag_contents(src_tag: Tag, new_name: str) -> None:
        new_tag = Tag(name=new_name)
        new_tag.string = src_tag.get_text()
        src_tag.clear()
        src_tag.append(new_tag)

    @staticmethod
    def _clean_children(col: Tag) -> None:
        '''
        Removes/formats all found `PageElement` objects from a given `Tag` based on their 
        `.name` property.

        :param col: The `Tag` object to format
        '''
        for tag in col.find_all(TAGS):
            if tag.name in FIXTAGS:
                repl_children(tag)
            elif tag.name in BADTAGS:
                destroy(tag)
