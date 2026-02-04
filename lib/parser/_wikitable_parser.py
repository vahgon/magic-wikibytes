from lib.exceptions import NoTagFoundError, WikitableFormatError
from collections import defaultdict
import re

try:
    from bs4 import Tag, BeautifulSoup, ResultSet
    from bs4.filter import SoupStrainer
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("bs4 not found. Install with -> pip install bs4")
    raise e

newTable: defaultdict[int, ResultSet[Tag]] = defaultdict(lambda: ResultSet(source=None, result=[Tag(name='') for _ in range(5)]))
def _format_wikitable(wikitable: Tag) -> None:
    rows = [row.find_all(['td', 'th']) for row in wikitable.select('tr')]
    headers = [re.sub(pattern=r'\n', repl='', string=x.extract().get_text()) for x in rows.pop(0)[:]]

    global newTable
    for rowIdx, row in enumerate(rows):
        for colIdx, col in enumerate(row):
            if 'rowspan' in col.attrs:
                for i in range(int(col.attrs['rowspan'][0])):
                    newTable[rowIdx + i][colIdx] = col
                del col.attrs['rowspan']
                continue
            if len(row) != 5:
                for i in range(len(newTable[rowIdx])):
                    if newTable[rowIdx][i].name == '':
                        newTable[rowIdx][i] = col
                        break
                continue
            newTable[rowIdx][colIdx] = col
    for e in newTable:
        for i in newTable[e]:
            print(i.get_text())
        
        input()
        print()

def parse_html(html: str) -> None:
    parser = SoupStrainer(name='table', attrs={ 'class': 'wikitable sortable' })
    wikitable = BeautifulSoup(markup=html, parse_only=parser, features='lxml').select_one('tbody')

    if not (isinstance(wikitable, Tag)):
        e = NoTagFoundError()
        e.add_note("Error formatting wikitable - no <tbody> tag was found.")
        raise e

    _ = _format_wikitable(wikitable)

def pretty_html(html: str) -> str:
    ...
