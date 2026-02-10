from lib.util import ColType, FileData, USER_ARGS
from lib.exceptions import NoTagFoundError, WikitableFormatError
from collections import defaultdict
from codecs import encode, decode
import re

try:
    from bs4 import Tag, BeautifulSoup, ResultSet
    from bs4.filter import SoupStrainer
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("bs4 not found. Install with -> pip install bs4")
    raise e

wikitable: Tag | BeautifulSoup | None
parser: SoupStrainer = SoupStrainer(name='table', attrs={ 'class': 'wikitable sortable' })

parsedTable: defaultdict[int, ResultSet[Tag]] = defaultdict(lambda: ResultSet(source=None, result=[Tag(name='') for _ in range(5)]))
listTable: list[dict[str, FileData]] = list()
headers: list[str] = list()

def _format_iso(isoText: str) -> str:
    ...

def _format_table_opts() -> None:
    ...

def _format_hex(hexText: str) -> str:
    qGroup: re.Match[str] | None = None
    hexText = hexText.replace(' ', '').replace('\xa0', '')

    for byteGroup in range(len(re.findall(pattern=r'(\?{2})+', string=hexText))):
        qGroup = re.search(pattern=r'(?:\?{2})+', string=hexText)

    if qGroup:
        qByteAmount = qGroup.group(0).count('??')
        hexText = str(hexText[:qGroup.start()] + hexText[qGroup.end():])

    hex = bytes.fromhex(hexText)
    return str(hex.hex(sep=' '))

def _mk_file_dict() -> None:
    global listTable

    for row in parsedTable:
        fileSig: dict[str, FileData] = dict()
        for idx, col in enumerate(parsedTable[row]):
            match idx:
                case ColType.HEX:
                    hex: list[str | bytes] = list()
                    for codeTag in col.find_all('code'):
                        hex.append(_format_hex(codeTag.extract().get_text().replace(' ', '').replace('\xa0', '')))
                        # if hex != "":
                        #     hex += '\n'+_format_hex(codeTag.extract().get_text().replace(' ', '').replace('\xa0', ''))
                        # else:
                        #     hex = _format_hex(codeTag.extract().get_text().replace(' ', '').replace('\xa0', ''))

                    fileSig[col.name] = hex
                case ColType.ISO:
                    fileSig[col.name] = col.get_text()
                case ColType.OFF:
                    fileSig[col.name] = col.get_text()
                case ColType.EXT:
                    fileSig[col.name] = col.get_text()
                case ColType.DES:
                    fileSig[col.name] = col.get_text()
                case _:
                    raise WikitableFormatError()
        listTable.append(fileSig)

def _format_tag_children(col: Tag) -> None:
    badTags = ['cite', 'sup', 'span']
    fixTags = ['a']

    for tag in badTags:
        for colTag in col.find_all(tag):
            colTag.decompose()

    for tag in fixTags:
        for childTag in col.find_all(tag):
            _ = childTag.replaceWithChildren()

    for codeTag in col.find_all('code'):
        for br in codeTag.find_all('br'):
            _ = br.extract()

def _parse_wikitable(wikitable: Tag) -> None:
    global parsedTable
    global headers
    rows = [row.find_all(['td', 'th']) for row in wikitable.select('tr')]
    headers = [re.sub(pattern=r'\n', repl='', string=x.extract().get_text()) for x in rows.pop(0)[:]]

    if len(headers) != 5:
        e = WikitableFormatError()
        e.add_note("Problem initializing wikitable parser - could not find the expected 5 <th> tags")
        raise e

    for rowIdx, row in enumerate(rows):
        for colIdx, col in enumerate(row):
            _format_tag_children(col)
            if col.has_attr('rowspan'):
                for i in range(int(col.attrs['rowspan'][0])):
                    parsedTable[rowIdx + i][colIdx] = col
                    parsedTable[rowIdx + i][colIdx].name = headers[colIdx]
                del col.attrs['rowspan']
                continue
            if len(row) != 5:
                for i in range(len(row)):
                    if parsedTable[rowIdx][i].name == '':
                        parsedTable[rowIdx][i] = col
                        parsedTable[rowIdx][i].name = headers[i]
                        break
                continue
            parsedTable[rowIdx][colIdx] = col
            parsedTable[rowIdx][colIdx].name = headers[colIdx]
    _mk_file_dict()

def parse_html(html: str) -> list[dict[str, FileData]]:
    global wikitable
    wikitable = BeautifulSoup(markup=re.sub(pattern=r'\n', repl='', string=html), parse_only=parser, features='lxml').select_one('tbody')

    if not (isinstance(wikitable, Tag)):
        e = NoTagFoundError()
        e.add_note("Error formatting wikitable - no <tbody> tag was found.")
        raise e

    _parse_wikitable(wikitable)
    return listTable

def pretty_html(html: str) -> str:
    global wikitable
    if not isinstance(wikitable, Tag):
        wikitable = BeautifulSoup(markup=html, parser=parser, features='lxml')

    if not wikitable:
        e = WikitableFormatError()
        e.add_note("Error formatting wikitable - no <tbody> tag was found.")
        raise e
    
    return wikitable.prettify()
